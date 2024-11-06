## Filename: data_get.py
## Description: This file contains functions for getting data.

# Import necessary libraries, functions, and config options
from config import *
from utils import *
from goes2go import GOES

## GET DATA

def get_sat_data(start_time_val, end_time_val, satellite_val):

    satellite = satellite_translation.get(satellite_val, None)
    
    # Get the satellite product
    G = GOES(satellite=satellite, product=sat_product, domain=sat_domain)

    # Get the data file list
    df = G.df(start=start_time_val, end=end_time_val)

    # Donwload the data
    G.timerange(start=start_time_val, end=end_time_val, save_dir=nc_dir)
    
    return df