## Just a wrapper for elara, the database I'm using
from .helpers import *
import elara, pickle

class Database:
    def __init__(self, path, key=None, commit=True):
        if key==None:
            self.db_handle = elara.exe(path, commit)
        else: self.db_handle = elara.exe_secure(path, commit, key)

    def put(self, key, data):
        '''
        Puts an object with key
        '''
        data_pickled = pickle.dumps(data)
        self.db_handle.set(key, data_pickled)

    def get(self, key):
        '''
        Gets an object by key
        '''
        data_pickled = self.db_handle.get(key)
        data = pickle.loads(data_pickled)
        return data
    
    def remove(self, key):
        '''
        Removes and object with key
        '''
        self.db_handle.rem(key)

    def keys(self):
        '''
        Returns a list of keys
        '''
        keys_list = self.db_handle.getkeys()
        return keys_list
    

