## Users DB
import json, os, pickle
from ..helpers import Object, _internalDB

class TokenStore:
    tokens = []
    def __init__(self):
        pass
class User:
    tokens = []
    def __init__(self, name, password, permissions=0):
        self.name = name
        self.password = password
        self.permissions = permissions
    def login(self, password):
        if password == self.password:
            return True
        else:
            return False
    def get_token(self, token):
        self.tokens.append(token)

class Token:
    def __init__(self, token, name):
        self.token = token
        self.user = name
    def __str__(self):
        return self.token

class db(_internalDB):
    def __init__(self):
        super().__init__(os.path.dirname(__file__)+"/dbfile")