## This is the main file to run to start all needed processes
from log import Logging, level # custom logging library
import flask, os, db
app = flask.Flask(__name__) # for the webserver making thing
log = Logging()


## Databases
users = db.Database("db/users.dbfile")
lessons = db.Database("db/lessons.dbfile")
flash = db.Database("db/flashcards.dbfile")
lead = db.Leaderboard()

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
