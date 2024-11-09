## Filename: ui.py
## Description: This file builds the user interface for the application.

import panel as pn
import datetime as dt
import warnings

from config import *

pn.extension(theme='dark')

def build_ui():
    def pn_repr(self, include=None, exclude=None):
        pn.extension()
        return pn.viewable.Viewable._repr_mimebundle_(self, include, exclude)
    pn.layout.Panel._repr_mimebundle_ = pn_repr

    warnings.filterwarnings('ignore')

    # Create the datetime picker widget
    start_dt = pn.widgets.DatetimePicker(
        name='Start Date/Time', value=start_time
    )

    end_dt = pn.widgets.DatetimePicker(
        name='End Date/Time', value=end_time
    )

    time_row = pn.Row(start_dt, end_dt)

    daynight_switch_text = pn.widgets.StaticText(value='Include Day/Night Composite')

    # lat_lon_array = pn.widgets.ArrayInput(name='Latitude and Longitude Array Input', value='[0, 0, 0, 0]')

    # Create a dropdown box (Select widget) with some options
    composite_dropdown = pn.widgets.Select(name='Satellite Composites', options=sat_composites, value='CIMSS True Color Sun Zenith Rayleigh', size=8, disabled_options=['---Daytime Only (Can Add Night Below)---', '---Day and Night Composites---'])
    satellite_dropdown = pn.widgets.Select(name='Satellite Type', options=sat_types, value='GOES-EAST (16)')
    daynight_switch = pn.widgets.Switch(name='Include Day/Night Composite', value=False)


    # Return both widgets in a column layout
    return pn.Column(time_row, composite_dropdown, satellite_dropdown, daynight_switch_text, daynight_switch, height=400)