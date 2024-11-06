## Filename: data_prc.py
## Description: This file is for processing the data.

def prc_data(ui):
    start_time_val = ui[0][0].value
    end_time_val = ui[0][1].value
    composite_val = ui[1].value
    satellite_val = ui[2].value
    daynight_val = ui[4].value

    return start_time_val, end_time_val, composite_val, satellite_val, daynight_val