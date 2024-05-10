### WEB SUMMARIES (ENCYCLOPEDIA) PROGRAM ###
### CREATED BY MINAS MARENTIS ON 24/11/22 AND COPIED INTO NEW ###
### FILE FOR PROGRAMMING COMPETITION ON 5/5/24 IN ORDER TO BE REVIEWED. ###
### SOURCED FROM M-M BASIC DOS [VERSION 1.15], SUBSET OF WEB EXTENSION COMMAND ###

### FEATURES: TEXT WRAPPING FOR BETTER VISUAL ELEMENTS, SPEECH MODULATOR TO DICTATE OUTPUT TEXT ###

import wikipedia
import textwrap
import pyttsx3
import os

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

        ### PROGRAM OUTPUT (TEXT AND AUDIO) ###
        text = f'{result}'
        engine.say(text)
        engine.runAndWait()

        print("")

        save = input("SAVE SUMMARY (Y/N)?: ").upper()

        if save == "Y":
            file_name = input("ENTER FILE NAME: ").upper()

            if os.path.exists(file_name):
                print("ERROR: FILE ALREADY EXISTS.")
                print("")
                exit()
                
            with open(file_name, mode='w') as file:
                file.write(wrapped_summary)
                file.close()

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
                
        else:
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
print("NOTE: ENSURE THAT ALL ABBREVIATIONS, SLANG LANGUAGE, AND ACRONYMS ARE OMITTED FROM TOPIC INPUT.")

topic = input("ENTER A TOPIC: ")
lines = int(input("NUMBER OF SENTENCES REQUIRED: "))
print("")
search(topic, lines)
