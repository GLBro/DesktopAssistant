import threading
import time
import tkinter
from random import *
from tkinter import *

import speech_recognition
from PIL import ImageTk, Image

import speech
import pyautogui

frames = []  # Stores the frames used in the current animation
window = Tk()  # Window that displays the assistant
label = Label(window)  # The label the displays the assistent
label.pack()
default = PhotoImage(file="animations/idle.gif")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
horizontal_displacement = 0  # How fast the assistant is moving
xpos = int(screen_width / 2)  # Current x position
clicked = False  # Has the assistant been clicked
start_speaking = False  # Is the assistant preparing to speak
speaking = False  # Is the assistant speaking
img = PhotoImage(file="animations/bubble_bl.png")  # Default image
bubble_text = ""  # Text in the speech bubble
bubble_reference = None  # The window that the text bubble is stored in
asking = False  # Is the assistant asking for a response
new_answer = ""  # The new anwser given by the user
add_new_answer = False  # Does the assistant need to add a new answer to the database
turn_off = False  # Does the assistant need to turn off
image_to_display = ImageTk.PhotoImage(file="animations/bubble_bl.png")  # Speech bubble image
image_toggle = False  # Does the assistant need to display an image
image_reference = None  # Stores the window that the displayed image is in
image_time = -1  # Countdown until displayed image should disappear


# Displays the window containing the assistant
def setup_window():
    global frames, window, label, screen_width, screen_height
    speech.get_api()
    window.geometry("150x160+" + str(xpos) + "+" + str(screen_height - 200))
    window.config(highlightbackground="pink")
    window.overrideredirect(True)
    window.wm_attributes("-transparentcolor", "pink")
    window.attributes("-topmost", True)
    label.config(bg="pink")
    setup_idle()
    label.bind("<Button-1>", click)
    window.after(0, animate, 0)
    window.mainloop()


# Current animation becomes idle
def setup_idle():
    global frames, horizontal_displacement
    print("idle")
    frames = [PhotoImage(file="animations/idle.gif", format="gif -index %i" % (i)) for i in range(16)]
    horizontal_displacement = 0
    label.config(image=frames[0])


# Current animation becomes walking right
def setup_right():
    global frames, horizontal_displacement
    print("right")
    frames = [PhotoImage(file="animations/walking_right.gif", format="gif -index %i" % (i)) for i in range(4)]
    horizontal_displacement = 5
    label.config(image=frames[0])


# Current animation becomes walking left
def setup_left():
    global frames, horizontal_displacement
    print("left")
    frames = [PhotoImage(file="animations/walking_left.gif", format="gif -index %i" % (i)) for i in range(4)]
    horizontal_displacement = -5
    label.config(image=frames[0])


# Current animation becomes sleeping
def setup_sleep():
    global frames, horizontal_displacement
    print("sleep")
    frames = [PhotoImage(file="animations/sleeping.gif", format="gif -index %i" % (i)) for i in range(16)]
    horizontal_displacement = 0
    label.config(image=frames[0])


# Current animation becomes alerted
def setup_alerted():
    global frames, horizontal_displacement, label
    print("alert")
    frames = [PhotoImage(file="animations/alerted.gif", format="gif -index %i" % (i)) for i in range(10)]
    horizontal_displacement = 0
    label.config(image=frames[0])


# Current animation becomes talking
def setup_talking():
    global frames, horizontal_displacement, label
    frames = [PhotoImage(file="animations/talking.gif", format="gif -index %i" % (i)) for i in range(9)]
    horizontal_displacement = 0
    label.config(image=frames[0])


# Switches between different animations, idle is more likely than others
def change_animation():
    options = ["idle", "idle", "right", "left", "sleep"]
    ans = choice(options)
    print("chose: " + ans)
    if ans == "idle":
        setup_idle()
    elif ans == "left":
        setup_left()
    elif ans == "right":
        setup_right()
    elif ans == "sleep":
        setup_sleep()


# Main loop of the program, animates image as well as handles any toggles that have been activated
def animate(count):
    global frames, label, window, default, xpos, horizontal_displacement, clicked, start_speaking, speaking, asking, new_answer, add_new_answer, image_toggle, image_time
    if len(frames) > 0:
        count += 1
        if count >= len(frames):
            count = 0
            if clicked:
                count = len(frames) - 4
        label.config(image=frames[count])
        num = randint(0, 101)
        # print(num)
        if num < 5 and not clicked and not speaking and not asking:
            change_animation()
            label.config(image=default)
    xpos += horizontal_displacement
    if xpos < 0:
        xpos = 0
    elif xpos > screen_width - 150:
        xpos = screen_width - 150
    window.geometry("150x160+" + str(xpos) + "+" + str(screen_height - 220))
    if start_speaking:
        summon_speech()
        start_speaking = False
        speaking = True
    if asking and not speaking:
        get_new_answer()
        asking = False
    if add_new_answer:
        speech.add_to_database(new_answer)
        add_new_answer = False
    if turn_off and not speaking and not start_speaking:
        window.destroy()
        exit()
    if image_toggle:
        summon_image()
        image_toggle = False
    if image_time != -1 and image_time + 5 < time.time():
        image_time = -1
        delete_image()
    window.after(100, animate, count)


