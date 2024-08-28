## This is the main file to run to start all needed processes
from log import Logging, level # custom logging library
import flask, os, db, pickle
app = flask.Flask(__name__) # for the webserver making thing
log = Logging()


## Databases
users = db.Database("db/users.dbfile")
lessons = db.Database("db/lessons.dbfile")
flash = db.Database("db/flashcards.dbfile")
lead = db.Leaderboard()

## Make sure the developer user exists
developer = users.get("developer")
if developer == None:
    developer = db.helpers.User("Quizzle", "unsafepassword")
    users.put("developer", developer)

## Make sure the tutorials are loaded
tutorial = lessons.get("welcome")
if tutorial == None:
    # long line
    tutorial = db.helpers.lesson("welcome", "[Tutorial] Welcome to Quizzle", "developer", "The tutorial that you load into when you first make an account", [{'type': 'slide', 'question': 'Welcome to Quizzle!', 'answers': ['Hello, Traveller!<br>This is <b>Quizzle</b>, a fun app that help you study for upcoming tests and assignments<br><i>Press "Enter" to continue</i>']}, {'type': 'slide', 'question': '', 'answers': ['You are currently in a lesson, which has 5 types of content:<br>A slide (which is what you are currently on!), Multiple Choice 4, Mulitple Choice 3 and Multiple Choice 2<br><i>Don\'t forget to press "Enter" once you have finished a slide or answered a question to move on</i>']}, {'type': 'multi-4', 'question': 'How many different content types are there in the lessons feature?', 'answers': ['5', '4', '3', '6']}, {'type': 'slide', 'question': '', 'answers': ["<b>Great job!</b><br>Now that you've mastered the basics of lessons, let's talk about everything else."]}, {'type': 'slide', 'question': 'The Home page', 'answers': ['<img src="/static/tutorial/home.png"><br>The home page is your landing page for everything in Quizzle. It contains your recent sets, lessons, and more.']}, {'type': 'slide', 'question': 'The Lessons and Sets pages', 'answers': ['<img src="/static/tutorial/lessons.png"><img src="/static/tutorial/sets.png"><br>These are where you will find all of the respective activities. <br>It also contains your recent and starred sets/lessons'], 'answer': '<img src="/static/tutorial/lessons.png"><img src="/static/tutorial/sets.png"><br>These are where you will find all of the respective activities. <br>It also contains your recent and starred sets/lessons'}, {'type': 'slide', 'question': 'The Leaderboard page', 'answers': ['<img src="/static/tutorial/leaderboard.png"><br>The leaderboard page shows how many points you (and your friends) have. <br>Points are earned by studying a flashcard set or finishing a lesson.<br>In fact, you\'re earning points right now!']}, {'type': 'slide', 'question': 'Lessons and Points', 'answers': ['When you complete a lesson, the amount of points you get depends on the number of questions you get correct.<br><img src="/static/tutorial/points.png>']}, {'type': 'slide', 'question': 'Pop Quiz!', 'answers': ["Get ready to test what you've learnt in this lesson!"]}, {'type': 'multi-4', 'question': 'How many different sections are there?', 'answers': ['4', '3', '5', '2']}, {'type': 'multi-3', 'question': 'Which icon is the "sets" section icon?', 'answers': ['<img src="/static/tutorial/sets.png">', '<img src="/static/tutorial/home.png">', '<img src="/static/tutorial/lessons.png">']}, {'type': 'multi-2', 'question': 'You have finished your first lesson!', 'answers': ['True', 'False']}])
    lessons.put("welcome", tutorial)
tutorial = flash.get("welcome")
if tutorial == None:
    tutorial = db.helpers.flash("welcome", "[Tutorial] Welcome to Flashcards", "developer", [{'term': 'These are flashcard sets (press space)', 'definition': 'Tada! (now press enter to move to the next card)'}, {'term': 'There are 2 parts to flashcards', 'definition': 'The term, and the definition'}, {'term': 'This is the term', 'definition': 'This is the definition'}, {'term': 'Pretty simple right?', 'definition': 'When you reach the end, you get 10 points.'}, {'term': 'Now your turn!', 'definition': 'Go find a set or make one yourself!'}])
    flash.put("welcome", tutorial)

def startupwebserver():
    global app
    from threading import Thread
    import wapp, server, wikipedia_bypass # gathers all the files
    return Thread(target=startupwebserverprocess, name="webserver", daemon=True) # create the thread
def startupwebserverprocess():
    global app
    app.run(host="0.0.0.0",port=5000,debug=False)

    

if __name__ == "__main__":
    import sys, time
    webprocess = startupwebserver()
    log.log("Starting webserver")
    webprocess.start() # start the webserver
    log.log("webprocesss started", level.done)
    log.log("starting loop")
    while True:
        try: pass
        except KeyboardInterrupt: break
    log.log("Bye!",level.exit)
