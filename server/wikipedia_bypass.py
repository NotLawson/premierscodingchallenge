## Used to bypass the wikipedia block at school
## parameters are sent using flask, and the response from the server is pickled before returning/or if not an object just returned normally
## This is the server side, will be used in the main server file

## NOTE: This isn't being used anymore, but this file is still part of the program to help out a friend of mine

from flask import Flask, request
import json
import wikipedia

if __name__=="__main__":
    app = Flask(__name__)
    import log
    from log import level

    log = log.Logging()
else:
    from log import level
    from __main__ import app, log

@app.route("/wikipedia_bypass")
def wikibypass():
    topic = request.headers["topic"]
    try: lines = int(request.headers["lines"])
    except: lines = 10
    try:
        summary = wikipedia.summary(topic, sentences = lines)
        return json.dumps({"code":200,"message":f"Topic '{topic}' found", "content":summary})
    except wikipedia.DisambiguationError as e:
        return json.dumps({"code":500, "message":f"The term {topic} can refer to many things. See error for list", "error":e})
    except wikipedia.PageError as e:
        return json.dumps({"code":500, "message":f"The term {topic} was not found. See error for list", "error":e})
    
if __name__=="__main__":
    app.run("0.0.0.0", 5000, debug=True) ## If running by itself