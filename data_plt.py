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

from satpy.writers import get_enhanced_image
from satpy.composites import DayNightCompositor

from datetime import datetime
from glob import glob

## PLOT DATA

def plt_img(df, composite_val, satellite_val, daynight_val):
    recipe = composite_translation.get(composite_val, None)
    satellite = satellite_translation.get(satellite_val, None)
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

        filename = f'{img_dir}goes_abi_{recipe}_{datetime.now().strftime("%Y%m%d%H%M")}.png'
        filename2 = f'{img_dir}goes_abi_{recipe}_cartopy_{datetime.now().strftime("%Y%m%d%H%M")}.png'
        new_scn.save_dataset(recipe, filename=filename)

        area = new_scn[recipe].attrs['area']
        dn_scn = new_scn.resample(area)
        image = get_enhanced_image(dn_scn[recipe]).data
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
        # Load the selected recipe dataset
        scn.load([recipe])

        # Resample the scene using minimum area
        new_scn = scn.resample(scn.min_area(), resampler='nearest')
        area = scn[recipe].attrs['area']
        print(area)

        # Save the regular composite dataset
        filename = f'{img_dir}goes_abi_{recipe}_{datetime.now().strftime("%Y%m%d%H%M")}.png'
        filename2 = f'{img_dir}goes_abi_{recipe}_cartopy_{datetime.now().strftime("%Y%m%d%H%M")}.png'
        new_scn.save_dataset(recipe, filename=filename)

        plt_scn = scn.resample(area)
        print("Plot scene shape: ", plt_scn[recipe].shape)
        image = get_enhanced_image(plt_scn[recipe]).data
        print("Image shape: ", image.shape)
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