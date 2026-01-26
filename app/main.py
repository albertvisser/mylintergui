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
from .config import Mode, checktypes, cmddict, default_option, default_linter

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
TXTW = 200
SEP = ', '


class LinterApp:
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
        self.common_part = ""
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
        self.get_editor_option()
        self.build_blacklist_if_needed()
        self.set_parameters(self.set_mode(args))
        self.gui = gui.LinterGui(master=self)
        self.setup_screen()
        self.gui.show()
        if self.skip_screen:
            self.doe()
            self.gui.close()
        else:
            self.gui.go()

    def setup_screen(self):
        "build the display"
        self.gui.start_display()
        options = []
        default = self.checking_type or default_option  # checktypes[default_option]
        for checktype in checktypes:
            options.append(('&' + checktype.title(), checktype == default))
        self.check_options = self.gui.build_radiobutton_row('Type of check:', options)
        options = []
        default = self.linter_from_input or default_linter  # cmddict[default_linter]
        for linter in cmddict:
            options.append(('py&lint' if linter == 'pylint' else '&' + linter, linter == default))
        self.linters = self.gui.build_radiobutton_block('Check using:', options)
        if self.mode == Mode.standard.value:
            initial = self.p['filelist'][0] if self.p['filelist'] else ''
            self.vraag_dir = self.gui.add_combobox_row("In directory:", self._mru_items["dirs"],
                                                       width=TXTW,
                                                       initial=initial, callback=self.check_loc,
                                                       button=("&Zoek", self.gui.zoekdir))
        elif self.mode == Mode.single.value:
            self.gui.show_single_mode_info('In file/directory:', self.p['filelist'][0])
        else:
            self.gui.show_multi_mode_info('In de volgende files/directories:', self.p['filelist'])
        if self.mode != Mode.single.value:
            self.vraag_filter = self.gui.add_checkbox_line(
                    'Use global whitelist/blacklist', toggle=True,
                    button=('Configure', self.configure_filter ))[0]
        if self.mode == Mode.standard.value:
            self.p['fromrepo'] = self.repo_only
            self.vraag_repo = self.gui.add_checkbox_line(
                'Check repository files only (also does subdirectories)', self.p['fromrepo'])[0]
        if self.mode != Mode.single.value or os.path.isdir(self.p['filelist'][0]):
            txt = "van geselecteerde directories " if self.mode == Mode.multi.value else ''
            self.vraag_subs = self.gui.add_checkbox_line(
                txt + "ook subdirectories doorzoeken", self.p["subdirs"])[0]
            self.vraag_links, self.vraag_diepte = self.gui.add_checkbox_line(
                    "symlinks volgen - max. diepte (-1 is onbeperkt):", spinner=(-1, 5))
            self.ask_skipdirs = self.gui.add_checkbox_line(
                    "selecteer (sub)directories om over te slaan")[0]
            self.ask_skipfiles = self.gui.add_checkbox_line(
                    "selecteer bestanden om over te slaan")[0]
        self.vraag_quiet = self.gui.add_checkbox_line('Output to file(s) directly',
                                                      toggle=self.dest_from_input,
                                                      button=('Configure', self.configure_quiet))[0]
        self.gui.add_buttons([('&Uitvoeren', self.doe), ('&Einde', self.gui.close)])
        self.gui.finalize_display(self.linters)

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

    def build_blacklist_if_needed(self):
        """(re)write blacklist
        """
        try:
            with blacklist.open() as _blf:
                self.blacklist = json.load(_blf)
        except FileNotFoundError:
            self.blacklist = initial_blacklist
            self.update_blacklistfile()

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
            args.d = settings.get_project_dir(pathlib.Path.cwd().name if args.r == '.' else args.r)

        for x in Mode:
            test = args.__getattribute__(x.value)
            if test:
                self.mode = x.value
                inp = test
                break
        else:
            self.mode = Mode.standard.value
            inp = ''
        return inp

    def set_parameters(self, inp):
        """determine where to read linting paramaters from depending on execution mode
        """
        if self.mode == Mode.standard.value:
            if inp:
                inp = pathlib.Path(inp).expanduser().resolve()
                self.p['filelist'] = [str(inp)]
                self.readini(inp)
            else:
                self.p['filelist'] = []
                self.readini()
        elif self.mode == Mode.single.value:  # data is file om te verwerken
            self.title += " - single file version"
            if not inp:
                raise ValueError('Need filename for application type "single"')
            inp = pathlib.Path(inp).resolve()
            self.p['filelist'] = [str(inp)]
            self.readini(inp.parent)
        elif self.mode == Mode.multi.value:  # data is file met namen om te verwerken
            self.title += " - file list version"
            if len(inp) == 1:
                fnames = get_paths_from_file(inp[0])
                if not fnames:
                    raise ValueError('Input is not a usable file for multi mode:'
                                     ' should contain (only) path names')
            elif inp:
                fnames = inp
            else:
                raise ValueError('Need filename or list of files for application type "multi"')
            self.p['filelist'] = fnames
            self.common_part = os.path.commonpath(fnames)
            self.readini(self.common_part)
        else:
            raise ValueError('Execution mode could not be determined from input')

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

    def update_blacklistfile(self):
        """write back changed blacklist entries
        """
        with blacklist.open('w') as _blf:
            json.dump(self.blacklist, _blf, indent=4)

    def doe(self):
        """Zoekactie uitvoeren en resultaatscherm tonen"""
        if mld := self.check_screen_input():   # TODO: is this needed when we skip the screen?
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
        # if not self.do_checks.filenames:
        #     self.gui.meld_info("Geen bestanden gevonden")
        #     return
        if len(self.p['filelist']) > 1 or os.path.isdir(self.p['filelist'][0]):
            canceled = self.determine_items_to_skip()
            if canceled:
                return
        self.do_checks.filenames = [x for x in self.do_checks.filenames if is_lintable(x)]
        if not self.do_checks.filenames:
            self.gui.meld_info("Geen (lintbare) bestanden gevonden")
            return
        self.gui.execute_action()
        gui.show_dialog(Results(self, self.common_part).gui)

    def check_screen_input(self):
        "validation of screen fields split off to lessen testing complexity"
        mld = self.check_type(self.gui.get_radiogroup_checked(self.check_options))
        mld = mld or self.check_linter(self.gui.get_radiogroup_checked(self.linters))
        if self.mode == Mode.standard.value:
            mld = mld or self.checkpath(self.gui.get_combobox_textvalue(self.vraag_dir))
            mld = mld or self.checkrepo(self.gui.get_checkbox_value(self.vraag_repo),
                                        self.gui.get_combobox_textvalue(self.vraag_dir))
        if (self.mode != Mode.single.value or os.path.isdir(self.p['filelist'][0])) and not mld:
            subdirs = self.gui.get_checkbox_value(self.vraag_subs)
            if subdirs:
                self.s += " en onderliggende directories"
            self.p["subdirs"] = subdirs
            self.p["follow_symlinks"] = self.gui.get_checkbox_value(self.vraag_links)
            self.p["maxdepth"] = self.gui.get_spinbox_value(self.vraag_diepte)
        if (self.mode == Mode.single.value and os.path.islink(self.p['filelist'][0])) and not mld:
            self.p["follow_symlinks"] = True
        mld = mld or self.check_quiet_options()
        return mld

    def check_loc(self, txt):
        """update location to get settings from
        """
        if os.path.exists(txt) and not txt.endswith(os.path.sep):
            self.readini(txt)
            # self.vraag_dir.clear()
            # self.vraag_dir.addItems(self._mru_items["dirs"])
            self.gui.set_checkbox_value(self.vraag_subs, self.p["subdirs"])
            self.gui.set_checkbox_value(self.vraag_repo, self.p["fromrepo"])

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
                self.p['filelist'] = [test]
        return mld

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
        if not is_checked:
            return ''
        command = mld = ''
        repo_loc = pathlib.Path(path).expanduser().resolve()
        if repo_loc.stem in DO_NOT_LINT:
            mld = 'De opgegeven repository is aangemerkt als do-not-lint'
        elif (repo_loc / '.git').exists():
            command = ['git', 'ls-files']
        elif (repo_loc / '.hg').exists():
            command = ['hg', 'manifest']
        else:
            mld = 'De opgegeven directory is geen (hg of git) repository'
        if command and not mld:
            result = subprocess.run(command, cwd=str(repo_loc), stdout=subprocess.PIPE,
                                    check=False).stdout
            # self.p['pad'] = ''
            # self.p['filelist'] = []
            filelist = [repo_loc / name for name in str(result, encoding='utf-8').split('\n')
                        if name]  # is dit een zinnige toevoeging?
            self.p["filelist"] = [str(x) for x in filelist if is_lintable(x)]
        return mld

    def configure_quiet(self):
        """configure quiet mode
        """
        ok = gui.show_dialog(QuietOptions(self).gui)
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
        ok = gui.show_dialog(FilterOptions(self).gui)
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
        linter = self.gui.get_radiogroup_checked(self.gui.linters)
        if not linter:
            return
        test = self.gui.get_radiogroup_checked(self.gui.check_options)
        if not test or test == 'default':
            return
        fnaam = checktypes[test][linter][-1].split('=')[-1]
        # subprocess.run(['xdg-open', fnaam], check=False)
        prog, fileopt, _ = self.editor_option
        subprocess.run(prog + [fileopt.format(fnaam)])

    def determine_items_to_skip(self):
        """remove entries from Linter.dirnames and/or Linter.filenames if requested
        """
        if not all((self.do_checks.dirnames, self.do_checks.filenames)):
            return False  # failsafe; kan eigenlijk niet (meer)
        skip_dirs = self.gui.get_checkbox_value(self.ask_skipdirs)
        skip_files = self.gui.get_checkbox_value(self.ask_skipfiles)

        go_on = skip_dirs or skip_files
        canceled = False
        while go_on:
            # eerste ronde: toon directories
            # print(self.do_checks.dirnames)
            if skip_dirs:
                self.names = sorted(self.do_checks.dirnames)
                canceled = not gui.show_dialog(SelectNames(self, files=False).gui)
                if canceled:
                    break
                self.remove_files_in_selected_dirs()
                if not skip_files:
                    go_on = False
            # tweede ronde: toon de files die overblijven
            if skip_files:
                # print(self.do_checks.filenames)
                self.names = sorted(self.do_checks.filenames)
                # print(self.names)
                canceled = not gui.show_dialog(SelectNames(self).gui)
                if canceled and not skip_dirs:
                    go_on = False
                    break
                if not canceled:
                    self.do_checks.filenames = self.names
                    go_on = False
        return canceled

    def remove_files_in_selected_dirs(self):
        """truncate list of filenames based on changes in list of dirnames
        """
        fnames = self.do_checks.filenames[:]
        for fname in fnames:
            for name in self.names:
                if fname.startswith(name + '/'):
                    self.do_checks.filenames.remove(fname)
                    break


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


