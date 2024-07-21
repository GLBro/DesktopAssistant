import speech_recognition as sr
from pyaudio import *
import os
from dotenv import load_dotenv


import movement

recognizer = sr.Recognizer()
microphone = sr.Microphone()
CLIENTID = ""
CLIENTKEY = ""


def getAPI():
    global CLIENTID, CLIENTKEY
    load_dotenv()
    CLIENTID = os.getenv("CLIENTID")
    CLIENTKEY = os.getenv("CLIENTKEY")


def listen():
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    text = recognizer.recognize_houndify(audio, CLIENTID, CLIENTKEY)
    print(text)
    movement.unclick(text[0])

