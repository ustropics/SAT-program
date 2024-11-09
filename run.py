## Filename: run.py
## Description: This file is for running the program.

from data_get import get_sat_data
from data_prc import prc_data
from data_plt import plt_img
from utils import create_directories


def run_program(ui):
    create_directories()
    start_time_val, end_time_val, composite_val, satellite_val, daynight_val = prc_data(ui)
    print(f"🌎 Beginning processing of [{composite_val}] from {start_time_val} to {end_time_val}.")
    df = get_sat_data(start_time_val, end_time_val, satellite_val)
    print(f"🎨 Data sucessfully processed! Handing datasets off to cartopy for final output.")
    plt_img(df, composite_val, satellite_val, daynight_val)