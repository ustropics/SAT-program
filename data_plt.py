## Filename: run.py
## Description: This file is the entry point of the application.

import os
import satpy

from config import *
from data_get import get_sat_data
from pyresample import create_area_def

df = get_sat_data() # Get the satellite data

# PLot data
def plt_img():
    first_file = df.loc[0, 'file']

    nc_file = os.path.join(nc_dir, first_file) # Load nc file

    for recipe in sat_recipes:
        print(recipe)

        scn = satpy.Scene(reader='abi_l2_nc', filenames=[nc_file]) # Load the scene
        print(scn.available_composite_names()) # Print available composite names
        print(scn.available_dataset_names()) # Print available dataset names

        scn.load([recipe]) # Load the scene

        new_scn = scn.resample(scn.min_area(), resampler='nearest') # Resample the scene

        my_area = create_area_def('my_area', {'proj': 'merc', 'lon_0': -95, 'lat_0': 25, 'lat_1': 35}, 
                                  width=1000, height=1000, 
                                  area_extent=[-105, 20, -90, 40], units='degrees')

        # new_scn = new_scn.resample(my_area)

        area = scn[recipe].attrs['area'] # Get the area
        print(area) # Print the area

        new_scn.save_dataset(recipe, filename=f'{img_dir}goes_abi_{recipe}'+'_{datetime}.png'.format(datetime=scn.start_time.strftime('%Y%m%d%H%M'))) # Save the dataset

# plt_satpy_img() # Plot the satellite image