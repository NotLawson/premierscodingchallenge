## WEB APP ##
from flask import Flask, render_template, url_for, request, redirect, make_response
from datetime import datetime
import db, helper, random # import utils
from log import Logging, level


if __name__=="__main__": # when running standalone
    app = Flask(__name__)
    log = Logging("web app", level.debug)
    
    users = db.Database("db/users")
    lessons = db.Database("db/lessons")
    flash = db.Database("db/flash")
    lead = db.Leaderboard()

else: # when running in main file
    from __main__ import app, log, users, lessons, flash, lead

@app.route("/")
def index():
    # Homepage

    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)
    userobj = users.get(resp["user"])


    # format date string
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

    suggestions = []
    # suggestions: what this does is grab a random starred set, random starred lesson, 2 most recent sets, 2 most recent lessons,
    # and 2 more suggestion slots reserved for later if I end up implementing the classes and assignments features

    # Sets
    try:
        set = userobj.recent_sets[0]
        setobj = flash.get(set)
        if setobj == None: raise Exception # break out of try loop
        suggestions.append(helper.Suggestion("↺ - "+setobj.name, "/sets/"+set,""))
    except Exception as e:
        print("Exception caught:",e)
        pass # ignore that it failed, most likely due to phantom sets or none at all
    try:
        set = userobj.recent_sets[1]
        setobj = flash.get(set)
        if setobj == None: raise Exception # break out of try loop
        suggestions.append(helper.Suggestion("↺ - "+setobj.name, "/sets/"+set,""))
    except Exception as e:
        print("Exception caught:",e)
        pass # ignore that it failed, most likely due to phantom sets or none at all
    try:
        set = userobj.starred_sets[random.randint(0, len(userobj.starred_sets)-1)]
        setobj = flash.get(set)
        if setobj == None: raise Exception # break out of try loop
        suggestions.append(helper.Suggestion("★ - "+setobj.name, "/sets/"+set,""))
    except Exception as e:
        print("Exception caught:",e)
        pass # ignore that it failed, most likely due to phantom sets or none at all

    # Lessons (essentially the same thing)
    try:
        lesson = userobj.recent_lessons[0]
        lessonobj = lessons.get(lesson)
        if lessonobj == None: raise Exception # break out of try loop
        suggestions.append(helper.Suggestion("↺ - "+lessonobj.name, "/lessons/"+lesson,""))
    except Exception as e:
        print("Exception caught:",e)
        pass # ignore that it failed, most likely due to phantom lessons or none at all
    try:
        lesson = userobj.recent_lessons[1]
        lessonobj = lessons.get(lesson)
        if lessonobj == None: raise Exception # break out of try loop
        suggestions.append(helper.Suggestion("↺ - "+lessonobj.name, "/lessons/"+lesson,""))
    except Exception as e:
        print("Exception caught:",e)
        pass # ignore that it failed, most likely due to phantom lessons or none at all
    try:
        lesson = userobj.starred_lessons[random.randint(0, len(userobj.starred_lessons)-1)]
        lessonobj = lessons.get(lesson)
        if lessonobj == None: raise Exception # break out of try loop
        suggestions.append(helper.Suggestion("★ - "+lessonobj.name, "/lessons/"+lesson,""))
    except Exception as e:
        print("Exception caught:",e)
        pass # ignore that it failed, most likely due to phantom lessons or none at all

    if len(suggestions) == 0: # check if there aren't any (which is likely for ftu) so it doesn't look broken
        suggestions.append(helper.Suggestion("Nothing here...", "/", "Get out there and study to get some suggestions!"))


    return render_template("home.html", title="Home", user = userobj, date = final_date, suggestions = suggestions)

@app.route("/leaderboard")
def leaderboard():
    # Leaderboard Page
    # This page shows how many points users have and contains a leaderboard
    # You earn point by completing sets and lessons

    # AUTH
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)

    leaderboardlist=lead.leaderboard() # get leaderboard list
    for user in leaderboardlist:
        user["name"] = users.get(user["name"]).name # replace the user's username (which is most likely an email) with thier display name
    
    return render_template("leaderboard.html", title="Leaderboard", leaderboardlist=leaderboardlist) # pass to jinja template

