## Filename: data_prc.py
## Description: This file is for processing the data.

def prc_data(ui):
    start_time_val = ui[0][0][1][1].value
    end_time_val = ui[0][0][1][2].value
    composite_val = ui[0][0][0][1].value
    location_val = ui[0][0][0][2].value
    projection_val = ui[0][1][0][1].value
    satellite_val = ui[0][1][0][2].value
    domain_val = ui[0][1][0][3].value
    daynight_val = ui[0][1][0][4].value
    lat1_val = ui[0][1][1][1][0].value
    lat2_val = ui[0][1][1][1][1].value
    lon1_val = ui[0][1][1][2][0].value
    lon2_val = ui[0][1][1][2][1].value
    border_color_val = ui[0][1][1][4][0].value
    border_width_val = ui[0][1][1][4][1].value
    latlon_grid_val = ui[0][1][2][1][0].value
    latlon_labels_val = ui[0][1][2][2][0].value
    state_borders_val = ui[0][1][2][3][0].value
    country_borders_val = ui[0][1][2][4][0].value
    water_borders_val = ui[0][1][2][5][0].value
    county_borders_val = ui[0][1][2][6][0].value
    


    return start_time_val, end_time_val, composite_val, satellite_val, daynight_val