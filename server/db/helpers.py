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
    def __init__(self):
        self.db_dict = {
            "db":{
                "ref1":Object("ref1", "Data"),
                "ref2":Object("ref2","Data")
            }
        }

    def get(self, ref):
        try: obj = self.db_dict['db'][ref]
        except:
            raise NoObjFound
        return obj
    def put(self, ref, data):
        self.db_dict['db'][ref] = data
    def refs(self):
        ref = list(self.db_dict["db"].keys())
        return ref