@app.route("/sets")
def sets():
    # Sets Page
    # This page shows all the sets available to study.
    # It also has sections containing Starred Sets, and Recent Sets

    # AUTH
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)
    

    # Main Sets section
    sets = [] # init sets list
    refs = flash.keys()

    for ref in refs: # iterate through the keys in the database
        set = flash.get(ref) # grab the object from the data base
        set.author = users.get(set.author).name # adjust the author name to a display name
        sets.append(set) # add the object to the sets list

    # Recent Sets section
    recents = []
    recent_sets = users.get(resp["user"]).recent_sets # get the keys of all recent sets from the user object

    for set in recent_sets: # iterate throught the recent sets
        # In the recents and starred section, an issue I came across when using items from them was that when a set is deleted
        # from the database, the coresponding keys in the recents and starred sections aren't deleted. This leads to the program 
        # attemping to load the data of nonexistent sets, which is and issue. (A) is a short function that when a set can't be found
        # from the lists, it will delete itself. This behaviour is only triggered when going to the lessons and sets main pages, but 
        # there are few other places that reference these lists (one being the home page, which deals with issues by not rendering the suggestion)

        setid=set
        set = flash.get(set) # grab the set object
        if set == None: obj = users.get(resp["user"]); obj.recent_sets.remove(setid); users.put(resp["user"], obj); break # (A)
        set.author = users.get(set.author).name # adjust the author name
        recents.append(set) # add to recents set


    # Starred Sets section
    # see above for main documentation
    starred = []
    starred_sets = users.get(resp["user"]).starred_sets
    for set in starred_sets:
        setid=set
        set = flash.get(set)
        if set == None: obj = users.get(resp["user"]); obj.starred_sets.remove(setid); users.put(resp["user"], obj); break
        set.author = users.get(set.author).name
        starred.append(set)

    return render_template("sets.html", title="Sets", sets=sets, recents=recents, starred=starred, len=len) # pass everything to jinja

@app.route("/sets/<setid>")
def sets_info(setid):
    # Set info page
    # This page allows users to view information about, play, star or delete a specific set.

    # AUTH
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)
    
    setobj = flash.get(setid) # get the set object

    if resp["user"] == setobj.author: setobj.owned = True # match the author to the user. If True, set the "setobj.owned" to true.

    if setid in users.get(resp["user"]).starred_sets: # check if the set is in the current user's starred sets
        starred=True
    else:
        starred=False
    
    setobj.author = users.get(setobj.author).name # adjust the author name

    return render_template("setinfo.html", set=setobj, username = resp["user"], starred=starred) # render the page

@app.route("/sets/create", methods = ["GET", "POST"])
def create_set():
    # Set creation page
    # Documentation will be in the templates/setcreator.html
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)
    return render_template("setcreator.html")

@app.route("/flashcards")
def flashcards_player():
    # Flashcards Player
    # This page "plays" the flashcards
    # See "/play/<setid>" for full docmentation

    # AUTH
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)

    progress = int(request.cookies.get("question")) # get the current progress from cookies
    setid = request.cookies.get("setid") # get the set it from cookies
    setobj = flash.get(setid) # grab the set object

    try: 
        question = setobj.content[progress-1] # Attempt to find the correct question. If at the end, IndexError is raised and caught.

    except IndexError:
        lead.addscore(resp["user"], 10) # add 10 point to the user's score
        return render_template("flashcards/end.html", set=setobj) # render the end page
    
    return render_template("flashcards/card.html", set=setobj, progress=progress-1,progressjs = progress, question=question, int=int) # render the normal flashcard page

