#! /usr/bin/env python3
"""\
Argument parser for GUI frontend to various static code analysis tools
"""
import argparse
from app.main import Base
from app.config import cmddict, checktypes

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('-d', '--directory', dest='d', metavar='NAME',
                   help='specify directory with files to check')
group.add_argument('-f', '--file', dest='f', metavar='NAME',
                   help='specify file to check')
group.add_argument('-l', '--list', nargs='+', dest='l', metavar='NAME',
                   help='specify list of files/directories to check')
parser.add_argument('-m', '--mode', dest='m', metavar='MODE',
                    choices=list(checktypes.keys()),
                    help='specify permissiveness of linter (%(choices)s)')
parser.add_argument('-c', '--linter', dest='c', metavar='NAME',
                    choices=list(cmddict.keys()),  # ['pylint', 'flake8'],
                    help='specify checker/linter to use (%(choices)s)')
parser.add_argument('-o', '--output-file', dest='o', metavar='NAME',
                    help='specify (single) file to send output to')
parser.add_argument('-r', '--repo-files-only', dest='r', metavar='NAME',
                    help='check only tracked files for specified repository')
parser.add_argument('-s', '--skip-screen', dest='s', action='store_true',
                    help='skip initial screen and use default options')
Base(args=parser.parse_args())
