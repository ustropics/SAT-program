## Filename: data_get.py
## Description: This file contains functions for getting data.

# Import necessary libraries, functions, and config options
from config import *
from utils import *
from goes2go import GOES

from datetime import datetime, timedelta
import pandas as pd

## GET DATA

def get_sat_data(data):
    
    current_time = datetime.now()

    if current_time.minute < 5:
        start_time = pd.to_datetime(data['start_time_val']) - timedelta(minutes=10)
        end_time = pd.to_datetime(data['end_time_val']) - timedelta(minutes=10)
        
        print("start time: ", start_time)
        print("end time: ", end_time)
    else:
        start_time = data['start_time_val']
        end_time = data['end_time_val']

    G = GOES(satellite=data['satellite_val'], product='ABI-L2-MCMIP', domain=data['domain_val'])

    df = G.df(start=start_time, end=end_time)
    G.timerange(start=start_time, end=end_time, save_dir=nc_dir)

    
    return df