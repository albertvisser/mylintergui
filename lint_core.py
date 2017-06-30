import os
import sys
import pathlib
import datetime
import subprocess
from types import SimpleNamespace
ROOT = pathlib.Path.home() / '.linters'
CMD = {
    'pylint': ('pylint3', '<src>'),
    'flake8': ('python3', '-m', 'flake8', '<src>')
    }
origpath = sys.path
sys.path.insert(0, str(pathlib.Path.home() / 'bin'))
import settings
sys.path = origpath
do_not_lint = settings.fcgi_repos + settings.private_repos + settings.non_deploy_repos
all_repos = settings.all_repos + settings.git_repos


def lint_all(args):
    """call linters on files in selected directories

    argument: list of project names (can be empty)
    """
    names = args.project
    lint_them_all = False
    if not names:
        lint_them_all = True
        names = settings.all_repos
    for name in names:
        if not lint_them_all and name not in all_repos:
            if [name] == names:
                print("Unknown project name", name)
            continue
        if name in do_not_lint:
            if [name] == names:
                print(name, "is marked as do-not-lint")
            continue
        os.chdir(os.path.join(settings.projects_base, name))
        args = SimpleNamespace(linter='', file=None, recursive=True)
        args.linter = 'pylint'
        Main(args)
        args.linter = 'flake8'
        Main(args)


class Main():
    """Main class for applying a linter to one or more files
    """

    def __init__(self, args):
        self.linter = args.linter
        if args.file:
            item = pathlib.Path(args.file).resolve()
            self.lint(item)
        else:
            self.scan(pathlib.Path.cwd(), args.recursive)
        print('ready.')

    def lint(self, item):
        """actually call the linter
        """
        print('checking', item)
        command = [x for x in CMD[self.linter]]
        for ix, word in enumerate(command):
            if word == '<src>':
                command[ix] = str(item)
        dts = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        out = ROOT / self.linter / '-'.join(
            (str(item.relative_to(pathlib.Path.home() / 'projects')), dts))
        print('writing to', out)
        if not out.parent.exists():
            out.parent.mkdir(parents=True)
        with out.open('w') as _out:
            subprocess.run(command, stdout=_out)

    def scan(self, here, recursive=False):
        """apply linter to files in directory
        """
        for item in here.iterdir():
            if item.is_file() and item.suffix == '.py':
                self.lint(item)
            elif item.is_dir() and recursive:
                self.scan(item, recursive)