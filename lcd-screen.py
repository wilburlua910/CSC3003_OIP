#!/usr/bin/env python3

import os
import threading
import queue
import time
from enum import Enum
from guizero import App, Text, PushButton, Box

class State(Enum):
    WAITING = 0
    START_CLEANING = 1
    DONE_CLEANING = 2

positive_green = "#6eff56"
negative_red = "#ff3333"
confused_yellow = "#fcff56"

# App stuff
os.environ["DISPLAY"] = ":0.0"

state_queue = queue.Queue()

def queue_listener():
    while 1:
        for state in list(state_queue.queue):
            print(state)


# threading.Thread(target=queue_listener).start()

# Screen stuff
def goto_cleaning_screen():
    start_screen_box.hide()
    cleaning_screen_box.show()
    state_queue.put(State.START_CLEANING)

    # for demo
    threading.Thread(target=arduino_ack, args=(state_queue, )).start()

# for demo
def arduino_ack(state_queue):
    time.sleep(3)
    state_queue.get(timeout=1)
    state_queue.put(State.DONE_CLEANING)

previous_screen: Box = None
# previous_repeat = None

def goto_confirm_stop_screen(previous_screen1):
    global previous_screen
    # global previous_repeat
    previous_screen = previous_screen1
    # previous_repeat = previous_screen1.repeat
    previous_screen.hide()
    # previous_screen.cancel()
    confirm_stop_screen_box.show()

def goback():
    global previous_screen
    confirm_stop_screen_box.hide()
    previous_screen.show()
    previous_screen = None

def goto_start_screen():
    confirm_stop_screen_box.hide()
    complete_good_screen_box.hide()
    complete_bad_screen_box.hide()
    start_screen_box.show()

# not used in command params, executed by worker threads/listeners
def goto_drying_screen():
    cleaning_screen_box.hide()
    drying_screen_box.show()
    
    # for demo
    threading.Thread(target=zoom).start()


# for demo
def zoom():
    time.sleep(3)
    goto_inspecting_screen()
    time.sleep(3)
    goto_complete_good_screen()

def goto_inspecting_screen():
    drying_screen_box.hide()
    inspecting_screen_box.show()

def goto_complete_good_screen():
    inspecting_screen_box.hide()
    complete_good_screen_box.show()

# poll based listeners
def cleaning_done():
    if cleaning_screen_box.visible and state_queue.qsize() > 0 and state_queue.queue[0] == State.DONE_CLEANING:
        state_queue.get()
        goto_drying_screen()

# Create app object
app = App(title="SyClone")
app.bg = "black"
app.text_color = "black"
app.set_full_screen()

# Start screen
start_screen_box = Box(app, visible=True, width="fill", height="fill")
ssb_titletext = Text(start_screen_box, text="SyClone", color="white")
ssb_start_button = PushButton(start_screen_box, text="Start", command=goto_cleaning_screen, width="fill", height="fill")
ssb_start_button.bg = positive_green

# Restart 
# restart_screen_box = Box(app, visible=False, width="fill", height="fill")
# rsb_title_text = Text(restart_screen_box, text="Restart from previously stopped cycle?", color="white")
# rsb_cancel_button = PushButton(restart_screen_box, text="Continue washing", command=goto_start_screen, width="fill", height="fill")
# rsb_cancel_button.bg = positive_green
# rsb_confirm_button = PushButton(restart_screen_box, text="Stop", command=goto_start_screen, width="fill", height="fill")
# rsb_confirm_button.bg = negative_red

# Cleaning screen
cleaning_screen_box = Box(app, visible=False, width="fill", height="fill")
csb_title_text = Text(cleaning_screen_box, text="Washing and sterilising", color="white")
csb_stop_button = PushButton(cleaning_screen_box, text="Stop", command=goto_confirm_stop_screen, args=[cleaning_screen_box], width="fill", height="fill")
csb_stop_button.bg = negative_red
cleaning_screen_box.repeat(1000, cleaning_done)

# Drying
drying_screen_box = Box(app, visible=False, width="fill", height="fill")
dsb_title_text = Text(drying_screen_box, text="Drying", color="white")
dsb_stop_button = PushButton(drying_screen_box, text="Stop", command=goto_confirm_stop_screen, args=[drying_screen_box], width="fill", height="fill")
dsb_stop_button.bg = negative_red

# Inspecting
inspecting_screen_box = Box(app, visible=False, width="fill", height="fill")
isb_title_text = Text(inspecting_screen_box, text="Inspecting", color="white")
isb_stop_button = PushButton(inspecting_screen_box, text="Stop", command=goto_confirm_stop_screen, args=[inspecting_screen_box], width="fill", height="fill")
isb_stop_button.bg = negative_red

# Confirm stop screen
confirm_stop_screen_box = Box(app, visible=False, width="fill", height="fill")
cssb_title_text = Text(confirm_stop_screen_box, text="Confirm stop?", color="white")
cssb_cancel_button = PushButton(confirm_stop_screen_box, text="Continue", command=goback, width="fill", height="fill")
cssb_cancel_button.bg = positive_green
cssb_confirm_button = PushButton(confirm_stop_screen_box, text="Stop", command=goto_start_screen, width="fill", height="fill")
cssb_confirm_button.bg = negative_red

# Complete - clean
complete_good_screen_box = Box(app, visible=False, width="fill", height="fill")
cgsb_title_text = Text(complete_good_screen_box, text="Cleaning complete", color="white")
cgsb_stop_button = PushButton(complete_good_screen_box, text="Confirm", command=goto_start_screen, width="fill", height="fill")
cgsb_stop_button.bg = positive_green

# Complete - inspect
complete_bad_screen_box = Box(app, visible=False, width="fill", height="fill")
cbsb_title_text = Text(complete_bad_screen_box, text="Cleaning incomplete, check for cleanliness", color="white")
cbsb_stop_button = PushButton(complete_bad_screen_box, text="Confirm", command=goto_start_screen, width="fill", height="fill")
cbsb_stop_button.bg = confused_yellow

app.display()
