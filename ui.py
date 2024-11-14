## Filename: ui.py
## Description: This file builds the user interface for the application.

import panel as pn
import io
import datetime as dt
import warnings
import json
import base64
import param

from config import *
from utils import default_locations, location_data
from run import run_prg
from panel.template import DarkTheme
from panel.theme import Material
from panel.reactive import ReactiveHTML
from PIL import Image

css = """
#input {
    background-color: #343c43;
}
.bk-input:active {
    background-color: green;
}

focus {
    background-color: green !important;
    color: inherit; /* Inherit text color from the main select */
}

.bk-input {
    /* Optional customizations for the overall dropdown */
    background-color: transparent;
    border: 1px solid #ccc; /* Customize as needed */
    color: #333; /* Customize text color */
}

/* Remove the blue background when focused */
.bk-input:focus {
    outline: none;
    background-color: transparent;
}

.bk-btn-success {
    background-color: #CEB888 !important;
    color: #2C2A29;
    border: none;
    cursor: pointer;
}

.bk-btn-success:hover {
    background-color: #FFD700 !important;
    color: #2C2A29;
    border: none;
    cursor: pointer;
}

.mdc-top-app-bar {
    background-color: #782F40 !important;
}

.mdc-drawer {
}

.bk-tab.bk-active {
    color: #CEB888 !important;
    outline: none !important;
}

.bk-tab:focus {

  outline: none !important;

}

.main-content {
    background-color: #343c43 !important;
}
"""

pn.extension('terminal', console_output='disable', design='material', global_css=[':root {--design-primary-color: #782F40}'], theme='dark', raw_css=[css])
pn.config.design = Material
image_filenames = []