def get_paths_from_file(fname):
    "read input from a file containing filenames"
    result = []
    with open(fname) as f_in:
        for line in f_in:
            line = line.strip()
            if line.endswith(("\\", "/")):
                line = line[:-1]
            if not pathlib.Path(line).absolute().exists(follow_symlinks=False):
                return []
            result.append(line)
    return result


def is_lintable(path):
    "return filename if file can be linted, else empty string"
    path = pathlib.Path(path)
    if not path.is_symlink():
        if path.suffix in ('.py', '.pyw'):  # python source files
            return True  # str(path)
        if path.suffix == '':  # check shebang
            filestart = path.read_text().split('\n')[0]
            if filestart.startswith('#!') and 'python' in filestart:
                return True  # str(path)
    return False  # ''


class FilterOptions:
    """configure what files (not) to lint
    """
    def __init__(self, parent):
        self.parent = parent
        self.gui = gui.FilterOptionsGui(self, parent.gui, parent.title)
        self.gui.add_title_line("Blacklist (do no lint):")
        self.skipdirs = self.gui.add_textentry_line(
            "Directory names:", SEP.join(self.parent.blacklist['exclude_dirs']), width=200)
        self.skipexts = self.gui.add_textentry_line(
            "File extensions:", SEP.join(self.parent.blacklist['exclude_exts']))
        self.skipfiles = self.gui.add_textentry_line(
            "File names:", SEP.join(self.parent.blacklist['exclude_files']))
        self.gui.add_title_line("")
        self.gui.add_title_line( "Whitelist (only lint):")
        self.do_exts = self.gui.add_textentry_line(
            "File extensions:", SEP.join(self.parent.blacklist['include_exts']))
        self.do_bangs = self.gui.add_textentry_line(
            "Shebang lines:", SEP.join(self.parent.blacklist['include_shebang']))
        self.gui.add_title_line("")
        self.gui.add_buttons([("&Terug", self.gui.reject), ("&Klaar", self.gui.accept)])

    def confirm(self):
        """transfer chosen options to parent"""
        self.parent.blacklist = {
            'exclude_dirs': self.get_text_from_gui(self.skipdirs),
            'exclude_exts': self.get_text_from_gui(self.skipexts),
            'exclude_files': self.get_text_from_gui(self.skipfiles),
            'include_exts': self.get_text_from_gui(self.do_exts),
            'include_shebang': self.get_text_from_gui(self.do_bangs)}

    def get_text_from_gui(self, textfield):
        "format the gui output for the settings file"
        return list(self.gui.get_textentry_value(textfield).split(SEP))


