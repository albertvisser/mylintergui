"""MyLinterGUI Gui-toolkit-onafhankelijke code

het meeste hiervan bevind zich in een class die als mixin gebruikt wordt
"""
import sys
import os
import pathlib
# import enum
import datetime
import contextlib
import subprocess
import json
# import app.qtqui as gui
from app import qtgui as gui
from .exec import Linter
from .config import Mode, checktypes  # , cmddict

origpath = sys.path
sys.path.insert(0, str(pathlib.Path.home() / 'bin'))
# importlib.import_module('settings')
import settings
sys.path = origpath
DO_NOT_LINT = settings.DO_NOT_LINT

BASE = pathlib.Path.home() / '.mylinter'
if not BASE.exists():
    BASE.mkdir()
edfile = BASE / 'open_result'
# initial_edfile = "program = 'SciTE'\\nfile-option = '-open:{}'\\nline-option = '-goto:{}'\\n"
initial_edfile = '\n'.join(("program = 'SciTE'", "file-option = '-open:{}'",
                            "line-option = '-goto:{}'"))
blacklist = BASE / 'donot_lint'
initial_blacklist = {
    'exclude_dirs': ['__pycache__', '.hg', '.git'],
    'exclude_exts': ['pyc', 'pyo', 'so', 'pck'],
    'include_exts': ['py', 'pyw', ''],
    'exclude_files': ['.hgignore', '.gitignore'],
    'include_shebang': ['python', 'python3'], }
HERE = pathlib.Path(__file__).parent
iconame = str(HERE / "lintergui.png")


def get_iniloc(path=None):
    """get location for ini file

    Note: pathlib.Path returns the same path when path is already a path object
    """
    path = pathlib.Path(path) if path else pathlib.Path.cwd()
    if path == pathlib.Path.home():
        here = '~'
    else:
        path = path.resolve()
        try:
            here = '~' + str(path.relative_to(pathlib.Path.home()))
        except ValueError:
            here = str(path)
    if here.startswith('/'):
        here = here[1:]
    iniloc = BASE / here.replace('/', '_')
    mrufile = iniloc / 'mru_items.json'
    optsfile = iniloc / 'options.json'
    return iniloc, mrufile, optsfile


