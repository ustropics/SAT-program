from config import *

import os
import json
import panel as pn
import time
from PIL import Image


def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

def create_directories():
    os.makedirs(nc_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)
            

def default_locations():
    with open(location_json, 'r') as f:
        data = json.load(f)

    locations = [item['location'] for item in data]
    return locations

def location_data(location):
    with open(location_json, 'r') as f:
        data = json.load(f)

    for item in data:
        if item['location'] == location:
            return item

def image_player(filenames):
    # State variables
    current_index = 0
    play = False
    speed = 1.0

    # Image Pane
    image_pane = pn.pane.PNG(Image.open(filenames[current_index]), width=400, height=300)

    # Function to load the current image
    def load_image():
        return Image.open(filenames[current_index])

    # Function to update the image when playing
    def update_image():
        nonlocal current_index
        if play:
            current_index = (current_index + 1) % len(filenames)
            image_pane.object = load_image()
            player.period = int(1000 / speed)  # Adjust the update period based on speed

    # Control functions
    def start_stop(event=None):
        nonlocal play
        play = not play
        if play:
            player.start()
        else:
            player.stop()

    def next_image(event=None):
        nonlocal current_index
        current_index = (current_index + 1) % len(filenames)
        image_pane.object = load_image()

    def previous_image(event=None):
        nonlocal current_index
        current_index = (current_index - 1) % len(filenames)
        image_pane.object = load_image()

    def increase_speed(event=None):
        nonlocal speed
        speed = min(speed + 0.1, 5.0)

    def decrease_speed(event=None):
        nonlocal speed
        speed = max(speed - 0.1, 0.1)

    # Setting up the Panel widgets and layout
    controls = pn.Row(
        pn.widgets.Button(name="Play/Pause", width=80).on_click(start_stop),
        pn.widgets.Button(name="<<", width=50).on_click(previous_image),
        pn.widgets.Button(name=">>", width=50).on_click(next_image),
        pn.widgets.Button(name="Speed +", width=70).on_click(increase_speed),
        pn.widgets.Button(name="Speed -", width=70).on_click(decrease_speed),
        pn.widgets.StaticText(value="Speed:"),
        pn.widgets.LiteralInput(value=speed, type=float, width=50)
    )

    # Periodic callback to handle play mode updates
    player = pn.state.add_periodic_callback(update_image, period=100, start=False)

    # Panel layout with the image and controls
    return pn.Column(image_pane, controls)