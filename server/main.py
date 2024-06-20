## This is the main file to run to start all needed processes

## First of all, messaging
from multiprocessing import Queue
from log import Logging, level # custom logging library
import flask, os
app = flask.Flask(__name__) # for the webserver making thing
log = Logging()


    

apiq = Queue() # input Queue for the api server
wappq = Queue() # input Queue for the web app server
events = Queue() # For general server events like restart, shutdown, so on so forth

class event:
    def __init__(self, name, origin, data):
        self.name = name
        self.origin = origin
        self.data = data
    def __str__(self):
        return self.name

@app.route("/restart")
def restart():
    # Doesn't work atm
    events.put(event("restart", "/restart", None))
    return "restarting now!"

def startupwebserver():
    global app
    from threading import Thread
    import wapp, server, wikipedia_bypass
    return Thread(target=startupwebserverprocess, name="webserver", daemon=True)
def startupwebserverprocess():
    global app
    app.run(host="0.0.0.0",port=5000,debug=False)

    

if __name__ == "__main__":
    import sys, time
    webprocess = startupwebserver()
    log.log("Starting webserver")
    webprocess.start()
    log.log("webprocesss started", level.done)
    log.log("starting loop")
    while True:
        try:
            current = events.get(block=False)
            if current.name == "restart":
                log.log(f"Restarting comming from {current.origin}", level.warn)
                os.execv(sys.argv[0], sys.argv)
                exit()
        except KeyboardInterrupt:
            log.log("Detected ctr+c, breaking...",level.warn)
            break
        except:
            pass
    log.log("Bye!",level.exit)
