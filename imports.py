## Filename: utils.py
## Description: This file contains utility functions for the application.

from utils import install_and_import

def pip_install():
    print("Installing necessary python modules and libraries...this can take a few minutes...")
    install_and_import('goes2go')
    install_and_import('satpy')
    install_and_import('pyspectral')
    install_and_import('panel')
    install_and_import('jupyter_bokeh')
    print("Python modules and libaries installed successfully... Have fun plotting!")