# Main Server file
# Server/
#   - api/
#       - userdata/
#          - flashcards AUTH -
#              - GET: Gets flashcards for a user
#              - POST: Updates flashcards for a user
#              - DELETE: Deletes flashcard set for a user
#          - notes AUTH -
#              - GET Gets notes
#              - POST: Adds notes
#              - DELETE: Deletes notes sets


## IMPORTS ##
from flask import Flask, request # For the webserver
import json # For data handling
from dotenv import load_dotenv # For .env
from os import getenv # For using .env
import os # for good measure
env=getenv
import random # For token generation
import db


## Setup ##
TOKENSTORE = db.user.TokenStore()

load_dotenv() # Load env
app = Flask(__name__) 

users = db.user.db(os.path.dirname(db.user.__file__)+"/dbfile")
notes = db.notes.db(os.path.dirname(db.notes.__file__)+"/dbfile")
flash = db.flashcards.db(os.path.dirname(db.flashcards.__file__)+"/dbfile")


## API ##
@app.route("/api/auth/token")
def get_token():
    user = request.headers.get("x-api-user")
    password = request.headers.get("x-api-password")
    if user in users.refs():
        userobj = users.get(user)
        if userobj.login(password):
            token=user.get_token()
            return json.dumps({"code":200,
                    "message":"Success",
                    "token":token})
    return json.dumps({
        'code':401,
        "message":"Invalid Credentials"
    })
        

@app.route("/api/auth")
def auth(request=request):
    token = request.headers.get("x-api-token")
    valid = False
    for i in TOKENSTORE.tokens:
        if i.token == token:
            user = i.user
            return json.dumps({
            "code":200,
            "message":"Valid Token",
            "user":user
            })
    return json.dumps({
        "code":401,
        "message":"Invalid Token"
    })
@app.route("/api/usercreate/<username>/<password>/")
def usercreate(username, password):
    user = db.user.User(TOKENSTORE, username, password)
    if username in users.refs():
        return json.dumps({"code":500, "message":"user already exists"})

    users.put(username, user)
    return json.dumps({"code":200, "message":"user added"})



@app.route("/api/userdata/<endpoint>", methods=["GET", "POST", "DELETE"])
def userdata_endpoint(endpoint):
    method = request.method
    data = db("userdata", "user")
    authenticate = auth(request)
    if authenticate["code"] == 401:
        response = {
            "code":401,
            "message":"Not logged in"
        }
        return response
    name = authenticate["user"]
    if endpoint == "flashcards":
        # FLASH CARDS
        if method == "GET":
            # GET
            pass

        elif method == "POST":
            # POST
            pass

        elif method == "DELETE":
            # DELETE
            pass
        # Compile response
        response = {}


    elif endpoint == "notes":
        # Notes
        if method == "GET":
            # GET
            pass

        elif method == "POST":
            # POST
            pass

        elif method == "DELETE":
            # DELETE
            pass
        # Compile response
        response = {}
    return response

## Starting ##
if __name__ == "__main__":
    DEBUG = bool(env("DEBUG"))
    app.run(host=env("host"), port=env("port"), debug=DEBUG)