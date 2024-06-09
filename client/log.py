### BetterLog ###
## IMPORTS ##
import time
from datetime import datetime # for time

# create log file
try:
    open("log.txt", "r")
except:
    open("log.txt", "x")

## COLOURS DEFINE ##
class colours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

## ERROR CLASS ##
# for people who use VSCode auto complete lol
class level:
    done = "DONE"
    warn = "WARNING"
    info = "INFO"
    error = "ERROR"
    fail = "FAIL"
    exit = "EXIT"
    debug = "DEBUG"

class Logging:
    def __init__(self, name="app", loglevel = level.info):
        self.name = name
        self.logginglevel = loglevel

        ## UNFINISHED/NOT IMPLEMENTED ##
        '''
        from threading import Thread
        q = "Q"
        self.thread = Thread(self.logthread(q), daemon=True)
        '''
    ## LOG ##
    def log(self, message, msg_error=level.info, name=None):
        if name == None:
            name = self.name
        message_state = ["",""]
        message_state[0] = str(datetime.now().strftime('%H:%M:%S'))
        message_state[1] = message

        if msg_error=="DONE":
            colour = colours.OKGREEN
        elif msg_error=="WARNING" or msg_error=="DEBUG":
            colour = colours.WARNING
        elif msg_error=="INFO":
            colour = colours.OKCYAN
        elif msg_error=="ERROR" or msg_error=="FAIL" or msg_error=="EXIT":
            colour = colours.FAIL
        
        message_structure=message_state[0]+" -- "+"("+colour+msg_error+colours.ENDC+") ["+name+"] "+colour+message_state[1]+colours.ENDC
        
        if self.logginglevel == level.warn:
            if (msg_error == level.warn or
                msg_error == level.error or 
                msg_error == level.exit or 
                msg_error == level.fail):
                print(message_structure)
                message_structure=message_state[0]+" -- "+"("+msg_error+") "+") ["+name+"] "+message_state[1]
                mod=open("log.txt","a")
                mod.write(message_structure+"\n")
            pass
        elif self.logginglevel == level.error:
            if (msg_error == level.error or 
                msg_error == level.exit or 
                msg_error == level.fail):
                print(message_structure)
                message_structure=message_state[0]+" -- "+"("+msg_error+") "+") ["+name+"] "+message_state[1]
                mod=open("log.txt","a")
                mod.write(message_structure+"\n")
        elif self.logginglevel == level.debug:
            print(message_structure)
            message_structure=message_state[0]+" -- "+"("+msg_error+") "+") ["+name+"] "+message_state[1]
            mod=open("log.txt","a")
            mod.write(message_structure+"\n")
        else: # All levels
            if msg_error == level.debug:
                pass
            else:
                print(message_structure)
                message_structure=message_state[0]+" -- "+"("+msg_error+") ["+name+"] "+message_state[1]
                mod=open("log.txt","a")
                mod.write(message_structure+"\n")

    ## ASK ##
    def ask(self, message, name=None):
        if name == None:
            name = self.name
        message_state = ["",""]
        msg_error = "INPUT"
        colour = colours.OKBLUE
        message_state[0] = str(datetime.now().strftime('%H:%M:%S'))
        message_state[1] = message
        message_structure=message_state[0]+" -- "+"("+colour+msg_error+colours.ENDC+") "+") ["+name+"] "+colour+message_state[1]+colours.ENDC+"\n"
        answer = input(message_structure)
        message_structure=message_state[0]+" -- "+"("+msg_error+") ["+name+"] "+message_state[1]+"\n"
        mod=open("log.txt","a")
        mod.write(message_structure+answer+"\n")
        mod.close()
        return answer
    
    def logthread(q):
        pass