## Filename: ui.py
## Description: This file builds the user interface for the application.

import panel as pn
import datetime as dt
import warnings

def build_ui():
    pn.extension()

    def pn_repr(self, include=None, exclude=None):
        pn.extension()
        return pn.viewable.Viewable._repr_mimebundle_(self, include, exclude)
    pn.layout.Panel._repr_mimebundle_ = pn_repr

    warnings.filterwarnings('ignore')

    datetime_picker = pn.widgets.DatetimePicker(
        name='Datetime Picker', value=dt.datetime(2021, 3, 2, 12, 10)
    )

    pn.Column(datetime_picker, height=400)