class Base:
    """Applicatielogica klasse voor de linter applicatie
    Gebruikt (qt_)gui voor de user interface en exec voor de uitvoering van het linten
    """
    def __init__(self, args):
        """attributen die altijd nodig zijn
        """
        self.title = "Albert's linter GUI frontend"
        self.iconame = iconame
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
        self.set_mode(args)
        self.gui = gui.MainGui(master=self)
        self.gui.setup_screen()

    def set_mode(self, args):
        """determine execution mode

        assumes command line parsing has already been done
        """
        self.linter_from_input = args.c
        self.dest_from_input = args.o
        self.skip_screen = args.s
        self.checking_type = args.m
        self.repo_only = False
        if args.r:
            self.repo_only = True
            args.d = settings.get_project_dir(args.r)

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
                                if line.endswith(("\\", "/")):
                                    line = line[:-1]
                                self.hier = pathlib.Path(line).resolve().parent
                            self.fnames.append(line)
                    except FileNotFoundError:
                        raise ValueError('Input name is not a usable file for multi '
                                         'mode: should contain (only) path names') from None
            elif inp:
                self.fnames = inp
            else:
                raise ValueError('Need filename or list of files for application type "multi"')
            self.readini(os.path.commonpath(self.fnames))
        else:
            raise ValueError('Execution mode could not be determined from input')

        if len(self.fnames) > 0:
            self.p["filelist"] = self.fnames
        for ix, name in enumerate(self.fnames):
            if name.endswith(("\\", "/")):
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
                opts = {}
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
        loc.mkdir(exist_ok=True)
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
            test = initial_edfile
            edfile.write_text(test)
        # print(test)
        self.editor_option = [x.split(' = ')[1].strip("'") for x in test.split('\n') if x]
        if self.editor_option[0].startswith('['):
            command_list = [x[1:-1] for x in self.editor_option[0][1:-1].split(', ')]
            self.editor_option[0] = command_list
        else:
            self.editor_option[0] = [self.editor_option[0]]

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

    def doe(self):
        """Zoekactie uitvoeren en resultaatscherm tonen"""
        test = self.gui.get_radiogroup_checked(self.gui.check_options)
        mld = self.check_type(test.replace('&', '').lower())
        if not mld:
            test = self.gui.get_radiogroup_checked(self.gui.linters)
            mld = self.check_linter(test.replace('&', '').lower())
        if not mld and self.mode == Mode.standard.value:
            mld = self.checkpath(self.gui.get_combobox_textvalue(self.gui.vraag_dir))

        if not mld:
            if self.mode == Mode.standard.value:  # and self.vraag_repo.isChecked():
                mld = self.checkrepo(self.gui.get_checkbox_value(self.gui.vraag_repo),
                                     self.gui.get_combobox_textvalue(self.gui.vraag_dir))
            elif self.mode != Mode.single.value or os.path.isdir(self.fnames[0]):
                self.checksubs(self.gui.get_checkbox_value(self.gui.vraag_subs),
                               self.gui.get_checkbox_value(self.gui.vraag_links),
                               self.gui.get_spinbox_value(self.gui.vraag_diepte))
            elif self.mode == Mode.single.value and os.path.islink(self.fnames[0]):
                self.p["follow_symlinks"] = True
        if not mld and self.gui.get_checkbox_value(self.gui.vraag_quiet):
            mld = self.check_quiet_options()
        if mld:
            self.gui.meld_fout(mld)
            return

        if not self.skip_screen:
            loc = self.p.get('pad', '') or os.path.dirname(self.p['filelist'][0])
            self.schrijfini(loc)
        self.p['blacklist'] = self.blacklist
        self.do_checks = Linter(**self.p)
        if not self.do_checks.ok:
            self.gui.meld_info('\n'.join(self.do_checks.rpt))
            return

        if not self.do_checks.filenames:
            self.gui.meld_info("Geen bestanden gevonden")
            return

        common_part = self.determine_common()
        if not (self.mode == Mode.single.value or (len(self.fnames) == 1
                                                   and os.path.isfile(self.fnames[0]))):
            skip_dirs = self.gui.get_checkbox_value(self.gui.ask_skipdirs)
            skip_files = self.gui.get_checkbox_value(self.gui.ask_skipfiles)

            go_on = skip_dirs or skip_files
            canceled = False
            while go_on:
                if skip_dirs:
                    # eerste ronde: toon directories
                    if self.do_checks.dirnames:
                        self.names = sorted(self.do_checks.dirnames)
                        canceled = not gui.show_dialog(gui.SelectNames, files=False)
                        if canceled:
                            break
                        # tweede ronde: toon de files die overblijven
                        fnames = self.do_checks.filenames[:]
                        for fname in fnames:
                            for name in self.names:
                                if fname.startswith(name + '/'):
                                    self.do_checks.filenames.remove(fname)
                                    break
                        if not self.gui.get_checkbox_value(self.gui.ask_skipfiles):
                            go_on = False
                if self.gui.get_checkbox_value(self.gui.ask_skipfiles):
                    self.names = sorted(self.do_checks.filenames)
                    canceled = not gui.show_dialog(gui.SelectNames)
                    if canceled and not self.gui.get_checkbox_value(self.gui.ask_skipdirs):
                        # canceled = True
                        break
                    if not canceled:
                        self.do_checks.filenames = self.names
                        go_on = False
            if canceled:
                return

        self.gui.execute_action()
        gui.Results(self.gui, common_part)

    def check_loc(self, txt):
        """update location to get settings from
        """
        if os.path.exists(txt) and not txt.endswith(os.path.sep):
            self.readini(txt)
            # self.vraag_dir.clear()
            # self.vraag_dir.addItems(self._mru_items["dirs"])
            self.gui.set_checkbox_value(self.gui.vraag_subs, self.p["subdirs"])
            self.gui.set_checkbox_value(self.gui.vraag_repo, self.p["fromrepo"])

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
            mld = "Please enter or select a directory"
        else:
            try:
                test = pathlib.Path(item).expanduser().resolve()
            except FileNotFoundError:
                mld = "De opgegeven directory bestaat niet"
            else:
                mld = ""
                test = str(test)
                with contextlib.suppress(ValueError):
                    self._mru_items["dirs"].remove(test)
                self._mru_items["dirs"].insert(0, test)
                self.s += f"\nin {test}"
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
            if self.quiet_options.get('dest', '') in ('single', 'multi'):
                dest_ok = True
            if self.quiet_options.get('pattern', ''):
                patt_ok = True
        if not dest_ok or not patt_ok:
            mld = 'Please configure all options for quiet mode'
        return mld

    def checkrepo(self, is_checked, path):
        """check setting for "only do tracked files"
        """
        self.p['fromrepo'] = is_checked
        command = mld = ''
        if not is_checked:
            return mld
        repo_loc = pathlib.Path(path).expanduser().resolve()
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
            result = subprocess.run(command, cwd=str(cwd), stdout=subprocess.PIPE, check=False).stdout
            self.p['pad'] = ''
            # self.p['filelist'] = [str(repo_loc / name)
            #                       for name in str(result, encoding='utf-8').split('\n')
            #                       if name]  # is dit een zinnige toevoeging?
            self.p['filelist'] = []
            filelist = [repo_loc / name for name in str(result, encoding='utf-8').split('\n')
                        if name]  # is dit een zinnige toevoeging?
            for path in filelist:
                if path.is_symlink():
                    continue
                if path.suffix in ('.py', '.pyw'):  # python source files
                    self.p['filelist'].append(str(path))
                elif path.suffix == '':  # check shebang
                    filestart = path.read_text().split('\n')[0]
                    if filestart.startswith('#!') and 'python' in filestart:
                        self.p['filelist'].append(str(path))
        return mld

    def configure_quiet(self):
        """configure quiet mode
        """
        # dlg = QuietOptions(self).exec_()
        # if dlg != qtw.QDialog.Accepted:
        ok = gui.show_dialog(gui.QuietOptions)
        if not ok:
            return
        if self.gui.newquietoptions['single_file']:
            self.quiet_options['dest'] = Mode.single.name
        else:
            self.quiet_options['dest'] = Mode.multi.name
        test = self.gui.newquietoptions['fname']
        if test:
            self.quiet_options['fname'] = test
        test = self.gui.newquietoptions['pattern']
        if test:
            self.quiet_options['pattern'] = test

    def configure_filter(self):
        """configure filtering
        """
        # dlg = FilterOptions(self).exec_()
        # if dlg == qtw.QDialog.Accepted:
        ok = gui.show_dialog(gui.FilterOptions)
        if ok:
            self.update_blacklistfile()

    def get_output_filename(self, name, fromname=''):
        """build filename for file to send output to
        """
        if fromname and '<ignore>' in name:
            fromname = fromname.replace(self.quiet_options['ignore'], '')
        name = name.replace('<filename>', fromname)
        name = name.replace('<ignore>', '')
        while '//' in name:
            name = name.replace('//', '/')
        name = name.replace('<linter>', self.p['linter'])
        name = name.replace('<date>', datetime.datetime.today().strftime('%Y%m%d%H%M%S'))
        name = os.path.expanduser(name)
        return name

    def configure_linter(self):
        """open pylint configuration in editor

        rekening houden met verschillende opbouw van de optie string:
        voor pylint is het ['name', 'value'], voor flake8 is het ['name=value']
        """
        linter = self.gui.get_radiogroup_checked(self.gui.linters).replace('&', '').lower()
        if not linter:
            return
        test = self.gui.get_radiogroup_checked(self.gui.check_options)[1:].lower()
        if not test or test == 'default':
            return
        fnaam = checktypes[test][linter][-1].split('=')[-1]
        # subprocess.run(['xdg-open', fnaam], check=False)
        prog, fileopt, _ = self.editor_option
        subprocess.run(prog + [fileopt.format(fnaam)])

    def determine_common(self):
        """get part of path all files have in common
        """
        if self.mode == Mode.single.value:
            test = self.fnames[0]
        elif self.mode == Mode.multi.value:
            test = os.path.commonpath(self.fnames)
            # if test in self.fnames:
            #    pass
            # else:
            #    while test and not os.path.exists(test):
                    ## test = test[:-1]
            if os.path.isfile(test):
                test = os.path.dirname(test) + os.sep
        else:
            test = self.p["pad"] + os.sep
        return test
