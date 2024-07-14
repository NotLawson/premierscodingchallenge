## WEB APP ##
from flask import Flask, render_template, url_for, request, redirect, make_response
from datetime import datetime
import db, os, helper, json
from log import Logging, level

users = db.user.db()
notes = db.notes.db()
flash = db.flashcards.db()

if __name__=="__main__":
    app = Flask(__name__)
    log = Logging("web app", level.debug)
else:
    from __main__ import app, log

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
    sets = []
    refs = flash.refs()
    for ref in refs:
        sets.append(flash.get(ref))

    return render_template("sets.html", title="Sets", sets=sets)

@app.route("/player")
def player():
    progress = int(request.cookies.get("question"))
    setid = request.cookies.get("setid")
    setobj = flash.get(setid)
    try: 
        question = setobj.content[progress-1]
    except IndexError:
        return render_template("endplayer.html", set=setobj)
    return render_template("player.html", set=setobj, progress=progress-1,progressjs = progress, question=question, int=int)

@app.route("/sets/<setid>")
def sets_info(setid):
    # AUTH
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login")
    log.log(str(flash.refs()), level.warn)
    setobj = flash.get(setid)
    return render_template("setinfo.html", set=setobj, username = resp["user"])

@app.route("/sets/create", methods = ["GET", "POST"])
def create_set():
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login")
    if request.method == "POST":
        name = request.form["name"]
        content = str(request.files["content"].read().decode("utf-8"))
        content = json.loads(content)["content"]
        while True:
            id = helper.generate_id()
            if id not in flash.refs():
                break
        
        setobj = db.flashcards.flash(id, name, resp["user"], content)
        flash.put(id, setobj)
        return redirect("/sets")
    return render_template("createset.html")

@app.route("/play/<setid>")
def play(setid):
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login")
    resp = make_response(redirect("/player"))
    resp.set_cookie("setid", setid)
    resp.set_cookie("question", "1")
    return resp

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        log.log(f"is '{username} in {str(users.refs())}'?")
        if username in users.refs():
            userobj = users.get(username)
        else:
            return render_template("login.html", message = "Wrong username", title = "Login")
        log.log(f"does {password} equal {userobj.password}?")
        if userobj.password == (password):
            token=helper.generate_token(username)
            resp = make_response(redirect("/"))
            resp.set_cookie("token", token)
            return resp
        return render_template("login.html", message = "Wrong Password", title = "Login")
    return render_template("login.html", message = None, title = "Login")

@app.route("/createuser", methods = ["GET", "POST"])
def create_user():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("name")
        if username in users.refs():
            return render_template("createuser.html", message = "User already exists")
        log.log(f"Creating user {username} with password {password}")
        users.put(username, db.user.User(name, password))
        resp = make_response(redirect("/"))
        token=helper.generate_token(username)
        resp.set_cookie("token", token)
        return resp
    return render_template("createuser.html", message = None)

def render_settings(userobj):
    dict_ = {
        "name":userobj.name,
    }
    return dict_

@app.route("/settings", methods = ["GET", "POST"])
def settings():
    # AUTH
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login")
    userobj = users.get(resp["user"])
    username = resp["user"]
    message = None
    if request.method == "POST":
        message = "Updated"
        name = request.form.get("name")
        if name != "":
            userobj.name = name
            log.log(f"Name Change: {name}")
        password = request.form.get("password")
        if password != "":
            userobj.password = request.form.get("password")
            log.log(f"Password change: '{password}'")
        users.put(username, userobj)
        
    return render_template("settings.html", message = message, settings=render_settings(userobj))


if __name__ == "__main__":
    app.run(port=5001, debug=True)
