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
        if data_pickled == None:
            return data_pickled
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
    

class Leaderboard:
    def __init__(self):
        self.db = Database("db/dbfiles/leaderboard.dbfile")
    def addscore(self, user, score):
        scoreobj = self.db.get(user)
        if scoreobj == None:
            scoreobj = {
                "name":user,
                "score":0
            }
        scoreobj["score"] += score
        self.db.put(user, scoreobj)
            

    def leaderboard(self):
        content = self.db.db_handle.retdb()
        
        keys = content.keys() #type:ignore
        leaderboard = []
        for key in keys:
            leaderboard.append(pickle.loads(content[key]))
        leaderboard.sort(key = self.sort, reverse=True)
        return leaderboard

    def sort(self, item):
        print(item)
        return item["score"]