# Happens when the assistant is clicked, assistant will begin to listen
def click(event):
    global xpos, screen_height, clicked, speech_thread, start_speaking, speaking
    ypos = screen_height - 220
    mouse_pos = pyautogui.position()
    if xpos < mouse_pos[0] < xpos + 150 and ypos < mouse_pos[
        1] < ypos + 160 and not clicked and not start_speaking and not speaking:
        clicked = True
        setup_alerted()
        try:
            speech_thread = threading.Thread(target=speech.listen)
            speech_thread.start()
        except Exception as e:
            unclick("Sorry, I didn't catch that")


# Assistant finishes listening and sets up ability to speak
def unclick(text):
    global clicked, speech_thread, start_speaking, bubble_text, asking, add_new_answer, speaking
    clicked = False
    # setUpIdle()
    start_speaking = True
    bubble_text = text
    split_text = bubble_text.split(" ")
    out = ""
    counter = 0
    limit = 15
    adder = 15
    if len(bubble_text) > 50:
        limit = 25
        adder = 25
    for chunk in split_text:
        counter += len(chunk)
        if counter > limit:
            limit = limit + adder
            out += chunk + "\n"
        else:
            out += chunk + " "
    bubble_text = out
    speech.speak(text)


# Displays speech bubble containing text
def summon_speech():
    global img, bubble_text, bubble_reference
    print("test")
    bubble = Toplevel()
    ypos = screen_height - 200
    bubble.geometry("300x150+" + str(xpos - 300) + "+" + str(ypos - 150))
    bubble.config(highlightbackground="pink")
    bubble.overrideredirect(True)
    bubble.wm_attributes("-transparentcolor", "pink")
    bubble.attributes("-topmost", True)
    img = PhotoImage(file="animations/bubble_br.png")
    font = "Helvetica 12 bold"
    if len(bubble_text) > 50:
        font = "Helvetica 8 bold"
    pic = Label(bubble, bg="pink", text=bubble_text, image=img, compound="center", font=font)
    pic.pack()
    if xpos > 450:
        img = PhotoImage(file="animations/bubble_br.png")
    else:
        bubble.geometry("300x150+" + str(xpos + 150) + "+" + str(ypos - 150))
        img = PhotoImage(file="animations/bubble_bl.png")
    pic.config(image=img)
    setup_talking()
    bubble_reference = bubble
    window.update_idletasks()


# Deletes speech bubble once assistant has stopped talking
def stop_talking():
    global speaking, bubble_reference, asking
    speaking = False
    if not asking:
        setup_idle()
    else:
        setup_alerted()
    bubble_reference.destroy()


# Sets toggle for new answer to be given
def ask_for_new_answer():
    global asking
    asking = True


# Gets a new answer from the user by listening again
def get_new_answer():
    global xpos, screen_height, clicked, speech_thread, asking
    print("Getting new answer")
    clicked = True
    setup_alerted()
    try:
        speech_thread = threading.Thread(target=speech.learn)
        speech_thread.start()
        asking = False
        setup_alerted()
    except Exception as e:
        unclick("Sorry, I didn't catch that")


# Sets toggle to add new answer to database
def update_new_answer(text):
    global new_answer, add_new_answer
    new_answer = text
    add_new_answer = True


# Sets toggle to turn off the assistant
def turning_off():
    global turn_off
    turn_off = True

# Sets toggle to display a new image
def activate_image(new_image):
    global image_to_display, image_toggle
    image_to_display = ImageTk.PhotoImage(new_image)
    image_toggle = True


# Displays a new image above the assistant
def summon_image():
    global image_to_display, image_reference, image_toggle, image_time
    print("displaying image")
    level = Toplevel()
    ypos = screen_height - 200
    size = (image_to_display.width(), image_to_display.height())
    level.geometry(str(size[0]) + "x" + str(size[1]) + "+" + str(xpos) + "+" + str(ypos - size[1]))
    level.config(highlightbackground="pink")
    level.overrideredirect(True)
    level.wm_attributes("-transparentcolor", "pink")
    level.attributes("-topmost", True)
    pic = Label(level, image=image_to_display, bg="pink")
    pic.img = img
    pic.pack()
    image_reference = level
    image_time = time.time()
    window.update_idletasks()


# Deletes the displayed image
def delete_image():
    global image_reference
    print("deleting image")
    image_reference.destroy()
    setup_idle()
