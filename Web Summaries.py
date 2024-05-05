### WEB-SUMMARIES (ENCYCLOPEDIA) PROGRAM ###
### CREATED BY MINAS MARENTIS ON 24/11/22 AND COPIED INTO NEW ###
### SOURCED FROM M-M BASIC DISK OPERATING SYSTEM [VERSION 1.15], SUBSET OF WEB EXTENSION ###
### FILE FOR PROGRAMMING COMPETITION ON 5/5/24 IN ORDER TO BE REVIEWED ###

### FEATURES: TEXT WRAPPING FOR BETTER VISUAL ELEMENTS, SPEECH MODULATOR TO DICTATE OUTPUT TEXT ###

import wikipedia
import textwrap
import pyttsx3

### SEARCH FUNCTION TO SOURCE INFORMATION FROM WIKIPEDIA ###
def search(topic, lines):
    try:
        ### INITIALISATION OF SPEECH UNIT ###
        engine = pyttsx3.init()
        voice_num = 1
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[voice_num].id)

        width = 80
        result = wikipedia.summary(topic, sentences=lines)
        wrapped_summary = textwrap.wrap(result, width=width)
        
        for line in wrapped_summary:
            print(line)

        ### PROGRAM OUTPUT ###
        text = f'{result}'
        engine.say(text)
        engine.runAndWait()

        print("")

        choice = input("SEARCH AGAIN (Y/N)?: ").upper()

        if choice == 'Y':
            print("")

            topic = input("ENTER A TOPIC: ")
            lines = int(input("NUMBER OF SENTENCES REQUIRED: "))
            search(topic, lines)
            
        else:
            print("")
            print("="*25)
            exit()

    except Exception as e:
        print(f"ERROR: '{e}'")

        print("")

        choice = input("SEARCH AGAIN (Y/N)?: ").upper()

        if choice == 'Y':
            print("")
            
            topic = input("ENTER A TOPIC: ")
            lines = int(input("NUMBER OF SENTENCES REQUIRED: "))
            search(topic, lines)

        else:
            print("")
            print("="*25)
            exit()

### CALLING THE 'SEARCH' FUNCTION ###
topic = input("ENTER A TOPIC: ")
lines = int(input("NUMBER OF SENTENCES REQUIRED: "))
search(topic, lines)
