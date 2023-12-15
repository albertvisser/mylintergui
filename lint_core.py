"""linter starter command line version
"""
import os
import sys
import pathlib
import datetime
import subprocess
from types import SimpleNamespace

ROOT = pathlib.Path.home() / '.linters'
CMD = {
    'pylint': ('pylint', '<src>'),
    'flake8': ('python', '-m', 'flake8', '<src>')}
origpath = sys.path
sys.path.insert(0, str(pathlib.Path.home() / 'bin'))
import settings
sys.path = origpath
# do_not_lint = settings.fcgi_repos + settings.private_repos + settings.non_deploy_repos
# all_repos = settings.all_repos + settings.git_repos


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
        if not lint_them_all and name not in settings.all_repos:
            if [name] == names:
                print("Unknown project name", name)
            continue
        if name in settings.DO_NOT_LINT:  # do_not_lint:
            if [name] == names:
                print(name, "is marked as do-not-lint")
            continue
        os.chdir(os.path.join(settings.PROJECTS_BASE, name))
        args = SimpleNamespace(linter='', file=None, recursive=True)
        args.linter = 'pylint'
        Main(args)
        args.linter = 'flake8'
        Main(args)


class Main:
    """Main class for applying a linter to one or more files
    """

    def __init__(self, args, repo_only=True):
        self.linter = args.linter
        self.determine_files(repo_only)
        if args.file:
            item = pathlib.Path(args.file).resolve()
            self.lint(item, args.out)
        else:
            self.scan(pathlib.Path.cwd(), args.recursive)
        print('ready.')

    def determine_files(self, filter_repo):
        """read hg manifest to filter out files that do not need to be checked
        """
        self.files = []
        if not filter_repo:
            return
        repo_loc = pathlib.Path.cwd()
        test = repo_loc / '.hg'
        if test.exists():
            command = ['hg', 'manifest']
        else:
            test = repo_loc / '.git'
            if test.exists():
                command = ['git', 'ls-files']
        if not command:
            return
        result = subprocess.run(command, stdout=subprocess.PIPE, check=False).stdout
        for name in str(result, encoding='utf-8').split('\n'):
            self.files.append(repo_loc / name)

    def lint(self, item, out='auto'):
        """actually call the linter
        """
        command = list(CMD[self.linter])
        for ix, word in enumerate(command):
            if word == '<src>':
                command[ix] = str(item)
        if not out:
            subprocess.run(command, check=False)
            return
        if out == 'auto':
            dts = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
            # LBYL
            if item.is_relative_to(pathlib.Path.home() / 'projects'):
                out = ROOT / self.linter / '-'.join(
                    (str(item.relative_to(pathlib.Path.home() / 'projects')), dts))
            else:
                out = ROOT / self.linter / '-'.join(
                    (str(item.relative_to(pathlib.Path.home())), dts))
            # EAFP - zelfde resultaat
            # try:
            #     out = ROOT / self.linter / '-'.join(
            #         (str(item.relative_to(pathlib.Path.home() / 'projects')), dts))
            # except ValueError:
            #     out = ROOT / self.linter / '-'.join(
            #         (str(item.relative_to(pathlib.Path.home())), dts))
            if not out.parent.exists():
                out.parent.mkdir(parents=True)
        # with out.open('w') as _out:
        #     subprocess.run(command, stdout=_out)

    def scan(self, here, recursive=False):
        """apply linter to files in directory
        """
        for item in here.iterdir():
            if item.is_file() and item.suffix in ('.py', 'pyw', ''):
                if item.name.startswith('.'):              # no hidden files
                    continue
                if self.files and item not in self.files:  # ignore unselected
                    continue
                self.lint(item)
            elif item.is_dir() and recursive:
                self.scan(item, recursive)
