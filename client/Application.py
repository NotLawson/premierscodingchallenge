### ELECTRONIC FLASHCARDS AND SUMMARIES APPLICATION ###
### BY MINAS MARENTIS AND LAWSON CONALLIN, 2024 ###
### FOR PARTIAL REQUIREMENTS FOR DIGITAL TECHNOLOGY GRADE
### AND PREMIERS CODING CHALLENGE YEAR 2024 ###

### WEB SUMMARIES SOURCED FROM M-M BASIC [VERSION 1.15] ###
### BY MINAS MARENTIS 2022 , 2023 , 2024 ###

### LOGGING SOURCED FROM https://github.com/notlawson/betterlog-python ###
## BY LAWSON CONALLIN ###

### [VERSION 1.01] APPLICATION BETA STAGE ###

import tkinter as tk
from tkinter import messagebox, filedialog, END, Scrollbar, Toplevel
import os, time
import pyttsx3
import textwrap
from threading import Thread
from log import Logging, level
import wiki_wrapper as wiki
import progressbar as taskbar

log = Logging("app", loglevel=level.debug)
class task:
    def __init__(self, task):
        '''
        How to use:
        create a task: helloworld = task(lambda: print("Hello World!"))
        run the task: helloworld.start() OR helloworld()
        It then runs in the background to stop tkinter from freezing'''
        self.func = task
        self.name = task.__name__
        self.widgets = [
            f"time -- (TASK) [{self.name}] Running for ", taskbar.Timer("%s"), "s ", taskbar.AnimatedMarker()
        ]
        self.thread = Thread(target=self.func, daemon=True)
        
        

    def __call__(self):
        #Thread(target=self._start, daemon=True).start()
        self.thread.start()
    
    def start(self):
        self.__call__()

    def _start(self):
        starttime = time.perf_counter()
        bar = taskbar.ProgressBar(max_value=1, widgets=self.widgets, redirect_stdout=True).start()
        while self.thread.is_alive():
            bar.update(0)
        bar.update(1)
        out = f"\rtime -- (DONE) [{self.name}] Finished in {bar.start_time}      "
        print(out)

    def start_ignore(self):
        self.thread.start()

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
    name = "save as"
    path = filedialog.asksaveasfilename(defaultextension=".flashcards", title="flashcards.txt")
    log.log(f"Got path {path}", level.debug, name)
    try: 
        log.log("Trying to create file", name=name)
        open(path, "x")
        log.log("File created", level.done, name)
    except:
        log.log("file already exists", level.warn, name)
    try:
        log.log("Writing to file...", name=name)   
        open(path, "w").write(str(output_text.dump("1.0", "end")))
        log.log("Finished writing to file", level.done, name)
    except Exception as e:
        log.log(f"Failed to save file {path}, error: {e}", level.fail, name)


def save_flashcards():
    pass

def flashcards_search():
    root.after(1, submit_flashcards)

def submit_flashcards():
    name = "search"
    try:
        log.log("starting search", name=name)
        output_text.delete(1.0, END)
        output_text.insert(END, "Searching..." + "\n")
        topic = input_entry1.get()
        lines = input_entry2.get()

        width = 50
        log.log(f"searching for {topic}", name=name)
        result = wiki.wiki(topic, lines)
        log.log("Finsished.", level.done, name)

        log.log("Wrapping", name=name)
        wrapped_summary = textwrap.wrap(result, width=width)


        output_text.delete(1.0, END)

        log.log("inserting search")
        for line in wrapped_summary:
            output_text.insert(END, line + '\n')
        log.log("Done", level.done, name)

    except Exception as e:
        error1 = messagebox.showinfo("ERROR:", e)
        log.log(f"Error encountered while searching: {e}", level.error, name)
        

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
    log.log("Exiting, goodbye!", level.exit)
    exit()

def main_loop():
    name = "mainloop"
    log.log("mainloop started", level.done, name)
    while True:
        pass

log.log("Init Tkinter")
root = tk.Tk()
root.title("Study Flashcard Generator")
root.geometry("600x450")
root.resizable(False, False)

### THIS IS THE TEXT OUTPUT FRAME WIDGET ###

log.log("packing output frame")
output_frame = tk.Frame(root)
output_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

### SCROLLING SIDE BAR FUNCTION ###

log.log("packing scrollbar")
scrollingbar = Scrollbar(output_frame)
scrollingbar.pack(side=tk.RIGHT, fill=tk.Y)

log.log("packing output_text")
output_text = tk.Text(output_frame, height=20, width=60, yscrollcommand=scrollingbar.set)
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollingbar.config(command=output_text.yview)

log.log("packing button frame")
button_frame = tk.Frame(root)
button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ns")

### BUTTON CREATION ###

log.log("packing buttons")
submit_button = tk.Button(button_frame, text="Submit", command=task(submit_flashcards)) # This button gets information from wikipedia or another source (if we implement)
dictate_button = tk.Button(button_frame, text="Dictate", command=task(dictate_flashcards)) # not sure

dictate_button.grid(row=0, column=0, pady=5, sticky="ew")

### UTILITY MENU CREATION ###

log.log("packing menu")
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

log.log("packing inputs")
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
log.log("starting keybind manager")
keybind = KeybindManager(root)
log.log("binding keys")
keybind.bind("Return", task(submit_flashcards))


### MAIN LOOP ###
'''framerate = 60

engine = TkEngine(root, framerate)
engine.start()
'''

mainloop = task(main_loop)
log.log("Starting mainloop")
mainloop.start_ignore()
log.log("starting tkinter")
root.mainloop()
