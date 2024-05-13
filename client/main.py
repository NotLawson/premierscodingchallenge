## Main client file ##
## This will be built into an exe ##
##
## The app will be tkinter app with that can take wikipedia results 

from tkinter import Tk, Label, Button, Entry
#import tensorflow as tf

from wikipedia_bypass import wiki

tk = Tk(screenName="Flashcards")

tk.title("Flashcards")

# Widget Functions
def submit():
    message = widgets["input"].get()
    widgets["output"].configure(text=message)
    pass



## Widgets
widgets = {
    "output":Label(tk, text="Hi connor", ),
    "input":Entry(tk),
    "submit":Button(tk, text="Submit", command = submit),

}
for widget in widgets.keys():
    widgets[widget].pack()
    
tk.mainloop()