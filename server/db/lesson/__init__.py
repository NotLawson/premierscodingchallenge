## Lessons DB

import json, pickle, os
from ..helpers import _internalDB, Object
class db(_internalDB):
    def __init__(self):
        super().__init__(os.path.dirname(__file__)+"/dbfile")

class lesson:
    def __init__(self, id, name, author, desc, content):
        self.id = id
        self.name = name
        self.author = author
        self.content = content
        self.desc = desc
        self.total = len(content)

    