class Slideshow(ReactiveHTML):
    index = param.Integer(default=0)
    img_data = param.String()

    _template = """
    <div>
        <img id="slideshow_el" src="data:image/png;base64, ${img_data}" 
             style="max-width: 90vw; max-height: 800px"></img>
    </div>
    """

    def __init__(self, image_paths, player, **params):
        super().__init__(**params)
        self.player = player
        self.images = []
        
        # Load images and convert to base64
        for img_path in image_paths:
            with open(img_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode("utf-8")
                self.images.append(img_data)
        
        # Set initial image
        if self.images:
            self.img_data = self.images[self.index]
        
        # Link the player value to image changes
        self.player.param.watch(self._on_player_value_change, 'value')

    def _on_player_value_change(self, event):
        # Change the image based on the player value (time/frame)
        self.index = int(event.new) % len(self.images)  # Ensure the index loops
        self.img_data = self.images[self.index]

def build_ui():
    def pn_repr(self, include=None, exclude=None):
        pn.extension()
        return pn.viewable.Viewable._repr_mimebundle_(self, include, exclude)
    pn.layout.Panel._repr_mimebundle_ = pn_repr

    warnings.filterwarnings('ignore')

    # Headers and Labels
    tab1_col1_header = pn.widgets.StaticText(name='Quick select a product type and preset location')
    tab1_col2_header = pn.widgets.StaticText(name='Set the time range for data (times are in UTC)')
    tab2_col1_header = pn.widgets.StaticText(name='Select the projection, satellite, and domain type')
    tab2_col2_header = pn.widgets.StaticText(name='Set custom latitude and longitude extent')
    tab2_col2_header2 = pn.widgets.StaticText(name='Set the border color and width')
    tab3_col1_header = pn.widgets.StaticText(name='Select additional overlays to display')

    # Text Labels
    daynight_switch_label = pn.widgets.StaticText(value='Include Day/Night Composite')
    lat_lon_grid_label = pn.widgets.StaticText(value='Latitude/Longitude Grid')
    lat_lon_labels_label = pn.widgets.StaticText(value='Latitude/Longitude Labels')
    state_borders_label = pn.widgets.StaticText(value='State Borders')
    country_borders_label = pn.widgets.StaticText(value='Country Borders')
    water_borders_label = pn.widgets.StaticText(value='Lake/River Borders')
    county_borders_label = pn.widgets.StaticText(value='County Borders')

    # Datetime Pickers
    start_dt = pn.widgets.DatetimePicker(name='Start Date/Time', value=start_time)
    end_dt = pn.widgets.DatetimePicker(name='End Date/Time', value=end_time)

    # Dropdowns
    composite_dropdown = pn.widgets.Select(name='Satellite Composites', size=14, options=list(composite_translation.keys()), value='CIMSS True Color Sun Zenith Rayleigh', disabled_options=['---Daytime Only (Can Add Night Below)---'])
    location_dropdown = pn.widgets.Select(name='Location', options=default_locations(), value='CONUS')
    projection_dropdown = pn.widgets.Select(name='Projection', size=4, options=list(projection_translation.keys()), value='Autoselect')
    satellite_dropdown = pn.widgets.Select(name='Satellite Type', options=list(satellite_translation.keys()), value='Autoselect')
    domain_dropdown = pn.widgets.Select(name='Domain', options=['Autoselect', 'CONUS', 'Full Disk'], value='Autoselect')
    nightcomp_dropdown = pn.widgets.Select(name='Night Composite', options=['None', 'VIIRS Day/Night Band'], value='None')

    # Text Inputs
    lon1_input = pn.widgets.TextInput(name='West Longitude', value='0', width=100)
    lat1_input = pn.widgets.TextInput(name='North Latitude', value='0', width=100)
    lon2_input = pn.widgets.TextInput(name='East Longitude', value='0', width=100)
    lat2_input = pn.widgets.TextInput(name='South Latitude', value='0', width=100)
    border_width = pn.widgets.TextInput(name='Border Width', value='0.5', width=100)

    # Color Picker
    placeholder_col = pn.Column('No image available yet. Click "Run" to generate an image.')

    border_color = pn.widgets.ColorPicker(name='Border Color', value='#EB3B00', width=100)
    placeholder = pn.pane.Placeholder(placeholder_col)
    player_placeholder = pn.pane.Placeholder('')

    # Switches
    daynight_switch = pn.widgets.Switch(name='Include Day/Night Composite', value=False)
    lat_lon_grid = pn.widgets.Switch(name='Include Latitude/Longitude Grid', value=False)
    lat_lon_labels = pn.widgets.Switch(name='Include Latitude/Longitude Labels', value=False)
    state_borders = pn.widgets.Switch(name='Include State Borders', value=False)
    country_borders = pn.widgets.Switch(name='Include Country Borders', value=False)
    water_borders = pn.widgets.Switch(name='Lake/River Borders', value=False)
    county_borders = pn.widgets.Switch(name='Include County Borders', value=False, disabled=True)

    # Containers
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


    # Button
    run_btn = pn.widgets.Button(name='Run', button_type='success')

    # Define the Run Button click behavior
    def on_run_click(event):
        global image_filenames
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
        # Set projections and satellite defaults
        data = location_data(vals['location_val'])
        vals['projection_val'] = data['projection'] if vals['projection_val'] == 'Autoselect' else vals['projection_val']
        vals['satellite_val'] = data['satellite'] if vals['satellite_val'] == 'Autoselect' else vals['satellite_val']
        vals['domain_val'] = data['domain'] if vals['domain_val'] == 'Autoselect' else vals['domain_val']

        # Extents defaults
        if vals['lat1_val'] == 0 and vals['lat2_val'] == 0 and vals['lon1_val'] == 0 and vals['lon2_val'] == 0:
            vals.update({'lat1_val': data['extent'][2], 'lat2_val': data['extent'][3], 'lon1_val': data['extent'][0], 'lon2_val': data['extent'][1]})

        # Run Program
        image_filenames = run_prg(vals)

        if image_filenames:
            player = pn.widgets.Player(
                name='Player',
                start=0,
                end=len(image_filenames)-1,
                step=1,
                visible_buttons=["slower", "play", "pause", "faster"],
                show_loop_controls=False,
                scale_buttons=0.9,
                width=150,
                interval=500
            )

            slideshow = Slideshow(image_paths=image_filenames, player=player)
            
            placeholder.update(slideshow)
            player_placeholder.update(player)
        
    run_btn.on_click(on_run_click)

    player_placeholder = pn.pane.Placeholder('')

    # Layout setup
    tab1_col1 = pn.Column(player_placeholder, tab1_col2_header, start_dt, end_dt, tab1_col1_header, composite_dropdown, location_dropdown)
    tab2_col1 = pn.Column(player_placeholder, tab2_col1_header, projection_dropdown, satellite_dropdown, domain_dropdown, nightcomp_dropdown, tab2_col2_header, lat_container, lon_container, tab2_col2_header2, border_container, tab3_col1_header, lat_lon_grid_container, lat_lon_labels_container, state_borders_container, country_borders_container, water_borders_container, county_borders_container)

    action_bar = pn.Row(run_btn)

    template = pn.template.MaterialTemplate(title='SAT-Viewer', theme=DarkTheme, header=[action_bar])

    # Tabs
    tabs = pn.Tabs(('Main', pn.Row(tab1_col1)), ('Projection Settings', pn.Row(tab2_col1)), ('Utilities', ''))

    # Final layout in the template
    template.sidebar.append(tabs)
    template.main.append(pn.Column(placeholder, sizing_mode='stretch_width'))

    return template.servable()