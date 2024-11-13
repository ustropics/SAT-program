import panel as pn
import datetime as dt
import warnings
import json

from config import *
from utils import default_locations, location_data
from run import run_prg

def colab_ui():
    def pn_repr(self, include=None, exclude=None):
        pn.extension()
        return pn.viewable.Viewable._repr_mimebundle_(self, include, exclude)
    pn.layout.Panel._repr_mimebundle_ = pn_repr

    warnings.filterwarnings('ignore')

    # Create headers
    tab1_col1_header = pn.widgets.StaticText(name='Quick select a product type and preset location')
    tab1_col2_header = pn.widgets.StaticText(name='Set the time range for data (times are in UTC)')
    tab2_col1_header = pn.widgets.StaticText(name='Select the projection, satellite, and domain type')
    tab2_col2_header = pn.widgets.StaticText(name='Set custom latitude and longitude extent')
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
    composite_dropdown = pn.widgets.Select(name='Satellite Composites', size=14, options=list(composite_translation.keys()), value='CIMSS True Color Sun Zenith Rayleigh', disabled_options=['---Daytime Only (Can Add Night Below)---'])
    location_dropdown = pn.widgets.Select(name='Location', options=default_locations(), value='CONUS')
    projection_dropdown = pn.widgets.Select(name='Projection', size=10, options=list(projection_translation.keys()), value='Autoselect')
    satellite_dropdown = pn.widgets.Select(name='Satellite Type', options=list(satellite_translation.keys()), value='Autoselect')
    domain_dropdown = pn.widgets.Select(name='Domain', options=['Autoselect','CONUS', 'Full Disk'], value='Autoselect')
    nightcomp_dropdown = pn.widgets.Select(name='Night Composite', options=['None', 'VIIRS Day/Night Band'], value='None')

    # Create input boxes
    lon1_input = pn.widgets.TextInput(name='West Longitude', value='0', width=100)
    lat1_input = pn.widgets.TextInput(name='North Latitude', value='0', width=100)
    lon2_input = pn.widgets.TextInput(name='East Longitude', value='0', width=100)
    lat2_input = pn.widgets.TextInput(name='South Latitude', value='0', width=100)
    border_width = pn.widgets.TextInput(name='Border Width', value='0.5', width=100)

    # Create special widgets
    border_color = pn.widgets.ColorPicker(name='Border Color', value='#EB3B00', width=100)

    # Create switches
    daynight_switch = pn.widgets.Switch(name='Include Day/Night Composite', value=False)
    lat_lon_grid = pn.widgets.Switch(name='Include Latitude/Longitude Grid', value=False)
    lat_lon_labels = pn.widgets.Switch(name='Include Latitude/Longitude Labels', value=False)
    state_borders = pn.widgets.Switch(name='Include State Borders', value=False)
    country_borders = pn.widgets.Switch(name='Include Country Borders', value=False)
    water_borders = pn.widgets.Switch(name='Lake/River Borders', value=False)
    county_borders = pn.widgets.Switch(name='Include County Borders', value=False, disabled=True)

    # Create buttons
    run_btn = pn.widgets.Button(name='Run', button_type='primary')
    gif_btn = pn.widgets.Button(name='Create GIF', button_type='primary')

    def on_run_click(event):
        vals = {
            'composite_val': composite_dropdown.value,
            'location_val': location_dropdown.value,
            'start_time_val': start_dt.value.isoformat(),
            'end_time_val': end_dt.value.isoformat(),
            'projection_val': projection_dropdown.value,
            'satellite_val': satellite_dropdown.value,
            'domain_val': domain_dropdown.value,
            'nightcomp_val': nightcomp_dropdown.value,
            'lat1_val': float(lat1_input.value),
            'lat2_val': float(lat2_input.value),
            'lon1_val': float(lon1_input.value),
            'lon2_val': float(lon2_input.value),
            'border_color_val': border_color.value,
            'border_width_val': border_width.value,
            'daynight_switch_val': daynight_switch.value,
            'lat_lon_grid_val': lat_lon_grid.value,
            'lat_lon_labels_val': lat_lon_labels.value,
            'state_borders_val': state_borders.value,
            'country_borders_val': country_borders.value,
            'water_borders_val': water_borders.value,
            'county_borders_val': county_borders.value
        }

        lat1_val = vals['lat1_val']
        lat2_val = vals['lat2_val']
        lon1_val = vals['lon1_val']
        lon2_val = vals['lon2_val']

        data = location_data(vals['location_val'])

        if vals['projection_val'] == 'Autoselect':
            projection_val = data['projection']
        else:
            projection_val = vals['projection_val']

        if vals['satellite_val'] == 'Autoselect':
            satellite_val = data['satellite']
        else:
            satellite_val = vals['satellite_val']

        if vals['domain_val'] == 'Autoselect':
            domain_val = data['domain']
        else:
            domain_val = vals['domain_val']     

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
            'start_time_val': vals['start_time_val'],
            'end_time_val': vals['end_time_val'],
            'composite_val': vals['composite_val'],
            'location_val': vals['location_val'],
            'projection_val': projection_val,
            'satellite_val': satellite_val,
            'domain_val': domain_val,
            'daynight_val': vals['daynight_switch_val'],
            'lat1_val': lat1_val,
            'lat2_val': lat2_val,
            'lon1_val': lon1_val,
            'lon2_val': lon2_val,
            'border_color_val': vals['border_color_val'],
            'border_width_val': vals['border_width_val'],
            'lat_lon_grid_val': vals['lat_lon_grid_val'],
            'lat_lon_labels_val': vals['lat_lon_labels_val'],
            'state_borders_val': vals['state_borders_val'],
            'country_borders_val': vals['country_borders_val'],
            'water_borders_val': vals['water_borders_val'],
            'county_borders_val': vals['county_borders_val']
        }

        # Save user_inputs to a json file
        run_prg(data_dict)
    

    run_btn.on_click(on_run_click)

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
    tab1_col1 = pn.Column(tab1_col1_header, composite_dropdown, location_dropdown, run_btn)
    tab1_col2 = pn.Column(tab1_col2_header, start_dt, end_dt)
    tab2_col1 = pn.Column(tab2_col1_header, projection_dropdown, satellite_dropdown, domain_dropdown, nightcomp_dropdown)
    tab2_col2 = pn.Column(tab2_col2_header, lat_container, lon_container, tab2_col2_header2, border_container)
    tab2_col3 = pn.Column(tab3_col1_header, lat_lon_grid_container, lat_lon_labels_container, state_borders_container, country_borders_container, water_borders_container, county_borders_container)

    tab1 = pn.Row(tab1_col1, tab1_col2)
    tab2 = pn.Row(tab2_col1, tab2_col2, tab2_col3)

    tabs = pn.Tabs(('Main', tab1), ('Projection Settings', tab2), 'Utilities')

    # Return both widgets in a column layout
    return pn.Column(tabs, height=500)