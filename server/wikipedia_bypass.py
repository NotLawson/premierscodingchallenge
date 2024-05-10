## Used to bypass the wikipedia block at school
## parameters are sent using flask, and the response from the server is pickled before returning/or if not an object just returned normally
## This is the server side, will be used in the main server file

from flask import Flask, request
import json
import wikipedia

app = Flask(__name__)

@app.route("/wikipedia_bypass")
def wikibypass():
    topic = request.headers["topic"]
    lines = int(request.headers["lines"])
    try:
        summary = wikipedia.summary(topic, sentences = lines)
        return json.dumps({"code":200,"message":f"Topic '{topic}' found", "content":summary})
    except wikipedia.DisambiguationError as e:
        return json.dumps({"code":500, "message":f"The term {topic} can refer to many things. See error for list", "error":e})
    except wikipedia.PageError as e:
        return json.dumps({"code":500, "message":f"The term {topic} was not found. See error for list", "error":e})
    
if __name__=="__main__":
    app.run("0.0.0.0", 5000, debug=True) ## If running by itself