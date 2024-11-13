## Filename: config.py
## Description: This file contains configuration settings for the application.

import datetime as dt

# Set initial variables to get data
sat_product = 'ABI-L2-MCMIP'
end_time = dt.datetime.utcnow()
start_time = end_time - dt.timedelta(minutes=20)

nc_dir = 'data/nc/'
img_dir = 'media/img/'
location_json = 'static/location_data.json'

composite_translation = {
    '---Daytime Only (Can Add Night Below)---': '---Daytime Only (Can Add Night Below)---',
    'True Color No Correction': 'true_color_nocorr',
    'CIMSS True Color Sun Zenith Rayleigh': 'cimss_true_color_sunz_rayleigh',
    'CIMSS True Color Sun Zenith': 'cimss_true_color_sunz',
    'CIMSS True Color': 'cimss_true_color',
    'True Color Reproduction Corrected': 'true_color_reproduction_corr',
    'True Color Reproduction Uncorrected': 'true_color_reporduction_uncorr',
    'True Color Reproduction': 'true_color_reproduction'
}

projection_translation = {
    'Autoselect': 'Autoselect',
    'Albers Equal Area': 'aea',
    'Azimuthal Equidistant': 'aeqd',
    'Equal Area Cylindrical': 'cea',
    'Lambert Azimuthal Equal Area': 'laea',
    'Lambert Conformal Conic': 'lcc',
    'Transverse Mercator': 'tmerc'
}

satellite_translation = {
    'Autoselect': 'Autoselect',
    'GOES-EAST (16)': 16,
    'GOES-WEST (17)': 17,
    'GOES-WEST (18)': 18
}

domain_translation = {
    'Autoselect': 'Autoselect',
    'CONUS': 'CONUS',
    'Full Disk': 'Full Disk'
}
