## Filename: config.py
## Description: This file contains configuration settings for the application.

import datetime as dt

# Set initial variables to get data
sat_sel = 16
sat_domain = 'C'
sat_product = 'ABI-L2-MCMIP'
end_time = dt.datetime.utcnow()
start_time = end_time - dt.timedelta(minutes=30)

# Set the list of available satellite composites
# sat_composites = ['true_color_nocorr', 'true_color_reproduction_corr', 'geo_color', 'true_color', 'true_color_crefl',
#                'cimss_true_color_sunz_rayleigh', 'cimss_true_color_sunz', 'cimss_true_color', 
#                'true_color_reproduction_corr', 'true_color_reporduction_uncorr', 'true_color_reproduction']

sat_composites = ['---Daytime Only (Can Add Night Below)---', 'True Color No Correction', 'CIMSS True Color Sun Zenith Rayleigh', 'CIMSS True Color Sun Zenith', 'CIMSS True Color', 'True Color Reproduction Corrected', 'True Color Reproduction Uncorrected', 'True Color Reproduction','---Day and Night Composites---','Night IR with High-resolution']
sat_types = ['GOES-EAST (16)', 'GOES-WEST (17)', 'GOES-WEST (18)']

# Set directory files
nc_dir = 'data/nc/'
img_dir = 'media/img/'