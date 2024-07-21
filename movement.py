import threading
import time
import tkinter
from random import *
from tkinter import *

import speech_recognition

import speech
import pyautogui

frames = []
window = Tk()
label = Label(window)
label.pack()
default = PhotoImage(file="animations/idle.gif")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
horizontal_displacement = 0
xpos = int(screen_width/2)
clicked = False
speaking = False
img = PhotoImage(file="animations/bubble_bl.png")
bubble_text = ""
def setupWindow():
    global frames, window, label, screen_width, screen_height
    speech.getAPI()
    window.geometry("150x160+"+str(xpos)+"+"+str(screen_height-200))
    window.config(highlightbackground="pink")
    window.overrideredirect(True)
    window.wm_attributes("-transparentcolor", "pink")
    window.attributes("-topmost", True)
    label.config(bg="pink")
    setUpIdle()
    label.bind("<Button-1>", click)
    window.after(0, animate, 0)
    window.mainloop()


def setUpIdle():
    global frames, horizontal_displacement
    print("idle")
    frames = [PhotoImage(file="animations/idle.gif", format="gif -index %i" %(i)) for i in range(16)]
    horizontal_displacement = 0
    label.config(image=frames[0])

def setUpRight():
    global frames, horizontal_displacement
    print("right")
    frames = [PhotoImage(file="animations/walking_right.gif", format="gif -index %i" %(i)) for i in range(4)]
    horizontal_displacement = 5
    label.config(image=frames[0])

def setUpLeft():
    global frames, horizontal_displacement
    print("left")
    frames = [PhotoImage(file="animations/walking_left.gif", format="gif -index %i" %(i)) for i in range(4)]
    horizontal_displacement = -5
    label.config(image=frames[0])

def setUpSleep():
    global frames, horizontal_displacement
    print("sleep")
    frames = [PhotoImage(file="animations/sleeping.gif", format="gif -index %i" %(i)) for i in range(16)]
    horizontal_displacement = 0
    label.config(image=frames[0])

def setUpAlerted():
    global frames, horizontal_displacement, label
    frames = [PhotoImage(file="animations/alerted.gif", format="gif -index %i" % (i)) for i in range(10)]
    horizontal_displacement = 0
    label.config(image=frames[0])



def changeAnimation():
    options = ["idle", "idle", "right", "left", "sleep"]
    ans = choice(options)
    print("chose: "+ans)
    if ans == "idle":
        setUpIdle()
    elif ans == "left":
        setUpLeft()
    elif ans == "right":
        setUpRight()
    elif ans == "sleep":
        setUpSleep()


def animate(count):
    global frames, label, window, default, xpos, horizontal_displacement, clicked, speaking
    if len(frames) > 0:
        count += 1
        if count >= len(frames):
            count = 0
            if clicked:
                count = len(frames)-4
        label.config(image=frames[count])
        num = randint(0, 101)
        #print(num)
        if num < 5 and not clicked:
            changeAnimation()
            label.config(image=default)
    xpos += horizontal_displacement
    if xpos < 0:
        xpos = 0
    elif xpos > screen_width-150:
        xpos = screen_width-150
    window.geometry("150x160+" + str(xpos) + "+" + str(screen_height-220))
    if speaking:
        summonSpeech()
        speaking = False
    window.after(100, animate, count)

def click(event):
    global xpos, screen_height, clicked, speech_thread
    ypos = screen_height - 220
    mouse_pos = pyautogui.position()
    if xpos < mouse_pos[0] < xpos+150 and ypos < mouse_pos[1] < ypos + 160 and not clicked:
        clicked = True
        setUpAlerted()
        try:
            speech_thread = threading.Thread(target=speech.listen)
            speech_thread.start()
        except Exception as e:
            raise e

def unclick(text):
    global clicked, speech_thread, speaking, bubble_text
    clicked = False
    setUpIdle()
    speaking = True
    bubble_text = text




def summonSpeech():
    global img, bubble_text
    print("test")
    bubble = Toplevel()
    ypos = screen_height-200
    bubble.geometry("300x150+"+str(xpos-300)+"+"+str(ypos-150))
    bubble.config(highlightbackground="pink")
    bubble.overrideredirect(True)
    bubble.wm_attributes("-transparentcolor", "pink")
    bubble.attributes("-topmost", True)
    img = PhotoImage(file="animations/bubble_br.png")
    pic = Label(bubble, bg="pink", text=bubble_text, image=img, compound="center", font="Helvetica 12 bold")
    pic.pack()
    if xpos > 450:
        img = PhotoImage(file="animations/bubble_br.png")
    else:
        bubble.geometry("300x150+" + str(xpos + 150) + "+" + str(ypos - 150))
        img = PhotoImage(file="animations/bubble_bl.png")
    pic.config(image=img)
    window.update_idletasks()
