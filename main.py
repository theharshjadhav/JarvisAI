import pyttsx3
from decouple import config
from datetime import datetime
import speech_recognition as sr
from random import choice
from utils import opening_text
import os
import subprocess as sp
import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib


USERNAME = config('USERNAME')
BOTNAME = config('BOTNAME')


engine = pyttsx3.init('sapi5')
# Set Rate
engine.setProperty('rate', 190)
# Set Volume
engine.setProperty('volume', 1.0)
# Set Voice (Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


# Text to Speech Conversion
def speak(text):
    """Used to speak whatever text is passed to it"""
    
    engine.say(text)
    engine.runAndWait()

def take_user_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        # r.adjust_for_ambient_noise = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        if not 'exit' in query or 'stop' in query:
            speak(choice(opening_text))
        else:
            hour = datetime.now().hour
            if hour>=21 and hour <= 6:
                speak("Good Night Sir! Take Care")
            else:
                speak("Have a Good Day Sir!")

    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that. Can you repeat?")
    
    except sr.RequestError:
        speak("Sorry, there was an error processing your request. Please try again later.")
    
    except:
        speak("Sorry didn't Understand that, can you repeat again? ")
        query = 'None'

    return query
    # return None


def greet_user():
    """Greets the user according to the time"""
    
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good afternoon {USERNAME}")
    elif (hour >= 16) and (hour < 23):
        speak(f"Good Evening {USERNAME}")
    speak(f"Hello {USERNAME} I am {BOTNAME}. How may I assist you?")


def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)

# def open_brave():
#     os.startfile(paths['brave'])

# def open_chrome():
#     os.startfile(paths['chrome'])

# def open_vscode():
#     os.startfile(paths['vscode'])


def open_application(command):
    paths = {
        'brave': r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        'chrome': r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        'vscode': r"C:\Users\harsh\AppData\Local\Programs\Microsoft VS Code\Code.exe"
    }

    command = command.lower()

    # Check if the spoken command contains "open" and an application name
    if 'open' in command:
        for app in paths:
            if app in command:
                app_path = paths.get(app)  # Get the path corresponding to the app
                sp.Popen(app_path)  # Open the application using its path
                return True
        # If no application found
        speak("Application not found in command!")
        return False
    else:
        speak("Invalid command format!")
        return False

# Get user input and open the application
user_command = take_user_input()
open_application(user_command)

