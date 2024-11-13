## Filename: data_plt.py
## Description: This file is for plotting the data.

import os
import satpy
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import hashlib

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
from acgc import figstyle
from glob import glob

from data_get import get_sat_data

## PLOT DATA

def plt_img(df, data):
    """
    This function plots the satellite image.
    """
    
    recipe = composite_translation.get(data['composite_val'], None)
    projection = projection_translation.get(data['projection_val'], None)

    filename_array = []

    for row in df.itertuples(index=False):
        nc_file = os.path.join(nc_dir, row.file)  # Load nc file

        concatenated_values = ''.join(str(value) for value in data.values()) + row.file
        hash_object = hashlib.sha256(concatenated_values.encode())
        hash_key = hash_object.hexdigest()

        filename = f'{img_dir}{hash_key}.webp'
        filename_array.append(filename)

        scn = satpy.Scene(reader='abi_l2_nc', filenames=[nc_file])  # Load the scene
        # print("scn attrs: ", scn.attrs)
        
        # Print list of bands and scenes available to load
        # print(scn.available_dataset_names())
        # print(scn.available_composite_names())

        lat_min, lat_max = data['lat1_val'], data['lat2_val']  # Latitude range for Florida
        lon_min, lon_max = data['lon1_val'], data['lon2_val']  # Longitude range for Florida

        # Define a custom area with Lambert Conformal projection and geographic bounds
        proj_dict = {
            'proj': projection,
            'lat_0': 0.5 * (lat_min + lat_max),  # Central latitude
            'lon_0': 0.5 * (lon_min + lon_max),  # Central longitude
            'lat_1': lat_min,     # First standard parallel
            'lat_2': lat_max,     # Second standard parallel
            'ellps': 'GRS80'
        }

        # Create the area definition in Satpy using latitude and longitude bounds

        area_def = create_area_def(
            'composite_area',  # Name of the area definition
            proj_dict,
            units='degrees',
            width=5420, 
            height=5420,
            area_extent=[lon_min, lat_min, lon_max, lat_max]
        )

        # print("Area Definition: ", area_def)

        if data['nightcomp_val'] == True:
            scn.load([recipe, 'ir108_3d'])
            compositor = DayNightCompositor("dnc", lim_low=85., lim_high=88., day_night="day_night")
            composite = compositor([scn[recipe], scn['ir108_3d']])
            new_scn = scn.resample(scn.min_area(), resampler='nearest')
            new_scn[recipe] = composite  # Assign the composite to the resampled scene
        else:
            scn.load([recipe])
            new_scn = scn.resample(area_def, resampler='nearest', cache_dir='cache/')
        
        area = new_scn[recipe].attrs['area']
        
        plt_scn = scn.resample(area)

        # print("Area CRS: ", plt_scn[recipe].attrs['area'])
        # print("scn attrs: ", plt_scn[recipe].attrs)
        image = get_enhanced_image(plt_scn[recipe]).data
        # print("image attributes: ", image.attrs)
        crs = plt_scn[recipe].attrs['area'].to_cartopy_crs()
        
        fig = plt.figure(figsize=(15,15))
        ax = fig.add_subplot(1, 1, 1, projection=crs)


        ax.add_feature(cfeature.COASTLINE, edgecolor=data['border_color_val'], linewidth=float(data['border_width_val']))
        ax.add_feature(cfeature.BORDERS, edgecolor=data['border_color_val'], linewidth=float(data['border_width_val']))
        ax.add_feature(cfeature.STATES, edgecolor=data['border_color_val'], linewidth=float(data['border_width_val']))
        ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
        
        if len(plt_scn[recipe].shape) > 2:
            image.plot.imshow(vmin=0, vmax=1, add_colorbar=False, rgb='bands', ax=ax)
            ax.set_title(f"Composite: {data['composite_val']} | Projection: {data['projection_val']} | Area: {data['location_val']}", fontsize=14, zorder=100)
        else:  # Single-band grayscale case
            image = np.squeeze(image)
            image.plot.imshow(vmin=0, vmax=1, add_colorbar=False, ax=ax)

        plt.savefig(filename, dpi=500, bbox_inches='tight')
        plt.close()

    return filename_array


# plt_satpy_img() # Plot the satellite image