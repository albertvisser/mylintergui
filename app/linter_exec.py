"""Uitvoeren van de find/replace actie

de uitvoering wordt gestuurd door in een dictionary verzamelde parameters
"""
import os
import subprocess
from .linter_config import cmddict, checktypes


class Linter(object):
    """interpreteren van de parameters en aansturen van de zoek/vervang routine
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
                raise TypeError('Onbekende optie ' + x)
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
        specs = ["Gecontroleerd met '{}'".format(self.p['linter'])]
        self.filenames = []
        self.dirnames = set()
        if self.p['fromrepo']:
            specs.append(" from repo manifest in {}".format(self.p['pad']))
            self.get_from_repo()
        else:
            if self.p['pad']:
                specs.append(" in {}".format(self.p['pad']))
                self.subdirs(self.p['pad'])
            else:
                if len(self.p['filelist']) == 1:
                    specs.append(" in {}".format(self.p['filelist'][0]))
                else:
                    specs.append(" in opgegeven bestanden/directories")
                for entry in self.p['filelist']:
                    self.subdirs(entry, is_list=False)
            if self.p['subdirs']:
                specs.append(" en onderliggende directories")
        self.rpt.insert(0, "".join(specs))
        self.results = {}
        self.specs = specs

    def get_from_repo(self):
        """get files from repo manifest
        also apply blacklisted names
        """
        if not self.p['filelist']:
            # get files from manifest (in case of standalone version of backend)
            # let's assume we'll always be going by the frontend for now
            pass
        self.filenames = []
        for entry in self.p['filelist']:
            # hlp = pathlib.Path(entry)
            # if hlp.name in self.p['blacklist']['exclude_files']:
            if os.path.basename(entry) in self.p['blacklist']['exclude_files']:
                continue
            # test = hlp.suffix.lstrip('.')
            test = os.path.splitext(entry)[1].lstrip('.')
            if test not in self.p['blacklist']['include_exts']:
                continue
            self.filenames.append(entry)

    def subdirs(self, pad, is_list=True, level=0):
        """recursieve routine voor zoek/vervang in subdirectories
        samenstellen lijst met te verwerken bestanden

        als is_list = False dan wordt van de doorgegeven naam eerst een list
        gemaakt. Daardoor hebben we altijd een iterable met directorynamen.
        """
        if os.path.isdir(pad):
            if os.path.basename(pad) not in self.p['blacklist']['exclude_dirs']:
                self.dirnames.add(pad)
        if self.p["maxdepth"] != -1:
            level += 1
            if level > self.p["maxdepth"]:
                return
        if is_list:
            try:
                _list = [fname.path for fname in os.scandir(pad)]
            except PermissionError:
                _list = []
        else:
            _list = [pad]
        for entry in _list:
            if os.path.isdir(entry):
                if os.path.basename(entry) in self.p['blacklist']['exclude_dirs']:
                    continue
                if self.p['subdirs']:
                    self.subdirs(entry, level=level)
            elif os.path.islink(entry) and not self.p['follow_symlinks']:
                pass
            else:
                if os.path.basename(entry) in self.p['blacklist']['exclude_files']:
                    continue
                ext = os.path.splitext(entry)[1]
                if ext and ext[1:] not in self.p['blacklist']['include_exts']:
                    continue
                if ext and ext[1:] in self.p['blacklist']['exclude_exts']:
                    continue
                if not ext and self.p['blacklist']['include_shebang']:
                    lines = []
                    with open(entry) as _in:
                        lines.append(_in.readline())
                        lines.append(_in.readline())
                    skip = True
                    if any([x[:2] == '#!' for x in lines]):
                        for line in lines:
                            if line.startswith('#!'):
                                for shb in self.p['blacklist']['include_shebang']:
                                    if shb in line:
                                        skip = False
                                        break
                    if skip:
                        continue
                self.filenames.append(entry)

    def do_action(self):
        """do the linting
        """
        for name in self.filenames:
            props = cmddict[self.p['linter'].lower()]
            command = [x.replace('{}', '{}'.format(name)) for x in props['command']]
            command[2:3] += checktypes[self.p['mode']][self.p['linter'].lower()]
            go = subprocess.run(command, stdout=subprocess.PIPE)
            if not go.stdout:
                self.results[name] = 'No results for {}'.format(name)
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
