# -*- coding: utf-8 -*-
"""imports the gui from a toolkit-specific module
so that the starters need not know about which one is used
"""
## from .linter_ppgui import MainFrame
## from .linter_tkgui import MainFrame
## from .linter_tk3gui import MainFrame
## from .linter_wxgui import MainFrame
## from .linter_qt4gui import MainFrame
from .linter_qtgui import MainFrame
MainFrame = MainFrame


def test():
    "test routine"
    MainFrame()

if __name__ == "__main__":
    test()
