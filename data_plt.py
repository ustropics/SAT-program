## Filename: data_plt.py
## Description: This file is for plotting the data.

import os
import satpy
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np

from config import *
from utils import *

from data_get import get_sat_data
from data_prc import prc_data
from pyresample import create_area_def
from pyproj import CRS

from satpy.writers import get_enhanced_image
from satpy.composites import DayNightCompositor
from pyresample import AreaDefinition

from datetime import datetime
from glob import glob

## PLOT DATA

def plt_img(df, composite_val, satellite_val, daynight_val):
    """
    This function plots the satellite image.
    """
    
    recipe = composite_translation.get(composite_val, None)
    satellite = satellite_translation.get(satellite_val, None)

    filename = f'{img_dir}goes_abi_{recipe}_{datetime.now().strftime("%Y%m%d%H%M")}.png'
    filename2 = f'{img_dir}goes_abi_{recipe}_cartopy_{datetime.now().strftime("%Y%m%d%H%M")}.png'


    
    first_file = df.loc[0, 'file']

    nc_file = os.path.join(nc_dir, first_file)  # Load nc file

    scn = satpy.Scene(reader='abi_l2_nc', filenames=[nc_file])  # Load the scene
    
    # Print list of bands and scenes available to load
    # print(scn.available_dataset_names())
    # print(scn.available_composite_names())

    if daynight_val == True:
        # Load the required datasets
        scn.load([recipe, 'ir108_3d'])

        # Create the day/night composite
        compositor = DayNightCompositor("dnc", lim_low=85., lim_high=88., day_night="day_night")
        composite = compositor([scn[recipe], scn['ir108_3d']])
        
        # Resample using the original Scene object
        new_scn = scn.resample(scn.min_area(), resampler='nearest')
        new_scn[recipe] = composite  # Assign the composite to the resampled scene
        new_scn.save_dataset(recipe, filename=filename)

        area = new_scn[recipe].attrs['area']
        dn_scn = new_scn.resample(area)
        # image = get_enhanced_image(dn_scn[recipe]).data
        crs = dn_scn[recipe].attrs['area'].to_cartopy_crs()

        fig = plt.figure(figsize=(15,15))
        ax = fig.add_subplot(1, 1, 1, projection=crs)
        ax.coastlines(resolution="10m", color="white", linewidth=0.8)

        if len(dn_scn[recipe].shape) > 2:
            image.plot.imshow(vmin=0, vmax=1, add_colorbar=False, rgb='bands', ax=ax)
        else:
            image = np.squeeze(image)
            image[0].plot.imshow(vmin=0, vmax=1, cmap='Greys_r', add_colorbar=False, ax=ax)

        plt.savefig(filename2, dpi=500, bbox_inches='tight')
        plt.close()
        
    else:

        # Define the desired lat/lon bounding box for Florida
        lat_min, lat_max = 24.396308, 31.000968  # Latitude range for Florida
        lon_min, lon_max = -87.634918, -78.031362  # Longitude range for Florida

        # Define a custom area with Lambert Conformal projection and geographic bounds
        proj_dict = {
            'proj': 'aea',
            'lat_0': 0.5 * (lat_min + lat_max),  # Central latitude, roughly the center of Florida
            'lon_0': 0.5 * (lon_min + lon_max),  # Central longitude, roughly the center of Florida
            'lat_1': lat_min,     # First standard parallel
            'lat_2': lat_max,     # Second standard parallel
            'ellps': 'GRS80'
        }

        # Create the area definition in Satpy using latitude and longitude bounds
        area_def = create_area_def(
            'albers_equal_area',
            proj_dict,
            units='degrees',
            width=5240,  # Approximate width based on resolution; adjust as needed
            height=5240, # Approximate height based on resolution; adjust as needed
            area_extent=[lon_min, lat_min, lon_max, lat_max]
        )
        
        # Load the selected recipe dataset
        scn.load([recipe])

        new_scn = scn.resample(area_def, resampler='nearest')

        # Resample the scene using minimum area
        # new_scn = scn.resample(scn.min_area(), resampler='nearest')
        # new_scn.save_dataset(recipe, filename=filename)
        
        area = new_scn[recipe].attrs['area']
        print(area)
        
        plt_scn = scn.resample(area)
        image = get_enhanced_image(plt_scn[recipe]).data
        crs = plt_scn[recipe].attrs['area'].to_cartopy_crs()

        fig = plt.figure(figsize=(20,20))
        ax = fig.add_subplot(1, 1, 1, projection=crs)
        ax.coastlines(resolution="10m", color="white")

        if len(plt_scn[recipe].shape) > 2:
            image.plot.imshow(vmin=0, vmax=1, add_colorbar=False, rgb='bands', ax=ax)
        else:  # Single-band grayscale case
            image = np.squeeze(image)
            image.plot.imshow(vmin=0, vmax=1, add_colorbar=False, ax=ax)

        plt.savefig(filename2, dpi=500, bbox_inches='tight')
        plt.close()

# plt_satpy_img() # Plot the satellite image