## Users DB
import json, os, pickle
from ..helpers import Object, _internalDB
class User(Object):
    def __init__(self, username, permissions, uuid=None, password=None):
        super().__init__(username,"user")
        permissions = permissions
        if not uuid == None:
            # TODO
            self.uuid = "uuid"
        self.password_overide = password

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
        