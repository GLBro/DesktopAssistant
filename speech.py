import random
from datetime import date
from datetime import datetime
import speech_recognition as sr
from pyaudio import *
import os
from dotenv import load_dotenv
import pyttsx3
import sqlite3
import movement
import time
import video
import web


def get_api():
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
    movement.unclick(respond(text[0]))


def speak(text):
    global engine
    engine.say(text)
    engine.runAndWait()
    movement.stop_talking()


def respond(text):
    global prev_question
    connection2 = sqlite3.connect('chat.db')
    cursor2 = connection2.cursor()
    text = text.lower()
    prev_question = text
    if "name" in text:
        return "my name is cubey, nice to meet you"
    elif text == "":
        return "Sorry, I didn't catch that"
    elif "joke" in text:
        joke_array = ["what do you call a magic dog? a labracadabrador!", "what did the pirate say when he turned 80? aye matey!", "did you hear about the two people who stole a calendar? they each got six months!", "why are ghosts such bad liars? because they are easy to see through!", "did you hear about the actor who fell through the floorboards? he was just going through a stage!"]
        return random.choice(joke_array)
    elif "turn off" in text:
        movement.turning_off()
        return "ok i will turn off"
    elif "time" in text or "date" in text:
        current_day = date.today().strftime("%d %B %Y")
        current_time = datetime.now().strftime("%H:%M")
        return "the current day is " + current_day + " and the current time is " + current_time
    elif "display " in text or "show me" in text:
        text = text.replace("show me a ", "", 1).replace("show me ", "", 1)
        text = text.replace("display ", "", 1)
        movement.activate_image(web.get_image(text))
        return "this is the " + text + " i found"
    elif "play " in text:
        text = text.replace("play ", "")
        return video.get_video(text)
    else:
        try:
            ans = cursor2.execute("SELECT ANSWER FROM responses WHERE QUESTION = '"+text+"'").fetchall()
            ans = ans[0][0]
        except:
            ans = cursor2.execute("SELECT * FROM responses").fetchall()
            best_pos = -1
            best_score = 0
            for i in range(len(ans)):
                score = lcs(ans[i][0], text) - (abs(len(ans[i][0])-len(text))*0.1)
                #print(score)
                if len(ans[i][0])*0.8 < score and score > best_score:
                    print(len(ans[i][0])*0.8, score)
                    best_pos = i
                    best_score = score
            if best_pos == -1:
                ans = "sorry i didn't understand, please tell me an appropriate answer"
                movement.ask_for_new_answer()
            else :
                ans = ans[best_pos][1]
        print(ans)
        return ans



def lcs(text1, text2):
    if text1 in text2:
        return len(text1)
    if text2 in text1:
        return len(text2)
    data = [[0]*(len(text2)+1) for i in range(len(text1)+1)]
    for i in range(1, len(text1)+1):
        for j in range(1, len(text2)+1):
            if text1[i-1] == text2[j-1]:
                #print(text1[i-1], text2[j-1], i, j)
                data[i][j] = data[i-1][j-1]+1
            else:
                data[i][j] = max(data[i-1][j], data[i][j-1])
    #print(data)
    return data[len(text1)][len(text2)]

def create_table():
    global connection, cursor
    connection.execute("CREATE TABLE responses(QUESTION TEXT PRIMARY KEY UNIQUE , ANSWER TEXT);")
    connection.execute("INSERT INTO responses VALUES ('how are you', 'i am good thanks')")
    connection.execute("INSERT INTO responses VALUES ('hi', 'hello')")
    cursor.execute("SELECT * FROM responses")
    print(cursor.fetchall())

def train():
    connection.execute("INSERT OR IGNORE INTO responses VALUES ('what are you', 'i am you virtual desktop assistant')")
    connection.execute("INSERT OR IGNORE INTO responses VALUES ('what is your name', 'my name is cubey, nice to meet you')")
    connection.execute("INSERT OR IGNORE INTO responses VALUES ('what can you do', 'i can talk, tell you the weather, play videos, and search the web, just ask')")
    connection.execute("INSERT OR IGNORE INTO responses VALUES ('hello', 'hi, how may i assist you')")
    connection.execute("INSERT OR IGNORE INTO responses VALUES ('hello world', 'i can assure you i am functioning')")
    connection.execute("INSERT OR IGNORE INTO responses VALUES ('thank you', 'no problem')")

def learn():
    global microphone, recognizer, connection, cursor, prev_question
    time.sleep(5)
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    text = recognizer.recognize_houndify(audio, CLIENTID, CLIENTKEY)
    print(text)
    if text[0] == "":
        text = ["Sorry, I didn't catch that"]
    else:
        movement.update_new_answer(text[0])
    movement.unclick(text[0])

def add_to_database(text):
    global prev_question, connection, cursor
    connection.execute("INSERT OR IGNORE INTO responses VALUES ('"+prev_question+"', '"+text+"')")
    connection.commit()

recognizer = sr.Recognizer()
microphone = sr.Microphone()
CLIENTID = ""
CLIENTKEY = ""
engine = pyttsx3.init()
connection = sqlite3.connect('chat.db')
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='responses'")
if cursor.fetchone() is None:
    create_table()
else:
    #train()
    cursor.execute("SELECT * FROM responses")
    print(cursor.fetchall())
connection.commit()
prev_question = ""
