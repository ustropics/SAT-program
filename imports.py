## Filename: utils.py
## Description: This file contains utility functions for the application.

from utils import *

def pip_install():
    print("Installing necessary python modules and libraries...this can take a few minutes...")
    install_and_import('goes2go')
    install_and_import('satpy')
    install_and_import('pyspectral')
    pip_install('panel')
    print("Python modules and libaries installed successfully... Have fun plotting!")