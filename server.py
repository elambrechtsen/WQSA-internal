from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/Meet the team")
def menu():
    return render_template("meet_the_team.html")


@app.route("/Upcoming events")
def upcoming_events():
    return render_template("upcoming_events.html")

@app.route("/Get involved")
def get_involved():
    return render_template("get_involved.html")


if __name__ == "__main__":
    app.run(debug=True)
