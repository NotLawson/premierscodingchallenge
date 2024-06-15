## WEB APP ##
from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import db, os, helper
users = db.user.db(os.path.dirname(db.user.__file__)+"/dbfile")
notes = db.notes.db(os.path.dirname(db.notes.__file__)+"/dbfile")
flash = db.flashcards.db(os.path.dirname(db.flashcards.__file__)+"/dbfile")

if __name__=="__main__":
    app = Flask(__name__)
else:
    from __main__ import app    

class testobj:
    def __init__(self, name):
        self.name = name

@app.route("/")
def index():
    # AUTH
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login")
    userobj = users.get(resp["user"])

    day = datetime.now().strftime("%A")
    date_day = datetime.now().strftime("%d")
    if date_day[0] == "1" and len(date_day) == 2:
        date_day += "th"
    else:
        if date_day[-1] == "1":
            date_day += "st"
        elif date_day[-1] == "2":
            date_day += "nd"
        elif date_day[-1] == "3":
            date_day += "rd"
        else:
            date_day += "th"
    month = datetime.now().strftime("%B")

    final_date = f"{day}, the {date_day} of {month}"
    return render_template("home.html", title="Home", user = userobj, date = final_date)

@app.route("/leaderboard")
def leaderboard():
    # AUTH
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login")

    return render_template("leaderboard.html", title="Leaderboard")

@app.route("/sets")
def sets():
    # AUTH
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login")

    return render_template("sets.html", title="Sets")

@app.route("/login", methods = ["GET", "POST"])
def login():
    return "there isn't actually a login page yet, get the token from the api"

if __name__ == "__main__":
    app.run(port=5001, debug=True)
