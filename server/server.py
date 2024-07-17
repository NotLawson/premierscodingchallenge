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
import helper



## Setup ##

load_dotenv() # Load env
if __name__=="__main__":
    app = Flask(__name__)
    import log
    from log import level

    log = log.Logging()
else:
    from log import level
    from __main__ import app, log

users = db.user.db()
notes = db.notes.db()
flash = db.flashcards.db()


## API ##
@app.route("/api/auth/token")
def get_token():
    user = request.headers.get("x-api-user")
    password = request.headers.get("x-api-password")
    log.log(f"is '{user} in {users.refs()}'")
    if user in users.refs():
        userobj = users.get(user)
        if userobj.password == password:
            token=helper.generate_token(user)
            return json.dumps({"code":200,
                    "message":"Success",
                    "token":token})
    return json.dumps({
        'code':401,
        "message":"Invalid Credentials",
        "credentials":[user, password]
    }), 401
        

@app.route("/api/auth")
def auth(request=request):
    return helper.auth(request)

@app.route("/api/usercreate/<username>/<password>/")
def usercreate(username, password):
    if username in users.refs():
        return json.dumps({"code":500, "message":"user already exists"}), 500
    user = db.user.User(username, password)
    users.put(username, user)
    users.push()
    return json.dumps({"code":200, "message":"user added"})

@app.route("/api/sets/<endpoint>", methods = ["GET", "POST", "DELETE"])
def setsapi(endpoint):
    path = endpoint.split("/")
    resp=helper.authw(request)
    userobj = users.get(resp["user"])
    if path[0]=="star":
        setid=path[1]
        userobj.starred.append("setid")
        users.put(resp["user"], userobj)
        return "{'code':200,'message':'done'}", 200
    
    elif path[0] == "create":
        name = request.headers.get("name")
        while True:
            id = helper.generate_id()
            if id not in flash.refs():
                break
        content = json.loads(request.data)["content"]
        obj = db.flashcards.flash(id, name, userobj.name, content)
        flash.put(id, obj)
        return {
            "code":200, 
            "message":"Created",
            "id":id
        }
    else:
        return "{'code':404, 'message':'endpoint not found'}", 404

@app.route("/api/db/<db_name>/<action>")
def db_api(db_name, action):
    if db_name=="users":
        if action=="push":
            log.log(f"Received database push order for {db_name}", level.warn, name = f"Server (/api/db/{db_name}/{action})")
            users.push()
            return json.dumps({"code":200,
                               "message":"Pushed users db"})
        elif action=="pull":
            log.log(f"Received database pull order for {db_name}", level.warn, name = f"Server (/api/db/{db_name}/{action})")
            users.pull()
            return json.dumps({"code":200,
                               "message":"Pulled users db"})
        elif action=="refs":
            log.log(f"Received database refs order for {db_name}", level.warn, name = f"Server (/api/db/{db_name}/{action})")
            return json.dumps({"code":200,
                               "message":"found users refs",
                               "refs":users.refs()})
    elif db_name=="flash":
        if action=="push":
            log.log(f"Received database push order for {db_name}", level.warn, name = f"Server (/api/db/{db_name}/{action})")
            flash.push()
            return json.dumps({"code":200,
                               "message":"Pushed flash db"})
        elif action=="pull":
            log.log(f"Received database pull order for {db_name}", level.warn, name = f"Server (/api/db/{db_name}/{action})")
            flash.pull()
            return json.dumps({"code":200,
                               "message":"Pulled flash db"})
        elif action=="refs":
            log.log(f"Received database refs order for {db_name}", level.warn, name = f"Server (/api/db/{db_name}/{action})")
            return json.dumps({"code":200,
                               "message":"found flash refs",
                               "refs":flash.refs()})
    elif db_name=="notes":
        if action=="push":
            notes.push()
            return json.dumps({"code":200,
                               "message":"Pushed notes db"})
        elif action=="pull":
            notes.pull()
            return json.dumps({"code":200,
                               "message":"Pushed users db"})
    return json.dumps({"code":404,
                               "message":"No db found"}), 404

## Starting ##
if __name__ == "__main__":
    DEBUG = bool(env("DEBUG"))
    app.run(host=env("host"), port=env("port"), debug=DEBUG)
