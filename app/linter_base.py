"""Gui-onafhankelijke code t.b.v. Afrift applicaties

het meeste hiervan bevind zich in een class die als mixin gebruikt wordt
"""
import os
import pathlib
import logging
import enum
## import pickle
import json

BASE = pathlib.Path.home() / '.mylinter'
if not BASE.exists():
    BASE.mkdir()
edfile = BASE / 'open_result'
blacklist = BASE / 'donot_lint'
HERE = pathlib.Path(__file__).parent
iconame = str(HERE / "find.ico")
logfile = pathlib.Path(HERE) / '..' / 'logs' / 'linter.log'
logging.basicConfig(filename=str(logfile), level=logging.DEBUG,
                    format='%(asctime)s %(message)s')


def log(message):
    if 'DEBUG' in os.environ and os.environ["DEBUG"] != "0":
        logging.info(message)


def get_iniloc():
    here = str(pathlib.Path.cwd()).replace(os.environ['HOME'] + '/', '~').replace(
        '/', '_')
    if here[0] == '_':
        here = here[1:]
    iniloc = BASE / here
    mrufile = iniloc / 'mru_items.json'
    optsfile = iniloc / 'options.json'
    return iniloc, mrufile, optsfile


class Mode(enum.Enum):
    single = 'f'
    standard = 'd'
    multi = 'l'


class LBase(object):
    """
    mixin base class voor de Application classes

    deze class bevat methoden die onafhankelijk zijn van de gekozen
    GUI-toolkit"""

    ## def __init__(self, parent, apptype="", fnaam="", flist=None):
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
            'pattern': '/'.join(('~', '.linters', '<linter>', '<ignore>',
                                 '<filename>-<date>')),
            'fname': '<linter>_results-<date>',
            'ignore': '~/projects'}
        self._words = ('woord', 'woord', 'spec', 'pad', )
        self._optkeys = ("subdirs",)
        for key in self._optkeys:
            self.p[key] = False
        self._options = ("searchsubdirs",)
        self.readini()
        self.fnames = []
        self.get_editor_option()
        self.build_blacklist()

    def set_mode(self, args):
        # determine execution mode assuming command line parsing has already been done
        self.linter_from_input = args.c
        self.dest_from_input = args.o
        self.skip_screen = args.s

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
            self.hier = pathlib.Path.cwd()
            if inp.startswith('...'):   # TODO: kan dit slimmer m.b.v. pathlib?
                pass
            elif inp.startswith('..'):
                inp = inp.replace('..', str(self.hier.parent), 1)
            elif inp.startswith('.'):
                inp = inp.replace('.', str(self.hier), 1)
            elif inp.startswith('~'):
                inp = os.path.expanduser(inp)
            if inp:
                self.fnames = [inp]
        elif self.mode == Mode.single.value:  # data is file om te verwerken
            self.title += " - single file version"
            if not inp:
                raise ValueError('Need filename for application type "single"')
            inp = pathlib.Path(inp).resolve()
            self.fnames = [str(inp)]
            self.hier = inp.parent
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
                            ## if line.endswith("\\") or line.endswith("/"):
                                ## # directory afwandelen en onderliggende files verzamelen
                                ## pass
                            ## else:
                                ## self.fnames.append(line)
                            self.fnames.append(line)
                    except FileNotFoundError:
                        raise ValueError('Input name is not a usable file for multi '
                                         'mode: should contain (only) path names')
            elif inp:
                self.fnames = inp
            else:
                raise ValueError('Need filename or list of files for application type'
                                 ' "multi"')
        else:
            raise ValueError('Execution mode could not be determined from input')

        if len(self.fnames) > 0:
            self.p["filelist"] = self.fnames
        for ix, name in enumerate(self.fnames):
            if name.endswith("\\") or name.endswith("/"):
                self.fnames[ix] = name[:-1]

    def readini(self):
        """lees ini file (met eerder gebruikte zoekinstellingen)

        geen settings file of niet te lezen dan initieel laten
        """
        loc, mfile, ofile = get_iniloc()
        if loc.exists():
            with mfile.open() as _in:
                self._mru_items = json.load(_in)
            with ofile.open() as _in:
                opts = json.load(_in)
            for key in self._optkeys:
                self.p[key] = opts[key]
            for key in self.quiet_keys:
                if key in opts:
                    self.quiet_options[key] = opts[key]

    def schrijfini(self):
        """huidige settings toevoegen dan wel vervangen in ini file"""
        loc, mfile, ofile = get_iniloc()
        if not loc.exists():
            loc.mkdir()
        with mfile.open("w") as _out:
            json.dump(self._mru_items, _out, indent=4)
        opts = {key: self.p[key] for key in self._optkeys}
        opts.update({key: self.quiet_options[key] for key in self.quiet_keys})
        with ofile.open("w") as _out:
            json.dump(opts, _out, indent=4)

    def get_editor_option(self):
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
        try:
            with blacklist.open() as _blf:
                self.blacklist = json.load(_blf)
        except FileNotFoundError:
            self.blacklist = {
                'exclude_dirs': ['__pycache__', '.hg', '.git'],
                'exclude_exts': ['pyc', 'pyo', 'so', 'pck'],
                'include_exts': ['py', 'pyw', ''],
                'exclude_files': ['.hgignore', '.gitignore'],
                'include_shebang': ['python', 'python3'], }
            self.update_blacklistfile()

    def update_blacklistfile(self, data):
        with blacklist.open('w') as _blf:
            json.dump(self.blacklist, _blf, indent=4)

    def check_linter(self, item):
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
        elif not os.path.exists(item):
            mld = "De opgegeven directory bestaat niet"
        else:
            mld = ""
            try:
                self._mru_items["dirs"].remove(item)
            except ValueError:
                pass
            self._mru_items["dirs"].insert(0, item)
            self.s += "\nin {0}".format(item)
            self.p["pad"] = item
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
