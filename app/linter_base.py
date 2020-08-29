"""MyLinterGUI Gui-toolkit-onafhankelijke code

het meeste hiervan bevind zich in een class die als mixin gebruikt wordt
"""
import sys
import os
import pathlib
import logging
import enum
import subprocess
import json
origpath = sys.path
sys.path.insert(0, str(pathlib.Path.home() / 'bin'))
## importlib.import_module('settings')
import settings
sys.path = origpath
DO_NOT_LINT = settings.DO_NOT_LINT

BASE = pathlib.Path.home() / '.mylinter'
if not BASE.exists():
    BASE.mkdir()
edfile = BASE / 'open_result'
blacklist = BASE / 'donot_lint'
initial_blacklist = {
    'exclude_dirs': ['__pycache__', '.hg', '.git'],
    'exclude_exts': ['pyc', 'pyo', 'so', 'pck'],
    'include_exts': ['py', 'pyw', ''],
    'exclude_files': ['.hgignore', '.gitignore'],
    'include_shebang': ['python', 'python3'], }
HERE = pathlib.Path(__file__).parent
iconame = str(HERE / "lintergui.png")
logfile = pathlib.Path(HERE) / '..' / 'logs' / 'linter.log'
logging.basicConfig(filename=str(logfile), level=logging.DEBUG,
                    format='%(asctime)s %(message)s')


def log(message):
    """log only if debugging mode is on
    """
    if 'DEBUG' in os.environ and os.environ["DEBUG"] != "0":
        logging.info(message)


def get_iniloc(path=None):
    """get location for ini file

    Note: pathlib.Path returns the same path when path is already a path object
    """
    path = pathlib.Path(path) if path else pathlib.Path.cwd()
    if path == pathlib.Path.home():
        here = str(path)[1:]
    else:
        try:
            here = '~' + str(path.relative_to(pathlib.Path.home()))
        except ValueError:
            here = str(path)[1:]
    iniloc = BASE / here.replace('/', '_')
    mrufile = iniloc / 'mru_items.json'
    optsfile = iniloc / 'options.json'
    return iniloc, mrufile, optsfile


class Mode(enum.Enum):
    """execution modes
    """
    single = 'f'
    standard = 'd'
    multi = 'l'


