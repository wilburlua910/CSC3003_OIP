#!/usr/bin/env python3

from PIL.Image import init
from Inference.inference import Camera
import os
import threading
import concurrent.futures as futures
import queue
import time
from enum import Enum
from guizero import App, Text, PushButton, Box


#Custom imports 
from Inference import inference
import gpiocontrol


positive_green = "#6eff56"
negative_red = "#ff3333"
confused_yellow = "#fcff56"

size, interpreter, labels = None, None, None

# App stuff
os.environ["DISPLAY"] = ":0.0"

# Screen stuff
def goto_cleaning_screen():
    start_screen_box.hide()
    cleaning_screen_box.show()

previous_screen: Box = None
# previous_repeat = None

def goto_confirm_stop_screen(previous_screen1):
    global previous_screen

    previous_screen = previous_screen1

    previous_screen.hide()

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

def goto_inspecting_screen():
    cleaning_screen_box.hide()
    inspecting_screen_box.show()

    # #TODO - Camera stuff
    # with futures.ThreadPoolExecutor() as executor:
    #     future_obj = executor.submit(camera.run_inference(
    #         labels= labels,
    #         interpreter= interpreter,
    #         size = size 
    #     ))
    # future_obj.add_done_callback(inference_cb)

def goto_complete_good_screen():
    inspecting_screen_box.hide()
    complete_good_screen_box.show()

# poll based listeners
def cleaning_done():
    if cleaning_screen_box.visible:

        #TODO - Check if Arduino pin is HIGH 
        goto_inspecting_screen()

def inspecting_done():
    pass
    #TODO - check boolean input from camera 
    #Check if -> good ? 1 , bad? 2, not done yet ? 0

def initialize_camera():
    cam = Camera()
    time.sleep(1)
   
    return cam

#Camera 
camera = initialize_camera()
size, interpreter, labels = camera.size, camera.interpreter, camera.labels

# Create app object
app = App(title="SyClone")
app.bg = "black"
app.text_color = "black"
app.set_full_screen()


def inference_cb(future_obj):

    #Print 1 or 2
    print("State of cleaning: " + future_obj.results) 


# Start screen
start_screen_box = Box(app, visible=True, width="fill", height="fill")
ssb_titletext = Text(start_screen_box, text="SyClone", color="white")
ssb_start_button = PushButton(start_screen_box, text="Start", command=goto_cleaning_screen, width="fill", height="fill")
ssb_start_button.bg = positive_green

#TODO: gotocleaningscreen => pull pin to high to indicate standy > start 

# Cleaning screen
cleaning_screen_box = Box(app, visible=False, width="fill", height="fill")
csb_title_text = Text(cleaning_screen_box, text="Cleaning", color="white")
csb_stop_button = PushButton(cleaning_screen_box, text="Stop", command=goto_confirm_stop_screen, args=[cleaning_screen_box], width="fill", height="fill")
csb_stop_button.bg = negative_red
cleaning_screen_box.repeat(1000, cleaning_done)

# Inspecting
inspecting_screen_box = Box(app, visible=False, width="fill", height="fill")
isb_title_text = Text(inspecting_screen_box, text="Inspecting", color="white")
isb_stop_button = PushButton(inspecting_screen_box, text="Stop", command=goto_confirm_stop_screen, args=[inspecting_screen_box], width="fill", height="fill")
isb_stop_button.bg = negative_red
inspecting_screen_box.repeat(1000, inspecting_done)

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
