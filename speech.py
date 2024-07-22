import speech_recognition as sr
from pyaudio import *
import os
from dotenv import load_dotenv
import pyttsx3

import movement

recognizer = sr.Recognizer()
microphone = sr.Microphone()
CLIENTID = ""
CLIENTKEY = ""
engine = pyttsx3.init()


def getAPI():
    global CLIENTID, CLIENTKEY
    load_dotenv()
    CLIENTID = os.getenv("CLIENTID")
    CLIENTKEY = os.getenv("CLIENTKEY")


def listen():
    with microphone as source:
        # recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    text = recognizer.recognize_houndify(audio, CLIENTID, CLIENTKEY)
    print(text)
    if text[0] == "":
        text = ["Sorry, I didn't catch that"]
    movement.unclick(text[0])


def speak(text):
    global engine
    engine.say(text)
    engine.runAndWait()
    movement.stopTalking()


def respond(text):
    text = text.lower()



def LCS(text1, text2):
    if text1 in text2:
        return len(text1)
    if text2 in text1:
        return len(text2)
    data = [[0]*(len(text2)+1) for i in range(len(text1)+1)]
    for i in range(len(text1)+1):
        for j in range(len(text2)+1):
            if text1[i-1] == text2[j-1]:
                data[i][j] = data[i-1][j-1]+1
            else:
                data[i][j] = max(data[i-1][j], data[i][j-1])
    return data[len(text1)][len(text2)]
