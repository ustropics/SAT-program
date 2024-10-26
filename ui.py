## Filename: ui.py
## Description: This file builds the user interface for the application.

import panel as pn
import datetime as dt
import warnings

pn.extension()

def build_ui():
    def pn_repr(self, include=None, exclude=None):
        pn.extension()
        return pn.viewable.Viewable._repr_mimebundle_(self, include, exclude)
    pn.layout.Panel._repr_mimebundle_ = pn_repr

    warnings.filterwarnings('ignore')

    # CSS styling for widget labels (adjust color to fit your theme)
    css = """
    .custom-widget .bk-input-group label {
        color: white;  /* Change this color to suit your theme */
    }
    """

    # Apply the CSS to the layout
    pn.config.raw_css.append(css)

    # Create the datetime picker widget with the custom class
    datetime_picker = pn.widgets.DatetimePicker(
        name='Datetime Picker', value=dt.datetime(2021, 3, 2, 12, 10),
        css_classes=['custom-widget']
    )

    # Create a dropdown box (Select widget) with the custom class
    dropdown = pn.widgets.Select(
        name='Options', options=['Option 1', 'Option 2', 'Option 3'],
        value='Option 1', css_classes=['custom-widget']
    )

    # Return both widgets in a column layout
    return pn.Column(datetime_picker, dropdown, height=400)