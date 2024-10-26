## Filename: config.py
## Description: This file contains configuration settings for the application.

# Set initial variables to get data
sat_sel = 16
sat_domain = 'F'
sat_product = 'ABI-L2-MCMIP'
start_time = '2024-10-08 16:00'
end_time = '2024-10-08 16:10'

# Set the list of available satellite composites
# sat_composites = ['true_color_nocorr', 'true_color_reproduction_corr', 'geo_color', 'true_color', 'true_color_crefl',
#                'cimss_true_color_sunz_rayleigh', 'cimss_true_color_sunz', 'cimss_true_color', 
#                'true_color_reproduction_corr', 'true_color_reporduction_uncorr', 'true_color_reproduction']

sat_composites = ['Select an option', 'true_color_nocorr', 'cimss_true_color_sunz_rayleigh', 'cimss_true_color_sunz', 'cimss_true_color', 'true_color_reproduction_corr', 'true_color_reporduction_uncorr', 'true_color_reproduction']

# Set directory files
nc_dir = 'data/nc/'
img_dir = 'media/img/'