## Filename: run.py
## Description: This file is for running the program.

from data_get import get_sat_data
from data_prc import prc_data
from data_plt import plt_img
from utils import create_directories

import json


def run_program(ui):
    create_directories()
    data = prc_data(ui)
    print(data)
    print(f"🌎 Beginning processing of [{data['composite_val']}] from {data['start_time_val']} to {data['end_time_val']}.")
    df = get_sat_data(data)
    print(f"🎨 Data sucessfully processed! Handing datasets off to cartopy for final output.")
    plt_img(df, data)

def run_prg(data):
    create_directories()
    df = get_sat_data(data)
    filenames = plt_img(df, data)
    return filenames


