## This is the main file to run to start all needed processes

## First of all, messaging
from multiprocessing import Queue
#import log # custom logging library
import flask
app = flask.Flask(__name__) # for the webserver making thing

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
    return Thread(target=startupwebserverprocess, name="webserver")
def startupwebserverprocess():
    global app
    app.run(port=5000,debug=False)

    

if __name__ == "__main__":
    import sys, time
    webprocess = startupwebserver()
    print("Starting webserver")
    webprocess.start()
    print("webprocesss started")
    print("starting loop")
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print("Detected ctr+c, breaking...")
            break
    print("stopping webserver")
    webprocess.kill()
    print("webserver stopped")
    print("Bye!")
