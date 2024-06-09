### ELECTRONIC FLASHCARDS AND SUMMARIES APPLICATION ###
### BY MINAS MARENTIS AND LAWSON CONALLIN, 2024 ###
### FOR PARTIAL REQUIREMENTS FOR DIGITAL TECHNOLOGY GRADE
### AND PREMIERS CODING CHALLENGE YEAR 2024 ###

### WEB SUMMARIES SORUCED FROM M-M BASIC [VERSION 1.15] ###
### BY MINAS MARENTIS 2022 , 2023 , 2024 ###

### [VERSION 1.01] APPLICATION BETA STAGE ###

import tkinter as tk
from tkinter import messagebox, filedialog, END, Scrollbar, Toplevel
import os
import pyttsx3
import wikipedia
import textwrap
from threading import Thread

class task:
    def __init__(self, task):
        '''
        How to use:
        create a task: helloworld = task(lambda: print("Hello World!"))
        run the task: helloworld.start() OR helloworld()
        It then runs in the background to stop tkinter from freezing'''
        self.func = task
        

    def __call__(self):
        self.thread = Thread(target=self.func, daemon=True)
        self.thread.start()
    
    def start(self):
        self.__call__()

class TkEngine:
    def __init__(self, root, framerate):
        '''
        This was supposed to run tkinter without blocking the main thread by running it in a seperate thread, but that isn't working
        How to use:
        create the engine: engine = TkEngine(root, framerate)
        start the engine: engine.start()
        '''
        self.root = root
        self.framerate = framerate
        self.wait = 1000 / framerate

    def start(self):
        self.thread = Thread(target=self.loop, daemon=True)
        
    def loop(self):
        while True:
            self.tick()
            root.update()

    def tick(self):
        from time import sleep
        sleep(self.wait / 1000)

class KeybindManager:
    binds = {}
    def __init__(self, object):
        self.object = object
        self.object.bind("<Key>", self.handle)

    def bind(self, keycode, task):
        try:
            if self.binds[keycode] != None:
                raise KeybindTaken(f"The keybind {keycode} has already been taken")
        except:
            self.binds[keycode] = task
            
        
        
    def handle(self, event):
        try: self.binds[event.keysym]()
        except:
            pass

class KeybindTaken(Exception):
    pass

def save_as_flashcards():
    pass

def save_flashcards():
    pass

def flashcards_search():
    root.after(1, submit_flashcards)

def submit_flashcards():
    try:
        output_text.delete(1.0, END)
        output_text.insert(END, "Searching..." + "\n")
        topic = input_entry1.get()
        lines = input_entry2.get()

        width = 50
        import wiki_wrapper as wiki
        result = wiki.wiki(topic, lines)


        wrapped_summary = textwrap.wrap(result, width=width)


        output_text.delete(1.0, END)

        for line in wrapped_summary:
            output_text.insert(END, line + '\n')

    except Exception as e:
        error1 = messagebox.showinfo("ERROR:", e)
        

def print_flashcards():
    pass

def dictate_flashcards():
    try:
        topic = input_entry1.get()
        lines = input_entry2.get()

        width = 50
        import wiki_wrapper as wiki
        result = wiki.wiki(topic, lines)

        wrapped_summary = textwrap.wrap(result, width=width)

        engine = pyttsx3.init()
        voice_num = 1
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[voice_num].id)

        text = f'{result}'
        engine.say(text)
        engine.runAndWait()

    except Exception as e:
        error2 = messagebox.showinfo("ERROR:", e)

def clear_output():
    output_text.delete(1.0, END)

def about():
    about_window = Toplevel(root)
    about_window.title("About Study Flashcard Generator")
    about_window.geometry("300x200")
    about_window.resizable(False, False)

    about_label = tk.Label(about_window, text="Study Flashcard And Internet Summaries Generator\n\nCreated By\nMinas Marentis and Lawson Conallin\n\n[VERSION 1.01]")
    about_label.pack(pady=20)

    close_button = tk.Button(about_window, text="Close", command=about_window.destroy)
    close_button.pack(pady=6)

def user_guide():
    pass    

def exit_application():
    exit()

def main_loop():
    while True:
        pass

root = tk.Tk()
root.title("Study Flashcard Generator")
root.geometry("600x450")
root.resizable(False, False)

### THIS IS THE TEXT OUTPUT FRAME WIDGET ###

output_frame = tk.Frame(root)
output_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

### SCROLLING SIDE BAR FUNCTION ###

scrollingbar = Scrollbar(output_frame)
scrollingbar.pack(side=tk.RIGHT, fill=tk.Y)

output_text = tk.Text(output_frame, height=20, width=60, yscrollcommand=scrollingbar.set)
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollingbar.config(command=output_text.yview)

button_frame = tk.Frame(root)
button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

### BUTTON CREATION ###

submit_button = tk.Button(button_frame, text="Submit", command=task(submit_flashcards)) # This button gets information from wikipedia or another source (if we implement)
dictate_button = tk.Button(button_frame, text="Dictate", command=task(dictate_flashcards)) # not sure

dictate_button.grid(row=0, column=0, pady=5, sticky="ew")

### UTILITY MENU CREATION ###

main_menu = tk.Menu()

file_menu = tk.Menu(main_menu,tearoff=False)
help_menu = tk.Menu(main_menu,tearoff=False)

main_menu.add_cascade(label="File",menu=file_menu)
main_menu.add_cascade(label="Help",menu=help_menu)

file_menu.add_command(label="New", compound=tk.LEFT, accelerator="Ctrl+N", command=task(clear_output))
file_menu.add_command(label="Save", compound=tk.LEFT, accelerator="Ctrl+S", command=task(save_flashcards))
file_menu.add_command(label="Save As", compound=tk.LEFT, accelerator="Ctrl+Shift+S", command=task(save_as_flashcards))
file_menu.add_command(label="Print", compound=tk.LEFT, accelerator="Ctrl+P", command=task(print_flashcards))
file_menu.add_separator()
file_menu.add_command(label="Exit", compound=tk.LEFT, accelerator="Alt+F4", command=task(exit_application))

help_menu.add_command(label="About", compound=tk.LEFT, command=about)
help_menu.add_command(label="Quick Guide", compound=tk.LEFT, accelerator="Ctrl+H", command=task(user_guide))

### OUTPUT AND INPUT DISPLAY BOXES ###

input_frame = tk.Frame(root)
input_frame.grid(row=1, column=0, columnspan=2, padx=15, pady=15, sticky="ew")

input_label1 = tk.Label(input_frame, text="Topic:")
input_label1.grid(row=0, column=0, padx=(0, 5))

input_entry1 = tk.Entry(input_frame, width=30)
input_entry1.grid(row=0, column=1)

input_label2 = tk.Label(input_frame, text="Sentences Desired:")
input_label2.grid(row=1, column=0, padx=(0, 5))

input_entry2 = tk.Entry(input_frame, width=30)
input_entry2.grid(row=1, column=1)

submit_button_box = tk.Button(input_frame, text="Submit", command=task(submit_flashcards))
submit_button_box.grid(row=0, column=2, padx=(5, 0))

root.config(menu=main_menu)

### KEYBINDS ###
keybind = KeybindManager(root)
keybind.bind("Return", task(submit_flashcards))


### MAIN LOOP ###
'''framerate = 60

engine = TkEngine(root, framerate)
engine.start()
'''

mainloop = task(main_loop)
print("starting main loop")
mainloop()
print("starting tkinter")
root.mainloop()
