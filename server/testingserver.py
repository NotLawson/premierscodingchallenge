from flask import render_template, Flask, make_response, request, redirect
import random

app = Flask(__name__)

class setobj:
    name="Testing Set"
    content=[
        ["multi-4", "Question 1", ["Answer Correct", "Answer Incorrect", "Answer Incorrect", "Answer Incorrect",]],
        ["multi-4", "Question 2", ["Answer Correct", "Answer Incorrect", "Answer Incorrect", "Answer Incorrect",]],
        ["multi-4","Question 3", ["Answer Correct", "Answer Incorrect", "Answer Incorrect", "Answer Incorrect",]],
        ["multi-4", "Question 4", ["Answer Correct", "Answer Incorrect", "Answer Incorrect", "Answer Incorrect",]]
        # Question       Correct Answer    Incorrect Answers
    ]
    total = len(content)


i = -1
@app.route("/player")
def main():
    progress = int(request.cookies.get("question"))
    setid = request.cookies.get("setid")
    try: 
        question = setobj.content[progress-1]
    except IndexError:
        return "Finished!"
    return render_template("player.html", set=setobj, progress=progress-1,progressjs = progress, question=question, int=int)

@app.route("/setup")
def setup():
    resp = make_response(redirect("/player"))
    resp.set_cookie("question", "1")
    return resp

app.run(port=5001)