## WEB APP ##
from flask import Flask, render_template, url_for, request, redirect, make_response
from datetime import datetime
import db, os, helper, json
from log import Logging, level


if __name__=="__main__":
    app = Flask(__name__)
    log = Logging("web app", level.debug)
    
    users = db.Database("db/users")
    lessons = db.Database("db/lessons")
    flash = db.Database("db/flash")

else:
    from __main__ import app, log, users, lessons, flash

class testobj:
    def __init__(self, name):
        self.name = name

@app.route("/")
def index():
    # AUTH
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)
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
        return redirect("/login?redirect="+request.path)

    return render_template("leaderboard.html", title="Leaderboard")

@app.route("/sets")
def sets():
    # AUTH
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)
    sets = []
    refs = flash.keys()
    for ref in refs:
        sets.append(flash.get(ref))

    return render_template("sets.html", title="Sets", sets=sets)

@app.route("/flashcards")
def flashcards_player():
    progress = int(request.cookies.get("question"))
    setid = request.cookies.get("setid")
    setobj = flash.get(setid)
    try: 
        question = setobj.content[progress-1]
    except IndexError:
        return render_template("flashcards/end.html", set=setobj)
    return render_template("flashcards/card.html", set=setobj, progress=progress-1,progressjs = progress, question=question, int=int)


@app.route("/sets/<setid>")
def sets_info(setid):
    # AUTH
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)
    log.log(str(flash.keys()), level.warn)
    setobj = flash.get(setid)
    return render_template("setinfo.html", set=setobj, username = resp["user"])

@app.route("/sets/create", methods = ["GET", "POST"])
def create_set():
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)
    if request.method == "POST":
        name = request.form["name"]
        content = str(request.files["content"].read().decode("utf-8"))
        content = json.loads(content)["content"]
        while True:
            id = helper.generate_id()
            if id not in flash.keys():
                break
        userobj = users.get(resp["user"])
        setobj = db.flash(id, name, userobj.name, content)
        flash.put(id, setobj)
        return redirect("/sets")
    return render_template("createset.html")

@app.route("/play/<setid>")
def play(setid):
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)
    resp = make_response(redirect("/flashcards"))
    resp.set_cookie("setid", setid)
    resp.set_cookie("question", "1")
    return resp


## LESSONS

@app.route("/lessons")
def lessons_home():
    # AUTH
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)
    sets = []
    refs = lessons.keys()

    for ref in refs:
        sets.append(lessons.get(ref))
    
    recents = []
    recent_lessons = users.get(resp["user"]).recent_lessons
    for lesson in recent_lessons:
        recents.append(lessons.get(lesson))
    starred = []
    starred_lessons = users.get(resp["user"]).starred_lessons
    for lesson in starred_lessons:
        starred.append(lessons.get(lesson))

    print(recents)
    print(recent_lessons)
    return render_template("lessons.html", title="Lessons", lessons=sets, recents=recents, starred=starred, len=len)

@app.route("/player")
def player():
    progress = int(request.cookies.get("question"))
    setid = request.cookies.get("lessonid")
    setobj = lessons.get(setid)
    try: 
        question = setobj.content[progress-1]
    except IndexError:
        return render_template("lessons/end.html", lesson=setobj)
    if question["type"] == "multi-4":
        return render_template("lessons/multi-4.html", set=setobj, progress=progress-1,progressjs = progress, question=question, int=int)
    elif question["type"] == "multi-3":
        return render_template("lessons/multi-3.html", set=setobj, progress=progress-1,progressjs = progress, question=question, int=int)
    elif question["type"] == "multi-2":
        return render_template("lessons/multi-2.html", set=setobj, progress=progress-1,progressjs = progress, question=question, int=int)
    elif question["type"] == "slide":
        return render_template("lessons/slide.html", set=setobj, progress=progress-1,progressjs = progress, question=question, int=int)


@app.route("/lessons/<lessonid>")
def lessons_info(lessonid):
    # AUTH
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)
    log.log(str(lessons.keys()), level.warn)
    lessonobj = lessons.get(lessonid)
    if lessonid in users.get(resp["user"]).starred_lessons:
        starred=True
    else:
        starred=False
    return render_template("lessoninfo.html", lesson=lessonobj, username = resp["user"], starred=starred)

@app.route("/lessons/create", methods = ["GET", "POST"])
def create_lesson():
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)
    if request.method == "POST":
        name = request.form["name"]
        desc = request.form["desc"]
        content = str(request.files["content"].read().decode("utf-8"))
        content = json.loads(content)["content"]
        while True:
            id = helper.generate_id()
            if id not in lessons.keys():
                break
        userobj = users.get(resp["user"])
        lessonobj = db.lesson(id, name, userobj.name, desc, content)
        lessons.put(id, lessonobj)
        return redirect("/lessons")
    return render_template("createlesson.html")

@app.route("/learn/<lessonid>")
def learn(lessonid):
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)
    userobj = users.get(resp["user"])
    recents = userobj.recent_lessons
    if lessonid not in recents:
        recents.reverse()
        recents.append(lessonid)
        recents.reverse()
        userobj.recent_lessons = recents
    else:
        recents.reverse()
        recents.remove(lessonid)
        recents.append(lessonid)
        recents.reverse()
        userobj.recent_lessons = recents
    users.put(resp["user"], userobj)
    resp = make_response(redirect("/player"))
    resp.set_cookie("lessonid", lessonid)
    resp.set_cookie("question", "1")
    return resp
@app.route("/lessons/clear_recents")
def clear_recent_lessons():
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)
    
    userobj = users.get(resp["user"])
    userobj.recent_lessons = []
    users.put(resp['user'], userobj)

    return redirect("/lessons")


@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        log.log(f"is '{username} in {str(users.keys())}'?")
        if username in users.keys():
            userobj = users.get(username)
        else:
            return render_template("login.html", message = "Wrong username", title = "Login")
        log.log(f"does {password} equal {userobj.password}?")
        if userobj.password == (password):
            token=helper.generate_token(username)
            path = request.args.get("redirect", "/")
            print(path)
            resp = make_response(redirect(path))
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
        if username in users.keys():
            return render_template("createuser.html", message = "User already exists")
        log.log(f"Creating user {username} with password {password}")
        users.put(username, db.User(name, password))
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
        return redirect("/login?redirect="+request.path)
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
