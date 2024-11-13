## Filename: data_prc.py
## Description: This file is for processing the data.

from config import *
from utils import *

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

    data = location_data(location_val)

    if projection_val == 'Autoselect':
        projection_val = data['projection']

    if satellite_val == 'Autoselect':
        satellite_val = data['satellite']

    if domain_val == 'Autoselect':
        domain_val = data['domain']      

    if float(lat1_val) == 0 and float(lat2_val) == 0 and float(lon1_val) == 0 and float(lon2_val) == 0:
        lat1_val = data['extent'][2]
        lat2_val = data['extent'][3]
        lon1_val = data['extent'][0]
        lon2_val = data['extent'][1]
    else:
        lat1_val = float(lat1_val)
        lat2_val = float(lat2_val)
        lon1_val = float(lon1_val)
        lon2_val = float(lon2_val)

    data_dict = {
        'start_time_val': start_time_val,
        'end_time_val': end_time_val,
        'composite_val': composite_val,
        'location_val': location_val,
        'projection_val': projection_val,
        'satellite_val': satellite_val,
        'domain_val': domain_val,
        'daynight_val': daynight_val,
        'lat1_val': lat1_val,
        'lat2_val': lat2_val,
        'lon1_val': lon1_val,
        'lon2_val': lon2_val,
        'border_color_val': border_color_val,
        'border_width_val': border_width_val,
        'latlon_grid_val': latlon_grid_val,
        'latlon_labels_val': latlon_labels_val,
        'state_borders_val': state_borders_val,
        'country_borders_val': country_borders_val,
        'water_borders_val': water_borders_val,
        'county_borders_val': county_borders_val
    }
    
    return data_dict