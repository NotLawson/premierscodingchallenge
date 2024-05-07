## Users DB
import json, os, pickle
from ..helpers import Object, _internalDB

class TokenStore:
    tokens = []
    def __init__(self):
        pass
class User:
    tokens = []
    def __init__(self, tokenstore, username, password, permissions=0):
        self.username = username
        self.password = password
        self.permissions = permissions
        self.tokenstore = tokenstore
    def login(self, password):
        if password == self.password:
            return True
        else:
            return False
    def get_token(self):
        import random
        chars = ['a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E', 'f', 'F', 'g', 'G', 'h', 'H', 'i', 'I', 'j', 'J', 'k', 'K', 'l', 'L', 'm', 'M', 'n', 'N', 'o', 'O', 'p', 'P', 'q', 'Q', 'r', 'R', 's', 'S', 't', 'T', 'u', 'U', 'v', 'V', 'w', 'W', 'x', 'X', 'y', 'Y', 'z', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        while True:
            taken = False
            token=""
            i=0
            for i in range(20):
                token+=random.choice(chars)
                i+=1
            for i in self.tokenstore.tokens:
                if token==i.token:
                    taken = True
                    break
            if not taken:
                break
        self.tokenstore.tokens.append(Token(token,self.username))
        self.tokens.append(token)
        return token

class Token:
    def __init__(self, token, name):
        self.token = token
        self.user = name
    def __str__(self):
        return self.token

class db(_internalDB):
    pass