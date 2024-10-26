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
    datetime_picker = pn.widgets.DatetimePicker(
        name='Start Date/Time', value=dt.datetime(2021, 3, 2, 12, 10)
    )

    # Create a dropdown box (Select widget) with some options
    dropdown = pn.widgets.Select(name='Satellite Composites', options=sat_composites, value='Select an option')

    # Return both widgets in a column layout
    return pn.Column(datetime_picker, dropdown, height=400)