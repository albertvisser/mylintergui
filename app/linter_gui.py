"""imports the gui from a toolkit-specific module
so that the starters need not know about which one is used
"""
from .linter_qtgui import MainFrame
MainFrame = MainFrame


def test():
    "test routine"
    MainFrame()

if __name__ == "__main__":
    test()
