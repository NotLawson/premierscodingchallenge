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

def generate_token(username):
    import random
    chars = ['a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E', 'f', 'F', 'g', 'G', 'h', 'H', 'i', 'I', 'j',
             'J', 'k', 'K', 'l', 'L', 'm', 'M', 'n', 'N', 'o', 'O', 'p', 'P', 'q', 'Q', 'r', 'R', 's', 'S', 't', 'T',
             'u', 'U', 'v', 'V', 'w', 'W', 'x', 'X', 'y', 'Y', 'z', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    while True:
            taken = False
            token=""
            i=0
            for i in range(20):
                token+=random.choice(chars)
                i+=1
            for i in TOKENSTORE.tokens:
                if token==i.token:
                    taken = True
                    break
            if not taken:
                break
    TOKENSTORE.tokens.append(db.Token(token,username))
    return token
def generate_id():
    import random
    chars = ['a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E', 'f', 'F', 'g', 'G', 'h', 'H', 'i', 'I', 'j',
             'J', 'k', 'K', 'l', 'L', 'm', 'M', 'n', 'N', 'o', 'O', 'p', 'P', 'q', 'Q', 'r', 'R', 's', 'S', 't', 'T',
             'u', 'U', 'v', 'V', 'w', 'W', 'x', 'X', 'y', 'Y', 'z', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    token = ""
    i = 0
    
    for i in range(20):
        token+=random.choice(chars)
        i+=1
    return token
    
class Suggestion:
    def __init__(self, title, link, desc):
        self.title = title
        self.link = link
        self.desc = desc

import db, json
TOKENSTORE = db.TokenStore() # this start the tokenstore globally
