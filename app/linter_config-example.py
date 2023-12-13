"""example configuration for lintergui
"""
import collections

cmddict = collections.OrderedDict([('flake8', {'command': ('python3', '-m', 'flake8', '{}')}),
                                   ('pylint', {'command': ('pylint3', '{}')}), ])

checktypes = {'permissive': {'pylint': ['--rcfile', '/home/<user>/.pylintrc-lean'],
                             'flake8': ['--config=/home/<user>/.config/flake8-lean']},
              'moderate': {'pylint': [], 'flake8': []},
              'anal': {'pylint': ['--rcfile', '/home/<user>/.pylintrc-strict'],
                       'flake8': ['--config=/home/<user>/.config/flake8-strict']}
              }
default_option = 1
