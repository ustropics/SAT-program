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