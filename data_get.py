## Filename: data_get.py
## Description: This file contains functions for getting data.

# Import necessary libraries, functions, and config options
from config import *
from goes2go import GOES

## GET DATA

def get_sat_data():
    
    # Get the satellite product
    G = GOES(satellite=sat_sel, product=sat_product, domain=sat_domain)

    # Get the data file list
    df = G.df(start=start_time, end=end_time)

    # Donwload the data
    G.timerange(start=start_time, end=end_time, save_dir=nc_dir)
    
    return df