class QuietOptions:
    """configure where to send output to
    """
    text = """\
    <linter>: replace linter name in path
    <ignore>: part of source filename not to include in target name
    <filename>: (remainder of) source filename
    <date>: datetime.datetime.today().strftime('%Y%m%d%H%M%S')
    """

    def __init__(self, parent):
        self.parent = parent
        self.gui = gui.QuietOptionsGui(self, parent.gui, parent.title)
        line = self.gui.start_line()
        self.gui.add_text_to_line(line, "Send output to:")
        self.gui.end_line(line)

        line = self.gui.start_line()
        checked = self.parent.quiet_options['dest'] == Mode.single.name
        self.single = self.gui.add_radiobutton_to_line(line, 'Single file:', checked)
        self.fname = self.gui.add_textentry_to_line(line, self.parent.quiet_options['fname'],
                                                    width=TXTW)
        self.gui.add_button_to_line(line, 'Select', self.gui.browse)
        self.gui.end_line(line)

        line = self.gui.start_line()
        checked = self.parent.quiet_options['dest'] == Mode.multi.name
        self.multi = self.gui.add_radiobutton_to_line(line, 'Multiple files like:', checked)
        self.pattern = self.gui.add_textentry_to_line(line, self.parent.quiet_options['pattern'],
                                                    width=TXTW + 100)
        self.gui.end_line(line)

        line = self.gui.start_line()
        self.gui.add_text_to_line(line, '<ignore> part of filename:', before=26)
        self.ignore = self.gui.add_textentry_to_line(line, self.parent.quiet_options['ignore'],
                                                    width=TXTW)
        self.gui.end_line(line)

        line = self.gui.start_line()
        self.gui.add_text_to_line(line, self.text)
        self.gui.end_line(line)

        self.gui.add_buttons([("&Terug", self.gui.reject), ("&Klaar", self.gui.accept)])

        if self.parent.dest_from_input:
            self.gui.set_radiobutton_value(self.single, True)
            self.gui.set_textentry_value(self.fname, self.parent.dest_from_input)

    def browse(self):
        """callback for selector
        """
        # TODO

    def confirm(self):
        """transfer chosen options to parent"""
        self.parent.newquietoptions = {
            'single_file': self.gui.get_radiobutton_value(self.single),
            'fname': self.gui.get_textentry_value(self.fname),
            'pattern': self.gui.get_textentry_value(self.pattern),
            'ignore': self.gui.get_textentry_value(self.ignore)}


