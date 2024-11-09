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

    # Create headers
    tab1_col1_header = pn.widgets.StaticText(name='Quick select a product type and preset location')
    tab1_col2_header = pn.widgets.StaticText(name='Set the time range for data (times are in UTC)')
    tab2_col1_header = pn.widgets.StaticText(name='Select the projection, satellite, and domain type')
    tab2_col2_header = pn.widgets.StaticText(name='Set custom latitude and longitude extent box')
    tab2_col2_header2 = pn.widgets.StaticText(name='Set the border color and width')
    tab3_col1_header = pn.widgets.StaticText(name='Select additional overlays to display')

    # Create text labels
    daynight_switch_label = pn.widgets.StaticText(value='Include Day/Night Composite')
    lat_lon_grid_label = pn.widgets.StaticText(value='Latitude/Longitude Grid')
    lat_lon_labels_label = pn.widgets.StaticText(value='Latitude/Longitude Labels')
    state_borders_label = pn.widgets.StaticText(value='State Borders')
    country_borders_label = pn.widgets.StaticText(value='Country Borders')
    water_borders_label = pn.widgets.StaticText(value='Lake/River Borders')
    county_borders_label = pn.widgets.StaticText(value='County Borders')

    # Create the datetime picker widgets
    start_dt = pn.widgets.DatetimePicker(name='Start Date/Time', value=start_time)
    end_dt = pn.widgets.DatetimePicker(name='End Date/Time', value=end_time)

    # Create droddown boxes
    composite_dropdown = pn.widgets.Select(name='Satellite Composites', size=14, options=sat_composites, value='CIMSS True Color Sun Zenith Rayleigh', disabled_options=['---Daytime Only (Can Add Night Below)---', '---Day and Night Composites---'])
    location_dropdown = pn.widgets.Select(name='Location', options=['location1', 'location2'], value='location2')
    projection_dropdown = pn.widgets.Select(name='Projection', size=10, options=['Orthographic', 'Mercator', 'Mollweide', 'Robinson', 'Geostationary'], value='Orthographic')
    satellite_dropdown = pn.widgets.Select(name='Satellite Type', options=sat_types, value='GOES-EAST (16)')
    domain_dropdown = pn.widgets.Select(name='Domain', options=['CONUS', 'Full Disk'], value='CONUS')
    nightcomp_dropdown = pn.widgets.Select(name='Night Composite', options=['None', 'VIIRS Day/Night Band'], value='None')

    # Create input boxes
    lon1_input = pn.widgets.TextInput(name='West Longitude', value='0', width=150)
    lat1_input = pn.widgets.TextInput(name='North Latitude', value='0', width=150)
    lon2_input = pn.widgets.TextInput(name='East Longitude', value='0', width=150)
    lat2_input = pn.widgets.TextInput(name='South Latitude', value='0', width=150)
    border_width = pn.widgets.TextInput(name='Border Width', value='0.5', width=150)

    # Create special widgets
    border_color = pn.widgets.ColorPicker(name='Border Color', value='orange', width=150)

    # Create switches
    daynight_switch = pn.widgets.Switch(name='Include Day/Night Composite', value=False)
    lat_lon_grid = pn.widgets.Switch(name='Include Latitude/Longitude Grid', value=False)
    lat_lon_labels = pn.widgets.Switch(name='Include Latitude/Longitude Labels', value=False)
    state_borders = pn.widgets.Switch(name='Include State Borders', value=False)
    country_borders = pn.widgets.Switch(name='Include Country Borders', value=False)
    water_borders = pn.widgets.Switch(name='Lake/River Borders', value=False)
    county_borders = pn.widgets.Switch(name='Include County Borders', value=False, disabled=True)


    # Create containers
    lat_container = pn.Row(lat1_input, lat2_input)
    lon_container = pn.Row(lon1_input, lon2_input)
    border_container = pn.Row(border_color, border_width)
    daynight_switch_container = pn.Row(daynight_switch, daynight_switch_label)
    lat_lon_grid_container = pn.Row(lat_lon_grid, lat_lon_grid_label)
    lat_lon_labels_container = pn.Row(lat_lon_labels, lat_lon_labels_label)
    state_borders_container = pn.Row(state_borders, state_borders_label)
    country_borders_container = pn.Row(country_borders, country_borders_label)
    water_borders_container = pn.Row(water_borders, water_borders_label)
    county_borders_container = pn.Row(county_borders, county_borders_label)


    # Create the columns for the tabs
    tab1_col1 = pn.Column(tab1_col1_header, composite_dropdown, location_dropdown)
    tab1_col2 = pn.Column(tab1_col2_header, start_dt, end_dt)
    tab2_col1 = pn.Column(tab2_col1_header, projection_dropdown, satellite_dropdown, domain_dropdown, nightcomp_dropdown)
    tab2_col2 = pn.Column(tab2_col2_header, lat_container, lon_container, tab2_col2_header2, border_container)
    tab2_col3 = pn.Column(tab3_col1_header, lat_lon_grid_container, lat_lon_labels_container, state_borders_container, country_borders_container, water_borders_container, county_borders_container)

    tab1 = pn.Row(tab1_col1, tab1_col2)
    tab2 = pn.Row(tab2_col1, tab2_col2, tab2_col3)

    tabs = pn.Tabs(('Main',tab1),('Projection Settings', tab2), 'Utilities')


    # Return both widgets in a column layout
    return pn.Column(tabs, height=440)