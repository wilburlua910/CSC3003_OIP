#!/usr/bin/env python3

from Inference.inference import Camera
import os
import concurrent.futures as futures
import time
from guizero import App, Text, PushButton, Box
from Inference import inference
import gpiocontrol
import constants

# App stuff
os.environ["DISPLAY"] = ":0.0"

# Initialise camera for inference
def initialize_camera():
    cam = Camera()
    time.sleep(1)
    return cam

# Camera
camera = initialize_camera()
size, interpreter, labels = camera.size, camera.interpreter, camera.labels



# Screen stuff
def goto_cleaning_screen():
    start_screen_box.hide()
    cleaning_screen_box.show()

previous_screen_saved: Box = None

def goto_confirm_stop_screen(previous_screen: Box):
    global previous_screen_saved
    previous_screen_saved = previous_screen
    previous_screen_saved.hide()
    confirm_stop_screen_box.show()

def goback():
    global previous_screen_saved
    confirm_stop_screen_box.hide()
    previous_screen_saved.show()
    previous_screen_saved = None

def goto_start_screen():
    complete_good_screen_box.hide()
    complete_bad_screen_box.hide()
    start_screen_box.show()

def goto_abend_start_screen():
    confirm_stop_screen_box.hide()
    start_screen_box.show()
    # TODO: send abend signal 3s

def goto_inspecting_screen():
    cleaning_screen_box.hide()
    inspecting_screen_box.show()

    # for debug
    print('Im in inspection block')

    with futures.ThreadPoolExecutor(max_workers=1) as executor:
        future_obj = executor.submit(camera.run_inference, interpreter, size, labels)
    future_obj.add_done_callback(inference_cb)

    # for debug
    print(future_obj.result())

def goto_complete_good_screen():
    inspecting_screen_box.hide()
    complete_good_screen_box.show()

def goto_complete_bad_screen():
    inspecting_screen_box.hide()
    complete_bad_screen_box.show()

# GUI polling state listeners
def cleaning_done():
    if cleaning_screen_box.visible:
        time.sleep(3)
    # TODO: write proper codes 
    #  and gpiocontrol.get_signal_done_cleaning():
        goto_inspecting_screen()

inference_done: inference.State = inference.State.STATE_IN_PROGRESS

def inspecting_done():
    global inference_done
    if inspecting_screen_box.visible:
        if inference_done == inference.State.STATE_ALL_CLEAN:
            goto_complete_good_screen()
        elif inference_done == inference.State.STATE_UNCLEAN:
            goto_complete_bad_screen()

# Callback for inference future
def inference_cb(future):
    global inference_done
    inference_done = future.result()



# Create app object
app = App(title="SyClone")
app.bg = "black"
app.text_color = "black"
app.set_full_screen()

# Start screen
start_screen_box = Box(app, visible=True, width="fill", height="fill")
ssb_titletext = Text(start_screen_box, text="SyClone", color="white")
ssb_start_button = PushButton(start_screen_box, text="Start", command=goto_cleaning_screen, width="fill", height="fill")
ssb_start_button.bg = constants.POSITIVE_GREEN

#TODO: gotocleaningscreen => pull pin to high to indicate standy > start 

# Cleaning screen
cleaning_screen_box = Box(app, visible=False, width="fill", height="fill")
csb_title_text = Text(cleaning_screen_box, text="Cleaning", color="white")
csb_stop_button = PushButton(cleaning_screen_box, text="Stop", command=goto_confirm_stop_screen, args=[cleaning_screen_box], width="fill", height="fill")
csb_stop_button.bg = constants.NEGATIVE_RED
cleaning_screen_box.repeat(1000, cleaning_done)

# Inspecting
inspecting_screen_box = Box(app, visible=False, width="fill", height="fill")
isb_title_text = Text(inspecting_screen_box, text="Inspecting", color="white")
isb_stop_button = PushButton(inspecting_screen_box, text="Stop", command=goto_confirm_stop_screen, args=[inspecting_screen_box], width="fill", height="fill")
isb_stop_button.bg = constants.NEGATIVE_RED
inspecting_screen_box.repeat(1000, inspecting_done)

# Confirm stop screen
confirm_stop_screen_box = Box(app, visible=False, width="fill", height="fill")
cssb_title_text = Text(confirm_stop_screen_box, text="Confirm stop?", color="white")
cssb_cancel_button = PushButton(confirm_stop_screen_box, text="Continue", command=goback, width="fill", height="fill")
cssb_cancel_button.bg = constants.POSITIVE_GREEN
cssb_confirm_button = PushButton(confirm_stop_screen_box, text="Stop", command=goto_abend_start_screen, width="fill", height="fill")
cssb_confirm_button.bg = constants.NEGATIVE_RED

# Complete - clean
complete_good_screen_box = Box(app, visible=False, width="fill", height="fill")
cgsb_title_text = Text(complete_good_screen_box, text="Cleaning complete", color="white")
cgsb_stop_button = PushButton(complete_good_screen_box, text="Confirm", command=goto_start_screen, width="fill", height="fill")
cgsb_stop_button.bg = constants.POSITIVE_GREEN

# Complete - inspect
complete_bad_screen_box = Box(app, visible=False, width="fill", height="fill")
cbsb_title_text = Text(complete_bad_screen_box, text="Cleaning incomplete, check for cleanliness", color="white")
cbsb_stop_button = PushButton(complete_bad_screen_box, text="Confirm", command=goto_start_screen, width="fill", height="fill")
cbsb_stop_button.bg = constants.CONFUSED_YELLOW

app.display()
