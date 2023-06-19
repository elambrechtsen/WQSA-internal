from flask import Flask, render_template, request, url_for, redirect
from db_functions import run_search_query_tuples, run_commit_query
from datetime import datetime

app = Flask(__name__)
db_path = 'data/WQSA_db.sqlite'

@app.template_filter()
def news_date(sqlite_dt):
    # create a date object
    x = datetime.strptime(sqlite_dt, '%Y-%m-%d %H:%M:%S')
    return x.strftime("%a %d %b %y %H:%M")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/error")
@app.errorhandler(404)
def not_found(e='Error'):
    return render_template("error.html", error=e)


@app.route("/meet_the_team")
def meet_the_team():
    return render_template("meet_the_team.html")


@app.route("/upcoming_events")
def upcoming_events():
    return render_template("upcoming_events.html")


@app.route("/get_involved", methods=["GET", "POST"])
def get_involved():
    if request.method == "POST":
        f = request.form
        print(f)
        print(f['firstname'])
       

        return render_template("confirm.html", form_data=f)
    elif request.method == "GET":
        temp_form_data = {
        "firstname" : "James",
        "lastname"  : "Smith",
        "email" : "james@gmail.com",
        "aboutme" : "love everything and everyone"
        }
        return render_template("get_involved.html", **temp_form_data)

@app.route("/news")
def news():
    sql = """select news.news_id, news.title, news.subtitle, news.content, news.newsdate, member.name
      from news
      join member on news.member_id = member.member_id
      order by news.newsdate desc;

      """
    result = run_search_query_tuples(sql, (), db_path, True)
    print(result)

    return render_template("news.html", news=result)

@app.route("/news_cud", methods=['GET', 'POST'])
def news_cud():
    # arrive at the pade in either et or post arrived
    data = request.args
    required_keys=['id', 'task']
    for k in required_keys:
        if k not in data.keys():
            message = "Do not know what to do with create, read, update on news (keys not present)"
            return render_template('error.html', error=message)
        if request.method == "GET":
            if data['task'] == 'delete':
                sql = "delete from news where news_id =?"
                values_tuple = (data['id'],)
                result = run_commit_query(sql, values_tuple, db_path)
                return redirect(url_for('news'))

            elif data['task'] == 'update':
                # populate e form with current data
               # sql = """select title, subtitle, content from news where news_id =?"""
                # sql = """update news set title=?, subtitle=?, content=?, newsdate=datetime('now') where news_id=?"""
                return "<h1> I want to update </h1>"
            elif data['task'] == 'add':
                temp = {"title": "Temp title", "subtitle": "Test subtitle", 'content': 'Test Content'}
                return render_template("news_cud.html", id=0, task=data['task'],
                                       title=temp['title'],
                                       subtitle=temp['subtitle'],
                                       content=temp['content'])

            else:
                message = 'unrecognised task from news page'
                return render_template('error.html', error=message)

        elif request.method == "POST":
            # collect form information
            f = request.form
            print(f)
            # add the news entry to the database
            #member is fixed for now
            if data['task'] == 'add:'
                sql = "insert into news(title, subtitle, content, newsdate, member_id) values (?,?,?, datetime('now'),2)"
                values_tuples = (f['title'], f['subtitle'], f['content'])
                result = run_commit_query(sql, values_tuples, db_path)
            else:
                return "<h1>Posting for update </h1>"
            return redirect(url_for('news'))



    return render_template("news_cud.html")

if __name__ == "__main__":
    app.run(debug=True)
