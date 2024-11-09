## Filename: data_prc.py
## Description: This file is for processing the data.

def prc_data(ui):
    start_time_val = ui[0][0][1][0].value
    end_time_val = ui[0][0][1][1].value
    composite_val = ui[0][0][0][1].value
    location_val = ui[0][0][0][2].value
    projection_val = ui[0][1][0][1].value
    satellite_val = ui[0][1][0][2].value
    domain_val = ui[0][1][0][3].value


    return start_time_val, end_time_val, composite_val, satellite_val, daynight_val