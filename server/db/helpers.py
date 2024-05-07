# Helpers

import os, pickle

## Object
class Object:
    def __init__(self, name, data):
        self.name = name
        self.data = data

## DB
class NoObjFound(Exception):
    pass

class _internalDB:
    def __init__(self, dbPath, nosync = False):
        self.dbPath = dbPath
        if not nosync:
            self.pull()

    def get(self, ref):
        try: obj = self.db_dict['db'][ref]
        except:
            raise NoObjFound
        return obj
    
    def put(self, ref, data):
        self.db_dict['db'][ref] = data
        self.push()

    def refs(self):
        ref = list(self.db_dict["db"].keys())
        return ref
    
    def remove(self, ref):
        del self.db_dict["db"][ref]

    def pull(self):
        try: self.db_dict = pickle.load(open(self.dbPath, "rb"))
        except:
            open(self.dbPath, "x")
            self.db_dict = {"db":{}}
            self.push()

    def push(self):
        try: pickle.dump(self.db_dict, open(self.dbPath, "wb"))
        except:
            open(self.dbPath, "x")
            pickle.dump(self.db_dict, open(self.dbPath, "wb"))