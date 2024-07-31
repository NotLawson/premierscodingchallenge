## Users DB
import json, os, pickle

class TokenStore:
    tokens = []
    def __init__(self):
        pass
class User:
    tokens = []
    starred = []
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

class flash:
    def __init__(self, id, name, author, content=[]):
        self.id = id
        self.name = name
        self.author = author
        self.content = content
        self.total = len(content)

class lesson:
    def __init__(self, id, name, author, desc, content):
        self.id = id
        self.name = name
        self.author = author
        self.content = content
        self.desc = desc
        self.total = len(content)