class SelectNames:
    """Tussenscherm om te verwerken files te kiezen
    """
    def __init__(self, parent, files=True):
        self.dofiles = files
        self.parent = parent
        self.gui = gui.SelectNamesGui(self, parent, parent.title + " - file list")

        line = self.gui.start_line()
        what = "bestanden" if files else "directories"
        self.gui.add_text_to_line(line, f"Selecteer de {what} die je *niet* wilt verwerken")

        line = self.gui.start_line()
        self.sel_all = self.gui.add_checkbox_to_line(line, 'Select/Unselect All', self.select_all,
                                                     before=10)
        self.flip_sel = self.gui.add_button_to_line(line, 'Invert selection', self.invert_selection,
                                                    before=20)

        self.checklist = self.gui.create_checkbox_list(self.parent.names)
        self.gui.create_button_bar([("&Terug", self.gui.reject), ("&Klaar", self.gui.accept)])

    def select_all(self):
        """check/uncheck all boxes
        """
        state = self.gui.get_checkbox_value(self.sel_all)
        for chk in self.checklist:
            self.gui.set_checkbox_value(chk, state)

    def invert_selection(self):
        """check unchecked and uncheck checked
        """
        for chk in self.checklist:
            self.gui.set_checkbox_value(chk, not self.gui.get_checkbox_value(chk))

    def confirm(self):
        "dialoog afsluiten"
        dirs = []
        for chk in self.checklist:
            if self.gui.get_checkbox_value(chk):
                if self.dofiles:
                    self.parent.names.remove(self.gui.get_checkbox_text(chk))
                else:
                    dirs.append(self.gui.get_checkbox_text(chk))
        if not self.dofiles:
            self.parent.names = dirs


