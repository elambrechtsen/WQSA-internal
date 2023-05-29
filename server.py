from flask import Flask, render_template, request

app = Flask(__name__)


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
    return render_template("news.html")


if __name__ == "__main__":
    app.run(debug=True)
