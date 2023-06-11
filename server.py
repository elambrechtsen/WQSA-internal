from flask import Flask, render_template, request, url_for
from db_functions import run_search_query_tuples
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

@app.route("/news_cud")
def news_cud():
    return render_template("news_cud.html")

if __name__ == "__main__":
    app.run(debug=True)
