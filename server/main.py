## This is the main file to run to start all needed processes

## First of all, messaging
from multiprocessing import Queue
from log import Logging, level # custom logging library
import flask
app = flask.Flask(__name__) # for the webserver making thing
log = Logging()

apiq = Queue() # input Queue for the api server
wappq = Queue() # input Queue for the web app server
events = Queue() # For general server events like restart, shutdown, so on so forth\

'''if __name__ == "__main__":
    from subprocess import Popen
    import sys
    import time

    apip = Popen([sys.executable,"server.py"], shell=True)
    print("Started API")
    appp = Popen([sys.executable, "app.py"], shell=True)
    print("Started app")
    print("Starting loop...")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print("Detected ctr+c, breaking...")
            break
    print("Killing subprocesses...")
    apip.kill()
    appp.kill()
    print("Processes killed, exiting")'''

def startupwebserver():
    global app
    from threading import Thread
    import wapp, server
    return Thread(target=startupwebserverprocess, name="webserver", daemon=True)
def startupwebserverprocess():
    global app
    app.run(port=5000,debug=False)

    

if __name__ == "__main__":
    import sys, time
    webprocess = startupwebserver()
    log.log("Starting webserver")
    webprocess.start()
    log.log("webprocesss started", level.done)
    log.log("starting loop")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            log.log("Detected ctr+c, breaking...",level.warn)
            break
    log.log("Bye!",level.exit)
