"""Uitvoeren van de find/replace actie

de uitvoering wordt gestuurd door in een dictionary verzamelde parameters
"""
import os
import pathlib
import subprocess
from .config import cmddict, checktypes


class Linter:
    """interpreteren van de parameters en uitvoeren van de linter aanroep
    """
    def __init__(self, **parms):
        self.p = {
            'linter': '',
            'pad': '',
            'filelist': [],
            'subdirs': False,
            "follow_symlinks": False,
            "maxdepth": 5,
            'fromrepo': False,
            'mode': '',
            'blacklist': {}}
        for x, y in parms.items():
            if x in self.p:
                self.p[x] = y
            else:
                raise ValueError('Onbekende optie ' + x)
        self.ok = True
        self.rpt = []  # verslag van wat er gebeurd is
        if not self.p['filelist'] and not self.p['pad']:
            self.rpt.append("Fout: geen lijst bestanden en geen directory opgegeven")
        elif self.p['filelist'] and self.p['pad']:
            self.rpt.append("Fout: lijst bestanden én directory opgegeven")
        elif not self.p['linter']:
            self.rpt.append('Fout: geen linter opgegeven')
        if self.rpt:
            self.ok = False
            return
        specs = [f"Gecontroleerd met \'{self.p['linter']}\'"]
        self.filenames = []
        self.dirnames = set()
        if self.p['fromrepo']:
            specs.append(f" from repo manifest in {self.p['pad']}")
            self.get_from_repo()
        else:
            if self.p['pad']:
                specs.append(f" in {self.p['pad']}")
                self.subdirs(self.p['pad'])
            else:
                if len(self.p['filelist']) == 1:
                    specs.append(f" in {self.p['filelist'][0]}")
                else:
                    specs.append(" in opgegeven bestanden/directories")
                for entry in self.p['filelist']:
                    self.subdirs(entry)
            if self.p['subdirs']:
                specs.append(" en onderliggende directories")
        self.rpt.insert(0, "".join(specs))
        self.results = {}
        self.specs = specs

    def get_from_repo(self):
        """get files from repo manifest
        also apply blacklisted names
        """
        # self.dirnames = set()
        # self.filenames = []
        for entry in self.p['filelist']:
            # print(entry)
            hlp = pathlib.Path(entry)
            if hlp.name in self.p['blacklist']['exclude_files']:
            # if os.path.basename(entry) in self.p['blacklist']['exclude_files']:
                continue
            test = hlp.suffix[1:]  # .lstrip('.')
            # test = os.path.splitext(entry)[1].lstrip('.')
            if test not in self.p['blacklist']['include_exts']:
                continue
            self.dirnames.add(str(hlp.parent))
            self.filenames.append(entry)

    def subdirs(self, pad, level=0):
        """ samenstellen lijsten met te verwerken directories en files
        """
        if self.p["maxdepth"] != -1:
            level += 1
            if level > self.p["maxdepth"]:
                self.rpt.append(f'{pad}: below maximum scanlevel')
                return
        path = pathlib.Path(pad)
        if path.is_symlink() and not self.p['follow_symlinks']:
            return
        if path.is_dir() and not self.dir_is_blacklisted(path):
            self.dirnames.add(pad)
            try:
                _list = list(os.scandir(pad))
            except PermissionError as err:
                self.rpt.append(f'could not scan {pad}: {err}')
                return
            for entry in _list:
                self.subdirs(entry.path, level=level)
        elif path.is_file():
            if not self.file_is_blacklisted(path):
                self.filenames.append(pad)
                try:
                    path.read_text()
                    # self.filenames.append(pad)
                except PermissionError as err:
                    self.rpt.append(f'could not read {pad}: {err}')

    def file_is_blacklisted(self, entry):
        "lookup filename in blacklist and return if it should be skipped"
        if entry.name in self.p['blacklist']['exclude_files']:
            return True
        ext = entry.suffix
        if ext:
            if (self.p['blacklist']['include_exts']
                    and ext[1:] not in self.p['blacklist']['include_exts']):
                return True
            if ext[1:] in self.p['blacklist']['exclude_exts']:
                return True
        elif self.p['blacklist']['include_shebang']:
            data = entry.read_text().split('\n', 1)[0]  # get first line of file
            if data.startswith('#!'):
                for runner in self.p['blacklist']['include_shebang']:
                    if runner in data:
                        return True
        return False

    def dir_is_blacklisted(self, entry):
        "lookup directory name in blacklist and return if it should be skipped"
        if entry.name in self.p['blacklist']['exclude_dirs']:
            return True
        return False

    def do_action(self):
        """do the linting
        """
        for name in self.filenames:
            props = cmddict[self.p['linter'].lower()]
            command = [x.replace('{}', f'{name}') for x in props['command']]
            command[2:3] += checktypes[self.p['mode']][self.p['linter'].lower()]
            go = subprocess.run(command, stdout=subprocess.PIPE, check=False)
            if not go.stdout:
                self.results[name] = f'No results for {name}'
            else:
                self.results[name] = str(go.stdout, encoding='utf-8')


"""\
checken van een package met output naar één file
pylint3 modreader > modreader/pylint_report.txt

dit checkt alle py files in de aangegeven directory
python3 -m flake8 . --output-file=flake8_report.txt

inbouwen:

pylint:
To silently run Pylint on a module_name.py module, and get its standard output and error:
from pylint import epylint as lint
(pylint_stdout, pylint_stderr) = lint.py_run('module_name.py', return_std=True)
flake8: misschien met
check = flake8.main.application.Application ()
check.initialize(options)
check.run_checks(program(s))
check.report() dan wel .report_errors() / .report.statistics()
of volgens 2.5 docs:
flake8.main.check_file(path, ignore=(), complexity=-1)
"""
