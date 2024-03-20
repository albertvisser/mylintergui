"""configuration for lintergui
"""
import enum


cmddict = {'flake8': {'command': ('python', '-m', 'flake8', '{}')},
           'pylint': {'command': ('pylint', '--reports=no', '{}')},
           'ruff': {'command': ('ruff', 'check', '{}')}}
checktypes = {'testing': {'pylint': ['--rcfile', '/home/albert/.pylintrc-testing'],
                             'flake8': ['--config=/home/albert/.config/flake8-testing'],
                             'ruff': ['--config=/home/albert/.ruff-testing.toml']},
              'permissive': {'pylint': ['--rcfile', '/home/albert/.pylintrc-lean'],
                             'flake8': ['--config=/home/albert/.config/flake8-lean'],
                             'ruff': ['--config=/home/albert/.ruff-lean.toml']},
              'moderate': {'pylint': ['--rcfile', '/home/albert/.pylintrc-regular'],
                          'flake8': ['--config=/home/albert/.config/flake8-regular'],
                          'ruff': ['--config=/home/albert/.config/ruff/.ruff.toml']},
              'anal': {'pylint': ['--rcfile', '/home/albert/.pylintrc-strict'],
                       'flake8': ['--config=/home/albert/.config/flake8-strict'],
                       'ruff': ['--config=/home/albert/.ruff-strict.toml']}}
default_option = 1


class Mode(enum.Enum):
    """execution modes
    """
    single = 'f'
    standard = 'd'
    multi = 'l'
