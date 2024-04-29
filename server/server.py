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
import pymongo as mongo


## Setup ##
load_dotenv() # Load env
app = Flask(__name__)

class db:
    def __init__(self, db_name, collection_name):
        self.client = mongo.MongoClient(f"mongodb://{env("mongoaddr")}:27017/")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

## API ##
@app.route("/api/userdata/<endpoint>", methods=["GET", "POST", "DELETE"])
def userdata_endpoint(endpoint):
    method = request.method
    data = db("userdata", "user")
    return {"code":200,
            "message":"Basic Userdata endpoint"}

## Starting ##
if __name__ == "__main__":
    DEBUG = bool(env("DEBUG"))
    app.run(host=env("host"), port=env("port"), debug=DEBUG)