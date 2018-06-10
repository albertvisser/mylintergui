"""example configuration for lintergui
"""
import collections

cmddict = collections.OrderedDict([
    ('pylint', {'command': ('pylint3', '{}')}),
    ('flake8', {'command': ('python3', '-m', 'flake8', '{}')}), ])

checktypes = {'permissive': {'pylint': ['--rcfile', '/home/<user>/.pylintrc-lean'],
                             'flake8': ['--config=/home/<user>/.config/flake8-lean']},
              'anal': {'pylint': ['--rcfile', '/home/<user>/.pylintrc-strict'],
                       'flake8': ['--config=/home/<user>/.config/flake8-strict']},
              'default': {'pylint': [], 'flake8': []}}
