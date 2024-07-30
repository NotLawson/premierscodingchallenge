### ELECTRONIC FLASHCARDS AND SUMMARIES APPLICATION ###
### BY MINAS MARENTIS AND LAWSON CONALLIN, 2024 ###
### FOR PARTIAL REQUIREMENTS FOR DIGITAL TECHNOLOGY GRADE
### AND PREMIERS CODING CHALLENGE YEAR 2024 ###

### WEB SUMMARIES SORUCED FROM M-M BASIC [VERSION 1.15] ###
### BY MINAS MARENTIS 2022 , 2023 , 2024 ###

### [VERSION 1.01] APPLICATION BETA STAGE ###

### TO BE INCLUDED IN THE PROGRAM: ###
### * 'MAGIC' AI TEXT SUMMARISER, WHERE USER CAN SPECIFY THE CONDENSING OF AN ENTIRE ARTICLE INTO SET NUMBER OF SENTENCES ###
### * 'MAGIC' AI TEXT SUMMARISER - DIFFERENT TONES OF THE SUMMARY: CASUAL OR FORMAL

import tkinter as tk
from tkinter import messagebox, filedialog, END, Scrollbar, Toplevel
from lorem_text import lorem
import pyttsx3
import wikipedia
import textwrap
import os
import win32api 
from textblob import TextBlob

url = ''

### KEYBINDER ALGORITHM (ATTRIBUTED TO LAWSON, 2024) ###
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

### SPELLING CORRECTIONS ###
def spell_check(text):
    a = TextBlob(text)
    return a.correct()

### SAVE-AS FLASHCARDS/SUMMARY ###
def save_as_flashcards(event=None):
    global url

    try:
        url = filedialog.asksaveasfile(mode='w', defaultextension=".rtf", filetypes=(("Document files", "*.rtf"), ("All files", "*.*")))
        content = output_text.get(1.0, END)    
        url.write(content)
        url.close()

    except Exception as e:
        error1 = messagebox.showinfo("ERROR:", e)

### SAVE FLASHCARDS/SUMMARY ###      
def save_flashcards(event=None):
    global url
    
    try:
        if url:
            content = str(output_text.get(1.0, END))
            with open(url, 'w', encoding='utf-8') as wf:
                wf.write(content)
        else:
            url = filedialog.asksaveasfile(mode='w', defaultextension=".rtf", filetypes=(("Document files","*.rtf"), ("All files","*.*")))
            content = output_text.get(1.0, END)    
            url.write(content)
            url.close()

    except Exception as e:
        error1 = messagebox.showinfo("ERROR:", e)

### OPEN FLASHCARDS/SUMMARY TO VIEW ###
def open_flashcards(event=None):
    global url
    
    url = filedialog.askopenfilename(initialdir=os.getcwd(),title="Select File",filetypes=(("Document files","*.rtf"),("All files","*.*")))

    try:
        with open(url, 'r') as fr:
            output_text.delete(1.0, END)
            output_text.insert(1.0, fr.read())
            
    except FileNotFoundError:
        return
    
    except:
        return
    
    root.title(os.path.basename(url))

### SUBROUTINE DEFAULT FROM SUBMISSION OF QUERY TO WIKIPEDIA ###
def get_flashcard_summary(topic, sentences):
    try:
        result = wikipedia.summary(topic, sentences)
        
        return result

    except Exception as e:
        sample_text = ""
        
        for x in range(sentences):
            sample_text = sample_text + lorem.sentence()
            
        return sample_text

### SUBMIT QUERY TO WIKIPEDIA (REQ. INTERNET CONNECTION) ###
def submit_flashcards():
    try:
        topic = input_entry1.get()
        lines = input_entry2.get()
        topic = spell_check(topic)
        topic = str(topic)

        width = 55
        result = get_flashcard_summary(topic, int(lines))       
        wrapped_summary = textwrap.wrap(result, width=width)

        output_text.delete(1.0, END)

        for line in wrapped_summary:
            output_text.insert(END, line + '\n')

    except Exception as e:
        error1 = messagebox.showinfo("ERROR:", e)
        