@app.route("/play/<setid>")
def play(setid):
    # Play endpoint
    # This just sets the cookies and redirects to the player

    # OVERALL PLAYER #
    # The player works like this:
    #    - It saves the set id, and card no. in cookies
    #    - When you got to the next card, it just reloads the page
    #    - The webserver then renders the page and passes data like card content etc to the JS
    #    - The JS then handles clicking through the cards, and updating data
    #    - The Flashcard content is stored in a 'flash' class, and is just JSON

    # AUTH
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)
    

    userobj = users.get(resp["user"]) # get user object

    # handle placing the set in recentss
    if setid in userobj.recent_sets: userobj.recent_sets.remove(setid)
    userobj.recent_sets.insert(0, setid)
    users.put(resp["user"], userobj)

    resp = make_response(redirect("/flashcards")) # make the response
    # set cookies
    resp.set_cookie("setid", setid)
    resp.set_cookie("question", "1")
    resp.set_cookie("score", "0")

    return resp # render

@app.route("/sets/clear_recents")
def clear_recent_sets():
    # Clear recent sets
    # this is just a small endpoint that clears all recent sets

    # AUTH
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)
    
    userobj = users.get(resp["user"]) # get the user object
    userobj.recent_sets = [] # reset :D
    users.put(resp['user'], userobj) # put the user object back

    return redirect("/sets") # render


## LESSONS
# This is VERY similar to the flashcards above, so explanations will not be as in depth

@app.route("/lessons")
def lessons_home():
    # Lessons Home page
    # See Flashcards home page for documentation

    # AUTH
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)
    lessons_l = []
    refs = lessons.keys()

    for ref in refs:
        lesson = lessons.get(ref)
        lesson.author = users.get(lesson.author).name
        lessons_l.append(lesson)
    
    recents = []
    recent_lessons = users.get(resp["user"]).recent_lessons
    for lesson in recent_lessons:
            lessonid=lesson
            lesson = lessons.get(lesson)
            if lesson == None: obj = users.get(resp["user"]); obj.recent_lessons.remove(lessonid); users.put(resp["user"], obj); break
            lesson.author = users.get(lesson.author).name
            recents.append(lesson)

    starred = []
    starred_lessons = users.get(resp["user"]).starred_lessons
    for lesson in starred_lessons:
        lessonid=lesson
        lesson = lessons.get(lesson)
        if lesson == None: obj = users.get(resp["user"]); obj.starred_lessons.remove(lessonid); users.put(resp["user"], obj); break
        try: lesson.author = users.get(lesson.author).name
        except: pass
        starred.append(lesson)

    print(recents)
    print(recent_lessons)
    return render_template("lessons.html", title="Lessons", lessons=lessons_l, recents=recents, starred=starred, len=len)

@app.route("/player")
def player():
    # Lessons endpoint
    # This just sets the cookies and redirects to the player
    # This is pretty much the same as the flashcards player, with a few key differences
    #    - Score is also tracked in cookies
    #    - There are slides, and questions where you need to click the answer to proceed
    #        - NOTE ABOUT SLIDES: You can put plain html into the slide content box. While this is a big security flaw, it also has 
    #          many practical uses such as embeding Youtube videos, MP4s, Images, and other HTML code. If this ever goes into production,
    #          I would have to clean the inputs of <script>, <link> etc OR use a whitelist of <iframe>, <h#>, <a>, etc to get rid of any 
    #          security issues. Until then, call it a feature ;D

    # AUTH
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)
    
    progress = int(request.cookies.get("question")) # get the progress cookie
    setid = request.cookies.get("lessonid") # get the id
    setobj = lessons.get(setid) # grab the set object

    try: 
        question = setobj.content[progress-1] # Attempt to find the correct question. If at the end, IndexError is raised and caught
    except IndexError:
        # The score here is a bit different. Instead of just giving a score of 10 when finished, it will only award a percentage of 10, 
        # based on how many questions the user got right.

        score = int(request.cookies.get("score")) # get the score cookie

        points = int(round(((score/setobj.total)*10), 0)) # don't even ask me what this is. It works, and that's all you need to know

        lead.addscore(resp["user"], points) # add the score to the leaderboard

        return render_template("lessons/end.html", lesson=setobj, score = score, points = points) # render
    
    # if there are still questions to go, find the question type:
    #  - multi-4: Multiple Choice 4
    #  - multi-3: Multiple Choice 3
    #  - multi-2: Muliple Choice 2 (True or False)
    #  - slide: Non-question content, such as a YT video, demo working out, etc
    
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
    # Lesson info page
    # Same as Set info page, look there

    # AUTH
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)
    
    lessonobj = lessons.get(lessonid) # get lesson object

    if resp["user"] == lessonobj.author: lessonobj.owned = True # check is owned

    if lessonid in users.get(resp["user"]).starred_lessons: # check starred
        starred=True
    else:
        starred=False
    
    lessonobj.author = users.get(lessonobj.author).name # adjust author name

    return render_template("lessoninfo.html", lesson=lessonobj, username = resp["user"], starred=starred) # render

