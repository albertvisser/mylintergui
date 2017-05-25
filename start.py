import sys
import argparse
from app.linter_gui import MainFrame

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('-d', '--directory', dest='d', metavar='NAME',
    help='specify directory to check')
group.add_argument('-f', '--file', dest='f', metavar='NAME',
    help='specify file to check')
group.add_argument('-l', '--list', nargs='+', dest='l', metavar='NAME',
    help='specify list of files/directories to check')
parsed_args = parser.parse_args()
MainFrame(args=parsed_args)
## print(parsed_args)

