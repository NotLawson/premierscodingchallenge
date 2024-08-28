# Main Server file

## IMPORTS ##
from flask import Flask, request # For the webserver
import json # For data handling
import os # for good measure
import db
import helper



## Setup ##
if __name__=="__main__": # when running standalone DEVELOPMENT ONLY
    app = Flask(__name__)
    import log
    from log import level
    users = db.Database("db/dbfiles/users.dbfile")
    lessons = db.Database("db/dbfiles/lessons.dbfile")
    flash = db.Database("db/dbfiles/flashcards.dbfile")
    log = log.Logging()
else: # when running from the main server file
    from log import level
    from __main__ import app, log, users, lessons, flash # take from main file
log.log("API loaded")

## API ##
@app.route("/api/auth/token")
def get_token():
    # Creates a login token
    user = request.headers.get("x-api-user")
    password = request.headers.get("x-api-password")

    if user in users.refs(): # cheking if user valid
        userobj = users.get(user) # getting user object

        if userobj.password == password: # matching password
            token=helper.generate_token(user) # creating token
            log.log("Successful token request for "+user, level.done)
            return {
                "code":200,             #
                "message":"Success",    # sending token to client
                "token":token           #
            }                           # 
    log.log("Unsuccessful token request for "+user, level.warn)
    return {
        "code":401,
        "message":"Invalid Credentials",
        "credentials":[user, password]
    }, 401

@app.route("/api/auth")
def auth(request=request):
    # auth request, for pages that require login
    return helper.auth(request)

@app.route("/api/lessons/<path:endpoint>", methods = ["GET", "POST", "DELETE"])
def lessonsapi(endpoint):
    # api for Lessons
    path = endpoint.split("/")

    resp=helper.authw(request) # auth
    userobj = users.get(resp["user"]) # get user object

    if path[0]=="star": # star endpoint
        lessonid=path[1]
        userobj.starred_lessons.insert(0, lessonid) #inserts the starred lesson into starred list
        users.put(resp["user"], userobj)
        return {'code':200,'message':'done'}, 200
    
    elif path[0]=="unstar": # unstar endpoint
        lessonid=path[1]
        userobj.starred_lessons.remove(lessonid) # removes the lesson from the starred list
        users.put(resp["user"], userobj)
        return {'code':200,'message':'done'}, 200
    
    elif path[0] == "create": # create a lesson
        name = request.headers.get("name")
        desc = request.headers.get("desc")

        while True: # generate ID
            id = helper.generate_id()
            if id not in lessons.keys():
                break
        
        content = json.loads(request.data)["content"] # loads set data
        obj = db.lesson(id, name, resp["user"], desc, content) # create a lesson
        lessons.put(id, obj) # pushes to the database
        user = resp["user"]
        log.log(f"Lesson created for {user}, id: {id}, name: '{name}'", level.done)
        return {
            "code":200, 
            "message":"Created",
            "id":id
        }
    
    elif path[0] == "delete": # delete endpoint
        lessonid = path[1]

        owner = lessons.get(lessonid).author # get 
        if owner != resp["user"]:
            log.log(f"User {user} not authorised to delete {lessonid}", level.error)
            return {'code':400, 'message':'not authorised'}, 400
        
        lessons.remove(lessonid)
        log.log(f"Lesson {lessonid} successfully deleted by {resp['user']}", level.done)
        return {'code':200, 'message':'deleted'}
    else:
        log.log(f"Endpoint {[path]} not found", level.warn)
        return {'code':404, 'message':'endpoint not found'}, 404

@app.route("/api/sets/<path:endpoint>", methods = ["GET", "POST", "DELETE"])
def setsapi(endpoint):
    # api for sets
    path = endpoint.split("/")

    resp=helper.authw(request) # auth
    userobj = users.get(resp["user"]) # get user obj

    if path[0]=="star": # star endpoint
        setid=path[1]

        userobj.starred_sets.insert(0, setid) # add set to starred

        users.put(resp["user"], userobj) # push user obj

        return {'code':200,'message':'done'}, 200
    
    elif path[0]=="unstar": # unstar endpoint
        setid=path[1]

        userobj.starred_sets.remove(setid) # remove from starred

        users.put(resp["user"], userobj) # push user

        return {'code':200,'message':'done'}, 200
    
    elif path[0] == "create": # create sets endpoint
        name = request.headers.get("name")

        while True: # generate id
            id = helper.generate_id()
            if id not in flash.keys():
                break

        content = json.loads(request.data)["content"] # parse content

        obj = db.flash(id, name, resp["user"], content) # create sets obj
        flash.put(id, obj) # save to database

        return {
            "code":200, 
            "message":"Created",
            "id":id
        }
    
    elif path[0] == "delete": # delete endpoint
        setid = path[1]

        owner = flash.get(setid).author # get set owner
        user = resp['user'] # get current user

        if owner != resp["user"]:
            return {'code':400, 'message':'not authorised'}, 400
        
        flash.remove(setid) # delete
        return {'code':200, 'message':'deleted'}
    else:
        return {'code':404, 'message':'endpoint not found'}, 404


## Starting ##
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