@app.route("/lessons/create", methods = ["GET", "POST"])
def create_lesson():
    # Lesson creator page
    # Documentation will be in templates/lessoncreator.html
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)
    return render_template("lessoncreator.html")


@app.route("/learn/<lessonid>")
def learn(lessonid):
    # learn endpoint
    # exactly the same as the play endpoint

    # AUTH
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)
    userobj = users.get(resp["user"])

    # handle recents
    if lessonid in userobj.recent_lessons: userobj.recent_lessons.remove(lessonid)
    userobj.recent_lessons.insert(0, lessonid)
    users.put(resp["user"], userobj)

    resp = make_response(redirect("/player")) # make response
    # set cookies
    resp.set_cookie("lessonid", lessonid)
    resp.set_cookie("question", "1")
    resp.set_cookie("score", "0")

    return resp # render

@app.route("/lessons/clear_recents")
def clear_recent_lessons():
    # Clear recent lessons handle
    # same as the clear recent sets handle

    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)
    
    userobj = users.get(resp["user"])
    userobj.recent_lessons = []
    users.put(resp['user'], userobj)

    return redirect("/lessons") # render

# phew, documentation is hard work


@app.route("/login", methods = ["GET", "POST"])
def login():
    # Login page

    # If submiting the login form
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users.keys(): # check to make sure the username is vaild
            userobj = users.get(username) # then grab the user object
        else:
            return render_template("login.html", message = "Wrong username", title = "Login") # render wrong username
        
        if userobj.password == (password): # check the password is correct
            token=helper.generate_token(username) # generate a token

            path = request.args.get("redirect", "/") # find the redirect path, with the default being "/"

            resp = make_response(redirect(path)) # make response
            resp.set_cookie("token", token) # set the token cookie

            return resp # render
        return render_template("login.html", message = "Wrong Password", title = "Login") # render wrong password
    
    # Or, if just loading the form
    return render_template("login.html", message = None, title = "Login") # render the login page

@app.route("/createuser", methods = ["GET", "POST"])
def create_user():
    # User creation form
    # similar to the Login page

    # if submiting the form
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("name")

        if username in users.keys(): # make sure that the username is clear
            return render_template("createuser.html", message = "User already exists") # render user already exists
        
        users.put(username, db.User(name, password)) # put the new user in the data base

        resp = make_response(redirect("/")) # redirect home

        token=helper.generate_token(username) # create a token
        resp.set_cookie("token", token)       #

        return resp # render
    
    # Or, if loading the form
    return render_template("createuser.html", message = None) # render form

def render_settings(userobj):
    # This is a simple function to help render to settings for a user
    # However, there weren't as many settings as I anticipated, so it is kind of useless.
    dict_ = {
        "name":userobj.name,
    }
    return dict_

@app.route("/settings", methods = ["GET", "POST"])
def settings():
    # Settings page

    # AUTH
    resp = helper.authw(request)
    if resp["code"] == 401:
        return redirect("/login?redirect="+request.path)
    userobj = users.get(resp["user"])

    username = resp["user"]
    message = None

    # if submiting a settings update
    if request.method == "POST":
        message = "Updated" # set the message to updated

        name = request.form.get("name")
        if name != "": # if the name has been changed
            userobj.name = name
        
        password = request.form.get("password")
        if password != "": # if the password has been changed
            userobj.password = request.form.get("password")

        users.put(username, userobj) # put the user object
        
    return render_template("settings.html", message = message, settings=render_settings(userobj)) # render page


if __name__ == "__main__":
    app.run(port=5001, debug=True)