class LBase(object):
    """
    mixin base class voor de Application classes

    deze class bevat methoden die onafhankelijk zijn van de gekozen
    GUI-toolkit"""

    def __init__(self):
        """attributen die altijd nodig zijn
        """
        self.title = "Albert's linter GUI frontend"
        self.fouttitel = self.title + "- fout"
        self.resulttitel = self.title + " - Resultaten"
        self.hier = ""
        self._mru_items = {}
        self.s = ''
        self.p = {}
        self._keys = ("dirs",)
        for key in self._keys:
            self._mru_items[key] = []
        self._optionskey = "options"
        self._sections = ('dirs',)
        self.quiet_keys = ('dest', 'pattern', 'fname', 'ignore')
        self.quiet_options = {
            'dest': 'multi',
            'pattern': os.path.join('~', '.linters', '<linter>', '<ignore>', '<filename>-<date>'),
            'fname': '<linter>_results-<date>',
            'ignore': os.path.expanduser('~/projects')}
        self._words = ('woord', 'woord', 'spec', 'pad', )
        self._optkeys = ("subdirs", "fromrepo")
        for key in self._optkeys:
            self.p[key] = False
        self.fnames = []
        self.get_editor_option()
        self.build_blacklist()

    def set_mode(self, args):
        """determine execution mode

        assumes command line parsing has already been done
        """
        self.linter_from_input = args.c
        self.dest_from_input = args.o
        self.skip_screen = args.s
        self.checking_type = args.m

        for x in Mode:
            test = args.__getattribute__(x.value)
            if test:
                self.mode = x.value
                inp = test
                break
        else:
            self.mode = Mode.standard.value
            inp = ''

        if self.mode == Mode.standard.value:
            if inp:
                inp = pathlib.Path(inp).expanduser().resolve()
                self.fnames = [str(inp)]
                self.readini(inp)
            else:
                self.readini()
        elif self.mode == Mode.single.value:  # data is file om te verwerken
            self.title += " - single file version"
            if not inp:
                raise ValueError('Need filename for application type "single"')
            inp = pathlib.Path(inp).resolve()
            self.fnames = [str(inp)]
            self.hier = inp.parent
            self.readini(self.hier)
        elif self.mode == Mode.multi.value:  # data is file met namen om te verwerken
            self.title += " - file list version"
            if len(inp) == 1:
                with open(inp[0]) as f_in:
                    try:
                        for line in f_in:
                            line = line.strip()
                            if not self.hier:
                                if line.endswith("\\") or line.endswith("/"):
                                    line = line[:-1]
                                self.hier = pathlib.Path(line).resolve().parent
                            self.fnames.append(line)
                    except FileNotFoundError:
                        raise ValueError('Input name is not a usable file for multi '
                                         'mode: should contain (only) path names')
            elif inp:
                self.fnames = inp
            else:
                raise ValueError('Need filename or list of files for application type'
                                 ' "multi"')
            self.readini(os.path.commonpath(self.fnames))
        else:
            raise ValueError('Execution mode could not be determined from input')

        if len(self.fnames) > 0:
            self.p["filelist"] = self.fnames
        for ix, name in enumerate(self.fnames):
            if name.endswith("\\") or name.endswith("/"):
                self.fnames[ix] = name[:-1]

    def readini(self, path=None):
        """lees ini file (met eerder gebruikte zoekinstellingen)

        geen settings file of niet te lezen dan initieel laten
        """
        loc, mfile, ofile = get_iniloc(path)
        if loc.exists():
            try:
                with mfile.open() as _in:
                    self._mru_items = json.load(_in)
            except FileNotFoundError:
                pass
            try:
                with ofile.open() as _in:
                    opts = json.load(_in)
            except FileNotFoundError:
                pass
            for key in self._optkeys:
                self.p[key] = opts.get(key, False)
            for key in self.quiet_keys:
                if key in opts:
                    if key == 'ignore' and opts[key].startswith('~'):
                        continue
                    self.quiet_options[key] = opts[key]

    def schrijfini(self, path=None):
        """huidige settings toevoegen dan wel vervangen in ini file"""
        loc, mfile, ofile = get_iniloc(path)
        if not loc.exists():
            loc.mkdir()
        with mfile.open("w") as _out:
            json.dump(self._mru_items, _out, indent=4)
        opts = {key: self.p[key] for key in self._optkeys}
        opts.update({key: self.quiet_options[key] for key in self.quiet_keys})
        with ofile.open("w") as _out:
            json.dump(opts, _out, indent=4)

    def get_editor_option(self):
        """determine which editor to use and how
        """
        try:
            test = edfile.read_text()
        except FileNotFoundError:
            test = '\n'.join(("program = 'SciTE'",
                              "file-option = '-open:{}'",
                              "line-option = '-goto:{}'",
                              ""))
            edfile.write_text(test)
        self.editor_option = [x.split(' = ')[1].strip("'")
                              for x in test.strip().split('\n')]

    def build_blacklist(self):
        """(re)write blacklist
        """
        try:
            with blacklist.open() as _blf:
                self.blacklist = json.load(_blf)
        except FileNotFoundError:
            self.blacklist = initial_blacklist
            self.update_blacklistfile()

    def update_blacklistfile(self):
        """write back changed blacklist entries
        """
        with blacklist.open('w') as _blf:
            json.dump(self.blacklist, _blf, indent=4)

    def check_type(self, item):
        """check linter options
        """
        if not item:
            mld = 'Please select a check type'
        else:
            mld = ""
            self.p["mode"] = item
        return mld

    def check_linter(self, item):
        """check linter options
        """
        if not item:
            mld = 'Please choose a linter to use'
        else:
            mld = ""
            self.p["linter"] = item
        return mld

    def checkpath(self, item):
        "controleer zoekpad"
        if not item:
            mld = ("Please enter or select a directory")
        else:
            try:
                test = pathlib.Path(item).expanduser().resolve()
            except FileNotFoundError:
                mld = "De opgegeven directory bestaat niet"
            else:
                mld = ""
                test = str(test)
                try:
                    self._mru_items["dirs"].remove(test)
                except ValueError:
                    pass
                self._mru_items["dirs"].insert(0, test)
                self.s += "\nin {0}".format(test)
                self.p["pad"] = test
                self.p['filelist'] = ''
        return mld

    def checksubs(self, *items):
        "subdirs aangeven"
        subdirs, links, depth = items
        if subdirs:
            self.s += " en onderliggende directories"
        self.p["subdirs"] = subdirs
        self.p["follow_symlinks"] = links
        self.p["maxdepth"] = depth

    def check_quiet_options(self):
        """check settings for quiet mode
        """
        mld = ''
        dest_ok = patt_ok = False
        if self.quiet_options:
            if 'dest' in self.quiet_options:
                if self.quiet_options['dest'] in ('single', 'multi'):
                    dest_ok = True
            if 'pattern' in self.quiet_options:
                if self.quiet_options['pattern']:
                    patt_ok = True
        if not dest_ok or not patt_ok:
            mld = 'Please configure all options for quiet mode'
        return mld

    def checkrepo(self, is_checked, path):
        """check setting for "only do tracked files"
        """
        command = mld = ''
        repo_loc = pathlib.Path(path).expanduser().resolve()
        if is_checked:
            test1 = repo_loc / '.hg'
            test2 = repo_loc / '.git'
            if repo_loc.stem in DO_NOT_LINT:
                mld = 'De opgegeven repository is aangemerkt als do-not-lint'
            elif test1.exists():
                command = ['hg', 'manifest']
                cwd = test1
            elif test2.exists():
                command = ['git', 'ls-files']
                cwd = test2
            else:
                mld = 'De opgegeven directory is geen (hg of git) repository'
            if command:
                result = subprocess.run(command, cwd=str(cwd),  # moet dit niet repo_loc zijn?
                                        stdout=subprocess.PIPE).stdout
                self.p['filelist'] = [str(repo_loc / name) for name in
                                      str(result, encoding='utf-8').split('\n')
                                      if name]
                self.p['pad'] = ''
        self.p['fromrepo'] = is_checked
        return mld
