## Flashcards DB
import json, pickle, os
from ..helpers import _internalDB, Object
class db(_internalDB):
    def __init__(self):
        super().__init__(os.path.dirname(__file__)+"/dbfile")

class flash:
    def __init__(self, id, name, author, content={}):
        self.id = id
        self.name = name
        self.author = author
        self.content = content
        self.html = f"<h3>Empty for {name}</h3>"