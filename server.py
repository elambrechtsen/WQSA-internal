from flask import Flask, render_template, request, url_for, redirect, session
from db_functions import run_search_query_tuples, run_commit_query
from datetime import datetime

app = Flask(__name__)
app.secret_key = "pjdghhhhhwdsa"
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
    news = run_search_query_tuples(sql, (), db_path, True)
    print(news)

    sql = """select news.news_id, comments.comments_content, comments.comments_date
      from news
      join comments on news.news_id = comments.news_id
      order by news.newsdate desc;
      """
    comments = run_search_query_tuples(sql, (), db_path, True)
    print(comments)
    return render_template("news.html", news=news, comments=comments)


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
                sql = """select title, subtitle, content from news where news_id =?"""
                values_tuple = (data['id'],)
                result = run_search_query_tuples(sql, values_tuple, db_path, True)
                result = result[0]
                return render_template("news_cud.html",
                                       **result,
                                       id=data['id'],
                                       task=data['task'])
            elif data['task'] == 'add':
                temp = {"title": "Temp title", "subtitle": "Test subtitle", 'content': 'Test Content'}
                return render_template("news_cud.html", id=0, task=data['task'],
                                        **temp)

            else:
                message = 'unrecognised task from news page'
                return render_template('error.html', error=message)

        elif request.method == "POST":
            # collect form information
            f = request.form
            print(f)
            # add the news entry to the database
            #member is fixed for now
            if data['task'] == 'add':
                sql = """insert into news(title, subtitle, content, newsdate, member_id) values (?,?,?, datetime('now', 'localtime'),?)"""
                values_tuples = (f['title'], f['subtitle'], f['content'], session['member_id'])
                result = run_commit_query(sql, values_tuples, db_path)
                #once added redirect to the news page to see newly added item
                return redirect(url_for('news'))

            elif data['task'] == 'update':
                sql = """update news set title=?, subtitle=?, content=?, newsdate=datetime('now') where news_id=?"""
                values_tuples = (f['title'], f['subtitle'], f['content'], data['id'])
                result = run_commit_query(sql, values_tuples, db_path)
                #collect the data from the form and update datbase from at the sent id
                return redirect(url_for('news'))
    return render_template("news_cud.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    print(session)
    error = "Your credentials are not recognised"
    if request.method == 'GET':
        return render_template('log-in.html', email='mike@gmail.com', password='temp')
    elif  request.method == 'POST':
        f=request.form
        print(f)
        sql = """ select member_id, name, password, authorisation from member where email = ?"""
        values_tuple =(f['email'],)
        result = run_search_query_tuples(sql, values_tuple, db_path, True)
        if result:
            result = result[0]
            if result['password'] == f['password']:
                #start a session
                session['name']=result['name']
                session['authorisation'] = result['authorisation']
                session['member_id'] = result['member_id']
                return redirect(url_for('index'))
            else:
                return render_template('log-in.html', email='mike@gmail.com', password='temp', error=error)
            return "<h1> Result is recognised </h1>"
        else:
            return render_template('log-in.html', email='mike@gmail.com', password='temp', error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
