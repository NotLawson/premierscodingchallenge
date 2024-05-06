## Flashcards DB
import json, pickle, os
from ..helpers import _internalDB, Object
class db(_internalDB):
    def __init__(self, nosync=False):
        if nosync:
            pass
        else:
            module_path = os.path.dirname(__file__)
            self.db_dict = pickle.load(open(module_path+"/dbfile", "rb"))
    def pull(self):
        module_path = os.path.dirname(__file__)
        self.db_dict = pickle.load(open(module_path+"/dbfile", "rb"))

    def push(self):
        module_path = os.path.dirname(__file__)
        pickle.dump(self.db_dict, open(module_path+"/dbfile", "wb"))