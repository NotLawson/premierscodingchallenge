## Main client file ##
## This will be built into an exe ##
##
## The app will be tkinter app with that can take wikipedia results 

from tkinter import Tk, Label, Button, Entry, Text, END
from asyncio import run as arun
#import tensorflow as tf

from client.wiki_wrapper import wiki

tk = Tk(screenName="Flashcards")

tk.title("Flashcards")

# Widget Functions
def submit():
    search = widgets["input"].get()
    widgets["output"].insert(END, f"Loading results for {search}...\n")
    arun(submitcoro())
async def submitcoro():
    message = widgets["input"].get()
    resp = wiki(message)
    widgets["output"].insert(END, resp)



## Widgets
widgets = {
    "output":Text(tk,),
    "input":Entry(tk),
    "submit":Button(tk, text="Submit", command = submit),

}
for widget in widgets.keys():
    widgets[widget].pack()
    
tk.mainloop()