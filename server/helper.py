# Helper functions
def auth(request):
    token = request.headers.get("x-api-token")
    print(token)
    if token == None:
        token = request.cookies.get("token")
        print(token)
    valid = False
    for i in TOKENSTORE.tokens:
        if i.token == token:
            user = i.user
            return json.dumps({
            "code":200,
            "message":"Valid Token",
            "user":user
            }), 200
    return json.dumps({
        "code":401,
        "message":"Invalid Token"
    }), 401
def authw(request):
    resp, _ = auth(request)
    print(resp)
    return json.loads(resp)
import db, json
TOKENSTORE = db.user.TokenStore() # this start the tokenstore globally
