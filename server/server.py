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
env=getenv
#import pymongo as mongo
import db

## Setup ##
load_dotenv() # Load env
app = Flask(__name__)

## API ##
@app.route("/api/auth")
def auth(request=request):
    return True # Figure it out later

@app.route("/api/userdata/<endpoint>", methods=["GET", "POST", "DELETE"])
def userdata_endpoint(endpoint):
    method = request.method
    name = auth(request)
    if name == False:
        response = {
            "code":401,
            "message":"Not logged it"
        }
        return response
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