class Results:
    """Show results on screen
    """
    helpinfo = ("Select a line and doubleclick or press Ctrl-G to open the indicated file\n"
                "at the indicated line (not in single file mode)")
    common_path_txt = 'De bestanden staan allemaal in of onder de directory "{}"'

    def __init__(self, parent, common_path=''):
        self.parent = parent
        self.common = common_path
        breedte = 50 if self.parent.mode == Mode.single.value else 150
        self.gui = gui.ResultsGui(self, parent.gui, parent.resulttitel, breedte)
        self.results = []
        label_txt = (f"{self.parent.do_checks.rpt[0]}"
                     f" ({len(self.parent.do_checks.results)} items)")
        if self.parent.mode == Mode.multi.value:
            label_txt += '\n' + self.common_path_txt.format(self.common.rstrip(os.sep))
        self.gui.add_top_text(label_txt)
        line, self.filelist = self.gui.add_combobox_line('Files checked:',
                                                         self.parent.do_checks.filenames)
        self.gui.add_button_to_line(line, "&Go To File", self.goto_result)
        # breakpoint()
        self.lijst = self.gui.add_results_list()
        self.populate_list()
        self.gui.add_buttons([("&Klaar", self.gui.accept), ("&Repeat Action", self.refresh),
                              ("Copy to &File(s)", self.kopie),
                              ("Copy to &Clipboard", self.to_clipboard)])

    def populate_list(self):
        """copy results to listbox
        """
        fname = self.gui.get_combobox_value(self.filelist)
        text = self.parent.do_checks.results[fname]
        self.gui.set_textbox_value(self.lijst, text)

    # def klaar(self):
    #     """finish dialog
    #     """
    #     self.gui.accept()

    def refresh(self):
        """callback for repeat action
        """
        self.results = []
        self.gui.set_textbox_value(self.lijst, "")
        self.parent.do_checks.rpt = ["".join(self.parent.do_checks.specs)]
        self.parent.gui.execute_action()
        self.populate_list()
        self.gui.set_combobox_value(self.filelist, 0)

    def kopie(self):
        """callback for button 'Copy to file'
        """
        ok = gui.show_dialog(QuietOptions(self).gui)
        if not ok:
            return
        if self.parent.newquietoptions['single_file']:
            fname = self.parent.get_output_filename(self.parent.newquietoptions['fname'])
            with open(fname, "w") as f_out:
                first_file = True
                for name, data in self.parent.do_checks.results.items():
                    if not first_file:
                        print('', file=f_out)
                        print('', file=f_out)
                    first_file = False
                    print(f'results for {name}', file=f_out)
                    print('', file=f_out)
                    print(data, file=f_out)
            msgstart = 'O'
        else:
            for name, data in self.parent.do_checks.results.items():
                fname = self.parent.get_output_filename(
                    self.parent.newquietoptions['pattern'], name)
                with open(fname, 'w') as f_out:
                    print(f'results for {name}', file=f_out)
                    print('', file=f_out)
                    print(data, file=f_out)
            msgstart = 'Last o'
        gui.show_message(self.gui, self.parent.title, f'{msgstart}utput saved as {fname}')

    def help(self):
        """suggest workflow
        """
        gui.show_message(self.gui, self.parent.title, self.helpinfo)

    def to_clipboard(self):
        """callback for button 'Copy to clipboard'
        """
        text = []
        first_file = True
        for name, data in self.parent.do_checks.results.items():
            if not first_file:
                text.extend(['', ''])
            first_file = False
            text.extend([f'results for {name}', '', data])
        self.gui.copy_to_clipboard('\n'.join(text))
        gui.show_message(self.gui, self.parent.title, 'Output copied to clipboard')

    def goto_result(self):
        """open the file containing the checked lines
        """
        fname = self.gui.get_combobox_value(self.filelist)
        prog, fileopt = self.parent.editor_option[:2]
        subprocess.run(prog + [fileopt.format(fname)], check=False)  # , lineopt.format(line)])
