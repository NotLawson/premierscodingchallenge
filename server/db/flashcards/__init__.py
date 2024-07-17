## Flashcards DB
import json, pickle, os
from ..helpers import _internalDB, Object
class db(_internalDB):
    def __init__(self):
        super().__init__(os.path.dirname(__file__)+"/dbfile")

class flash:
    def __init__(self, id, name, author, content=[]):
        self.id = id
        self.name = name
        self.author = author
        self.content = content
        self.total = len(content)
        self.html = f"<h3>Empty for {name}</h3>"

class setobj:
    name="Testing Set"
    content=[
        ["multi-4", "Question 1", ["Answer Correct", "Answer Incorrect", "Answer Incorrect", "Answer Incorrect",]],
        ["multi-4", "Question 2", ["Answer Correct", "Answer Incorrect", "Answer Incorrect", "Answer Incorrect",]],
        ["multi-4","Question 3", ["Answer Correct", "Answer Incorrect", "Answer Incorrect", "Answer Incorrect",]],
        ["multi-4", "Question 4", ["Answer Correct", "Answer Incorrect", "Answer Incorrect", "Answer Incorrect",]]
        # Question       Correct Answer    Incorrect Answers
    ]
    total = len(content)