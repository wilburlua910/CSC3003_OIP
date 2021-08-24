#!/usr/bin/env python3

# Export display variable
import os
os.environ["DISPLAY"] = ":0.0"

# Screen
from guizero import App, Text, PushButton, Box

positive_green = "#6eff56"
negative_red = "#ff3333"
confused_yellow = "#fcff56"

# Create app object
app = App(title="SyClone")
app.bg = "black"
app.text_color = "black"

def goto_cleaning_screen():
    start_screen_box.hide()
    cleaning_screen_box.show()

def goto_confirm_stop_screen():
    cleaning_screen_box.hide()
    confirm_stop_screen_box.show()

def goto_start_screen():
    confirm_stop_screen_box.hide()
    start_screen_box.show()

# Start screen
start_screen_box = Box(app, visible=True, width="fill", height="fill")
ssb_titletext = Text(start_screen_box, text="SyClone", color="white")
ssb_start_button = PushButton(start_screen_box, text="Start", command=goto_cleaning_screen, width="fill", height="fill")
ssb_start_button.bg = positive_green

# Cleaning screen
cleaning_screen_box = Box(app, visible=False, width="fill", height="fill")
csb_title_text = Text(cleaning_screen_box, text="Running Cycle 1", color="white")
csb_stop_button = PushButton(cleaning_screen_box, text="Stop", command=goto_confirm_stop_screen, width="fill", height="fill")
csb_stop_button.bg = negative_red

# Confirm stop screen
confirm_stop_screen_box = Box(app, visible=False, width="fill", height="fill")
cssb_title_text = Text(confirm_stop_screen_box, text="Confirm stop?", color="white")
cssb_confirm_button = PushButton(confirm_stop_screen_box, text="Confirm", command=goto_start_screen, width="fill", height="fill")
cssb_confirm_button.bg = negative_red

app.set_full_screen()
app.display()
