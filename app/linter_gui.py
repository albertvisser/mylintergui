"""imports the gui from a toolkit-specific module
so that the starters need not know about which one is used
for switching out gui toolkits, use a conditional import (see various other of my projects)
"""
from .linter_qtgui import MainFrame