### PRINTING FUNCTION (FOR WINDOWS COMPUTERS) ###
### THIS WILL PRINT THE FILE TO THE DEFAULT PRINTER LOCATED ON ###
### YOUR PERSONAL COMPUTER. A WAY TO SELECT A PRINTER WILL BE ###
### IMPLEMENTED LATER FOR EASE AND CONVENIENCE OF USE ###
def print_flashcards():
    try:
        file_to_print = filedialog.askopenfilename( 
          initialdir="/", title="Select file",  
          filetypes=(("Text files", "*.txt"), ("all files", "*.*"))) 
          
        if file_to_print: 
            win32api.ShellExecute(0, "print", file_to_print, None, ".", 0)

    except Exception as e:
        error3 = messagebox.showinfo("ERROR:", e)

### SPEECH MODULATOR AND DICTATION OF FLASHCARDS/SUMMARY ###
def dictate_flashcards():
    try:
        topic = input_entry1.get()
        lines = input_entry2.get()

        width = 50
        result = wikipedia.summary(topic, sentences=lines)
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

### CLEAR/NEW OUTPUT SCREEN ###
def clear_output():
    output_text.delete(1.0, END)

### BASIC INFORMATION ABOUT CREATORS ###
def about():
    about_window = Toplevel(root)
    about_window.title("About Study Flashcard Generator")
    about_window.geometry("300x200")
    about_window.resizable(False, False)

    about_label = tk.Label(about_window, text="Study Flashcard And Internet Summaries Generator\n\nCreated By\nMinas Marentis and Lawson Conallin\n\n[VERSION 1.01]")
    about_label.pack(pady=20)

    close_button = tk.Button(about_window, text="Close", command=about_window.destroy)
    close_button.pack(pady=6)

### SIMPLE USER GUIDE, FUNCTIONS OF EACH ELEMENT OF PROGRAM ###
def user_guide():
    pass    

### END APPLICATION TASK ###
def exit_application():
    root.destroy()

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

submit_button = tk.Button(button_frame, text="Submit", command=submit_flashcards)
dictate_button = tk.Button(button_frame, text="Dictate", command=dictate_flashcards)

dictate_button.grid(row=0, column=0, pady=5, sticky="ew")

### UTILITY MENU CREATION ###

main_menu = tk.Menu()

file_menu = tk.Menu(main_menu, tearoff=False)
edit_menu = tk.Menu(main_menu, tearoff=False)
help_menu = tk.Menu(main_menu, tearoff=False)

main_menu.add_cascade(label="File", menu=file_menu)
main_menu.add_cascade(label="Edit", menu=edit_menu)
main_menu.add_cascade(label="Help", menu=help_menu)

file_menu.add_command(label="New", compound=tk.LEFT, accelerator="Ctrl+N", command=clear_output)
file_menu.add_command(label="Open", compound=tk.LEFT, accelerator="Ctrl+O", command=open_flashcards)
file_menu.add_separator()
file_menu.add_command(label="Save", compound=tk.LEFT, accelerator="Ctrl+S", command=save_flashcards)
file_menu.add_command(label="Save As", compound=tk.LEFT, accelerator="Ctrl+Shift+S", command=save_as_flashcards)
file_menu.add_command(label="Print", compound=tk.LEFT, accelerator="Ctrl+P", command=print_flashcards)
file_menu.add_separator()
file_menu.add_command(label="Exit", compound=tk.LEFT, accelerator="Alt+F4", command=exit_application)

edit_menu.add_command(label="Cut", compound=tk.LEFT, accelerator="Ctrl+X", command=lambda:output_text.event_generate("<Control x>"))
edit_menu.add_command(label="Copy", compound=tk.LEFT, accelerator="Ctrl+C", command=lambda:output_text.event_generate("<Control c>"))
edit_menu.add_command(label="Paste", compound=tk.LEFT, accelerator="Ctrl+V", command=lambda:output_text.event_generate("<Control v>"))
edit_menu.add_command(label="Select All", compound=tk.LEFT, accelerator="Ctrl+A", command=lambda:output_text.event_generate("<Control a>"))

help_menu.add_command(label="About", compound=tk.LEFT, command=about)
help_menu.add_command(label="Quick Guide", compound=tk.LEFT, accelerator="Ctrl+H", command=user_guide)

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

submit_button_box = tk.Button(input_frame, text="Submit", command=submit_flashcards)
submit_button_box.grid(row=0, column=2, padx=(5, 0))

root.config(menu=main_menu)

keybind = KeybindManager(root)
keybind.bind("Return", submit_flashcards)

### MAIN LOOP ###

root.mainloop()
