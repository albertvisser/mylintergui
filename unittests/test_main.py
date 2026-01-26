"""unittests for ./app/main.py
"""
import types
import pytest
from app import main as testee


class MockLinterGui:
    "stub for gui.LinterGui"
    def __init__(self, *args, **kwargs):
        print('called LinterGui.__init__ with args', args, kwargs)

    def start_display(self):
        print('called LinterGui.start_display')

    def build_radiobutton_row(self, *args):
        print('called LinterGui.build_radiobutton_row with args', args)
        return args[0]

    def build_radiobutton_block(self, *args):
        print('called LinterGui.build_radiobutton_block with args', args)
        return args[0]

    def add_combobox_row(self, *args, **kwargs):
        print('called LinterGui.add_combobox_row with args', args, kwargs)
        return args[0]

    def show_single_mode_info(self, *args):
        print('called LinterGui.show_single_mode_info with args', args)

    def show_multi_mode_info(self, *args):
        print('called LinterGui.show_multi_mode_info with args', args)

    def add_checkbox_line(self, *args, **kwargs):
        print('called LinterGui.add_checkbox_line with args', args, kwargs)
        if 'spinner' in kwargs:
            return args[0], kwargs['spinner']
        return args[0], None

    def add_buttons(self, *args):
        print('called LinterGui.add_buttons with args', args)

    def finalize_display(self, *args):
        print('called LinterGui.finalize_display with args', args)

    def zoekdir(self):
        print('called LinterGui.zoekdir')

    def show(self):
        print('called LinterGui.show')

    def close(self):
        print('called LinterGui.close')

    def go(self):
        print('called LinterGui.go')

    def set_checkbox_value(self, *args):
        print('called LinterGui.set_checkbox_value with args', args)


class TestLinterApp:
    """unittests for main.LinterApp
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.LinterApp object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called LinterApp.__init__ with args', args)
        monkeypatch.setattr(testee.LinterApp, '__init__', mock_init)
        testobj = testee.LinterApp()
        testobj.gui = MockLinterGui()
        assert capsys.readouterr().out == ('called LinterApp.__init__ with args ()\n'
                                           "called LinterGui.__init__ with args () {}\n")
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for LinterApp.__init__
        """
        def mock_get_option(self):
            print('called LinterApp.get_editor_option')
        def mock_blacklist(self):
            print('called LinterApp.build_blacklist_if_needed')
        def mock_set_mode(self, *args):
            print('called LinterApp.set_mode with args', args)
            return 'xxx'
        def mock_set_parameters(self, *args):
            print('called LinterApp.set_parameters with args', args)
            self.skip_screen = False
        def mock_set_parameters_2(self, *args):
            print('called LinterApp.set_parameters with args', args)
            self.skip_screen = True
        def mock_setup_screen(self, *args):
            print('called LinterApp.setup_screen with args', args)
        def mock_doe(self, *args):
            print('called LinterApp.doe with args', args)
        monkeypatch.setattr(testee.LinterApp, 'get_editor_option', mock_get_option)
        monkeypatch.setattr(testee.LinterApp, 'build_blacklist_if_needed', mock_blacklist)
        monkeypatch.setattr(testee.LinterApp, 'set_mode', mock_set_mode)
        monkeypatch.setattr(testee.LinterApp, 'set_parameters', mock_set_parameters)
        monkeypatch.setattr(testee.LinterApp, 'setup_screen', mock_setup_screen)
        monkeypatch.setattr(testee.LinterApp, 'doe', mock_doe)
        monkeypatch.setattr(testee.gui, 'LinterGui', MockLinterGui)
        testobj = testee.LinterApp({'args': 'dict'})
        assert isinstance(testobj.gui, testee.gui.LinterGui)
        assert testobj.title == "Albert's linter GUI frontend"
        assert testobj.iconame == testee.iconame
        assert testobj.fouttitel == testobj.title + "- fout"
        assert testobj.resulttitel == testobj.title + " - Resultaten"
        assert testobj.common_part == ""
        assert testobj._mru_items == {"dirs": []}
        assert testobj.s == ''
        assert testobj.p == {"subdirs": False, "fromrepo": False}
        assert testobj._keys == ("dirs",)
        assert testobj._optionskey == "options"
        assert testobj._sections == ('dirs',)
        assert testobj.quiet_keys == ('dest', 'pattern', 'fname', 'ignore')
        assert testobj.quiet_options == {'dest': 'multi',
                                         'pattern': '~/.linters/<linter>/<ignore>/<filename>-<date>',
                                         'fname': '<linter>_results-<date>',
                                         'ignore': testee.os.path.expanduser('~/projects')}
        assert testobj._words == ('woord', 'woord', 'spec', 'pad', )
        assert testobj._optkeys == ("subdirs", "fromrepo")
        assert capsys.readouterr().out == (
            "called LinterApp.get_editor_option\n"
            "called LinterApp.build_blacklist_if_needed\n"
            "called LinterApp.set_mode with args ({'args': 'dict'},)\n"
            "called LinterApp.set_parameters with args ('xxx',)\n"
            f"called LinterGui.__init__ with args () {{'master': {testobj}}}\n"
            "called LinterApp.setup_screen with args ()\n"
            "called LinterGui.show\n"
            "called LinterGui.go\n")
        monkeypatch.setattr(testee.LinterApp, 'set_parameters', mock_set_parameters_2)
        testobj = testee.LinterApp({'args': 'dict'})
        assert isinstance(testobj.gui, testee.gui.LinterGui)
        assert testobj.title == "Albert's linter GUI frontend"
        assert testobj.iconame == testee.iconame
        assert testobj.fouttitel == testobj.title + "- fout"
        assert testobj.resulttitel == testobj.title + " - Resultaten"
        assert testobj.common_part == ""
        assert testobj._mru_items == {"dirs": []}
        assert testobj.s == ''
        assert testobj.p == {"subdirs": False, "fromrepo": False}
        assert testobj._keys == ("dirs",)
        assert testobj._optionskey == "options"
        assert testobj._sections == ('dirs',)
        assert testobj.quiet_keys == ('dest', 'pattern', 'fname', 'ignore')
        assert testobj.quiet_options == {'dest': 'multi',
                                         'pattern': '~/.linters/<linter>/<ignore>/<filename>-<date>',
                                         'fname': '<linter>_results-<date>',
                                         'ignore': testee.os.path.expanduser('~/projects')}
        assert testobj._words == ('woord', 'woord', 'spec', 'pad', )
        assert testobj._optkeys == ("subdirs", "fromrepo")
        assert capsys.readouterr().out == (
            "called LinterApp.get_editor_option\n"
            "called LinterApp.build_blacklist_if_needed\n"
            "called LinterApp.set_mode with args ({'args': 'dict'},)\n"
            "called LinterApp.set_parameters with args ('xxx',)\n"
            f"called LinterGui.__init__ with args () {{'master': {testobj}}}\n"
            "called LinterApp.setup_screen with args ()\n"
            "called LinterGui.show\n"
            "called LinterApp.doe with args ()\n"
            "called LinterGui.close\n")

    def test_setup_screen(self, monkeypatch, capsys, tmp_path):
        """unittest for LinterApp.setup_screen
        """
        monkeypatch.setattr(testee, 'checktypes', {'x': 'xxxx'})
        monkeypatch.setattr(testee, 'cmddict', {'a': 'aaa', 'b': 'bbb'})
        monkeypatch.setattr(testee, 'default_option', 'x')
        monkeypatch.setattr(testee, 'default_linter', 1)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mode = ''
        testobj.checking_type = ''
        testobj.p = {'filelist': [], 'subdirs': False}
        testobj._mru_items = {'dirs': []}
        testobj.dest_from_input = 'True'
        testobj.linter_from_input = ''
        testobj.repo_only = 'Yes'
        testobj.setup_screen()
        assert testobj.check_options == 'Type of check:'
        assert testobj.linters == 'Check using:'
        assert testobj.vraag_subs == 'ook subdirectories doorzoeken'
        assert testobj.vraag_links == 'symlinks volgen - max. diepte (-1 is onbeperkt):'
        assert testobj.vraag_diepte == (-1, 5)
        assert testobj.ask_skipdirs == 'selecteer (sub)directories om over te slaan'
        assert testobj.ask_skipfiles == 'selecteer bestanden om over te slaan'
        assert testobj.vraag_quiet == 'Output to file(s) directly'
        assert capsys.readouterr().out == (
                "called LinterGui.start_display\n"
                "called LinterGui.build_radiobutton_row with args"
                " ('Type of check:', [('&X', True)])\n"
                "called LinterGui.build_radiobutton_block with args"
                " ('Check using:', [('&a', False), ('&b', False)])\n"
                "called LinterGui.show_multi_mode_info with args"
                " ('In de volgende files/directories:', [])\n"
                "called LinterGui.add_checkbox_line with args"
                " ('Use global whitelist/blacklist',)"
                f" {{'toggle': True, 'button': ('Configure', {testobj.configure_filter})}}\n"
                "called LinterGui.add_checkbox_line with args"
                " ('ook subdirectories doorzoeken', False) {}\n"
                "called LinterGui.add_checkbox_line with args"
                " ('symlinks volgen - max. diepte (-1 is onbeperkt):',) {'spinner': (-1, 5)}\n"
                "called LinterGui.add_checkbox_line with args"
                " ('selecteer (sub)directories om over te slaan',) {}\n"
                "called LinterGui.add_checkbox_line with args"
                " ('selecteer bestanden om over te slaan',) {}\n"
                "called LinterGui.add_checkbox_line with args"
                " ('Output to file(s) directly',)"
                f" {{'toggle': 'True', 'button': ('Configure', {testobj.configure_quiet})}}\n"
                "called LinterGui.add_buttons with args"
                f" ([('&Uitvoeren', {testobj.doe}), ('&Einde', {testobj.gui.close})],)\n"
                "called LinterGui.finalize_display with args ('Check using:',)\n")

        testobj.mode = testee.Mode.standard.value
        testobj.p['filelist'] = [str(tmp_path)]
        testobj.setup_screen()
        assert testobj.check_options == 'Type of check:'
        assert testobj.linters == 'Check using:'
        assert testobj.vraag_dir == 'In directory:'
        assert testobj.vraag_repo == 'Check repository files only (also does subdirectories)'
        assert testobj.p['fromrepo'] == 'Yes'
        assert testobj.vraag_subs == 'ook subdirectories doorzoeken'
        assert testobj.vraag_links == 'symlinks volgen - max. diepte (-1 is onbeperkt):'
        assert testobj.vraag_diepte == (-1, 5)
        assert testobj.ask_skipdirs == 'selecteer (sub)directories om over te slaan'
        assert testobj.ask_skipfiles == 'selecteer bestanden om over te slaan'
        assert testobj.vraag_quiet == 'Output to file(s) directly'
        assert capsys.readouterr().out == (
                "called LinterGui.start_display\n"
                "called LinterGui.build_radiobutton_row with args"
                " ('Type of check:', [('&X', True)])\n"
                "called LinterGui.build_radiobutton_block with args"
                " ('Check using:', [('&a', False), ('&b', False)])\n"
                "called LinterGui.add_combobox_row with args ('In directory:', [])"
                f" {{'width': 200, 'initial': '{tmp_path}', 'callback': {testobj.check_loc},"
                f" 'button': ('&Zoek', {testobj.gui.zoekdir})}}\n"
                "called LinterGui.add_checkbox_line with args"
                " ('Use global whitelist/blacklist',)"
                f" {{'toggle': True, 'button': ('Configure', {testobj.configure_filter})}}\n"
                "called LinterGui.add_checkbox_line with args"
                " ('Check repository files only (also does subdirectories)', 'Yes') {}\n"
                "called LinterGui.add_checkbox_line with args"
                " ('ook subdirectories doorzoeken', False) {}\n"
                "called LinterGui.add_checkbox_line with args"
                " ('symlinks volgen - max. diepte (-1 is onbeperkt):',) {'spinner': (-1, 5)}\n"
                "called LinterGui.add_checkbox_line with args"
                " ('selecteer (sub)directories om over te slaan',) {}\n"
                "called LinterGui.add_checkbox_line with args"
                " ('selecteer bestanden om over te slaan',) {}\n"
                "called LinterGui.add_checkbox_line with args"
                " ('Output to file(s) directly',)"
                f" {{'toggle': 'True', 'button': ('Configure', {testobj.configure_quiet})}}\n"
                "called LinterGui.add_buttons with args"
                f" ([('&Uitvoeren', {testobj.doe}), ('&Einde', {testobj.gui.close})],)\n"
                "called LinterGui.finalize_display with args ('Check using:',)\n")

        testobj.mode = testee.Mode.single.value
        testobj.p['filelist'] = [str(tmp_path)]
        testobj.setup_screen()
        assert testobj.check_options == 'Type of check:'
        assert testobj.linters == 'Check using:'
        assert testobj.vraag_subs == 'ook subdirectories doorzoeken'
        assert testobj.vraag_links == 'symlinks volgen - max. diepte (-1 is onbeperkt):'
        assert testobj.vraag_diepte == (-1, 5)
        assert testobj.ask_skipdirs == 'selecteer (sub)directories om over te slaan'
        assert testobj.ask_skipfiles == 'selecteer bestanden om over te slaan'
        assert testobj.vraag_quiet == 'Output to file(s) directly'
        assert capsys.readouterr().out == (
                "called LinterGui.start_display\n"
                "called LinterGui.build_radiobutton_row with args"
                " ('Type of check:', [('&X', True)])\n"
                "called LinterGui.build_radiobutton_block with args"
                " ('Check using:', [('&a', False), ('&b', False)])\n"
                "called LinterGui.show_single_mode_info with args"
                f" ('In file/directory:', '{tmp_path}')\n"
                "called LinterGui.add_checkbox_line with args"
                " ('ook subdirectories doorzoeken', False) {}\n"
                "called LinterGui.add_checkbox_line with args"
                " ('symlinks volgen - max. diepte (-1 is onbeperkt):',) {'spinner': (-1, 5)}\n"
                "called LinterGui.add_checkbox_line with args"
                " ('selecteer (sub)directories om over te slaan',) {}\n"
                "called LinterGui.add_checkbox_line with args"
                " ('selecteer bestanden om over te slaan',) {}\n"
                "called LinterGui.add_checkbox_line with args"
                " ('Output to file(s) directly',)"
                f" {{'toggle': 'True', 'button': ('Configure', {testobj.configure_quiet})}}\n"
                "called LinterGui.add_buttons with args"
                f" ([('&Uitvoeren', {testobj.doe}), ('&Einde', {testobj.gui.close})],)\n"
                "called LinterGui.finalize_display with args ('Check using:',)\n")

        testobj.mode = testee.Mode.single.value
        testobj.p['filelist'] = [str(tmp_path / 'xxx')]
        testobj.setup_screen()
        assert testobj.check_options == 'Type of check:'
        assert testobj.linters == 'Check using:'
        assert testobj.vraag_subs == 'ook subdirectories doorzoeken'
        assert testobj.vraag_links == 'symlinks volgen - max. diepte (-1 is onbeperkt):'
        assert testobj.vraag_diepte == (-1, 5)
        assert testobj.ask_skipdirs == 'selecteer (sub)directories om over te slaan'
        assert testobj.ask_skipfiles == 'selecteer bestanden om over te slaan'
        assert testobj.vraag_quiet == 'Output to file(s) directly'
        assert capsys.readouterr().out == (
                "called LinterGui.start_display\n"
                "called LinterGui.build_radiobutton_row with args"
                " ('Type of check:', [('&X', True)])\n"
                "called LinterGui.build_radiobutton_block with args"
                " ('Check using:', [('&a', False), ('&b', False)])\n"
                "called LinterGui.show_single_mode_info with args"
                f" ('In file/directory:', '{tmp_path}/xxx')\n"
                "called LinterGui.add_checkbox_line with args"
                " ('Output to file(s) directly',)"
                f" {{'toggle': 'True', 'button': ('Configure', {testobj.configure_quiet})}}\n"
                "called LinterGui.add_buttons with args"
                f" ([('&Uitvoeren', {testobj.doe}), ('&Einde', {testobj.gui.close})],)\n"
                "called LinterGui.finalize_display with args ('Check using:',)\n")
        testobj.mode = testee.Mode.single.value
        testobj.p['filelist'] = [str(tmp_path)]
        testobj.setup_screen()
        assert testobj.check_options == 'Type of check:'
        assert testobj.linters == 'Check using:'
        assert testobj.vraag_subs == 'ook subdirectories doorzoeken'
        assert testobj.vraag_links == 'symlinks volgen - max. diepte (-1 is onbeperkt):'
        assert testobj.vraag_diepte == (-1, 5)
        assert testobj.ask_skipdirs == 'selecteer (sub)directories om over te slaan'
        assert testobj.ask_skipfiles == 'selecteer bestanden om over te slaan'
        assert testobj.vraag_quiet == 'Output to file(s) directly'
        assert capsys.readouterr().out == (
                "called LinterGui.start_display\n"
                "called LinterGui.build_radiobutton_row with args"
                " ('Type of check:', [('&X', True)])\n"
                "called LinterGui.build_radiobutton_block with args"
                " ('Check using:', [('&a', False), ('&b', False)])\n"
                "called LinterGui.show_single_mode_info with args"
                f" ('In file/directory:', '{tmp_path}')\n"
                "called LinterGui.add_checkbox_line with args"
                " ('ook subdirectories doorzoeken', False) {}\n"
                "called LinterGui.add_checkbox_line with args"
                " ('symlinks volgen - max. diepte (-1 is onbeperkt):',) {'spinner': (-1, 5)}\n"
                "called LinterGui.add_checkbox_line with args"
                " ('selecteer (sub)directories om over te slaan',) {}\n"
                "called LinterGui.add_checkbox_line with args"
                " ('selecteer bestanden om over te slaan',) {}\n"
                "called LinterGui.add_checkbox_line with args"
                " ('Output to file(s) directly',)"
                f" {{'toggle': 'True', 'button': ('Configure', {testobj.configure_quiet})}}\n"
                "called LinterGui.add_buttons with args"
                f" ([('&Uitvoeren', {testobj.doe}), ('&Einde', {testobj.gui.close})],)\n"
                "called LinterGui.finalize_display with args ('Check using:',)\n")

    def test_get_editor_option(self, monkeypatch, capsys, tmp_path):
        """unittest for LinterApp.get_editor_option
        """
        def mock_read(arg):
            print(f"called path.read with arg '{arg}'")
            raise FileNotFoundError
        def mock_read_2(arg):
            print(f"called path.read with arg '{arg}'")
            return "x = ['x', 'x', 'x']\ny = yyy\nz = zzz"
        def mock_write(arg, data):
            print(f"called path.write with arg '{arg}', '{data}'")
        mock_edfile = tmp_path / 'edfile'
        monkeypatch.setattr(testee, 'edfile', mock_edfile)
        monkeypatch.setattr(testee.pathlib.Path, 'read_text', mock_read)
        monkeypatch.setattr(testee.pathlib.Path, 'write_text', mock_write)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_editor_option()
        assert testobj.editor_option == [['SciTE'], '-open:{}', '-goto:{}']
        assert capsys.readouterr().out == (
            f"called path.read with arg '{mock_edfile}'\n"
            f"called path.write with arg '{mock_edfile}',"
            " 'program = 'SciTE'\nfile-option = '-open:{}'\nline-option = '-goto:{}''\n")
        monkeypatch.setattr(testee.pathlib.Path, 'read_text', mock_read_2)
        testobj.get_editor_option()
        assert testobj.editor_option == [['x', 'x', 'x'], 'yyy', 'zzz']
        assert capsys.readouterr().out == f"called path.read with arg '{mock_edfile}'\n"

    def test_build_blacklist_if_needed(self, monkeypatch, capsys, tmp_path):
        """unittest for LinterApp.build_blacklist_if_needed
        """
        original_open = testee.pathlib.Path.open
        def mock_open(arg):
            print(f"called path.open with arg '{arg.name}'")
            return original_open(arg)
        def mock_open_2(arg):
            print(f"called path.open with arg '{arg.name}'")
            raise FileNotFoundError
        def mock_load(arg):
            print(f"called json.load with arg '{arg.name}'")
            return {'x': 'y'}
        def mock_update():
            print('called LinterApp.update_blacklistfile')
        blacklistfile = tmp_path / 'blacklistfile'
        blacklistfile.write_text('blacklisted items')
        monkeypatch.setattr(testee.pathlib.Path, 'open', mock_open)
        monkeypatch.setattr(testee, 'blacklist', blacklistfile)
        monkeypatch.setattr(testee, 'initial_blacklist', {'initial': 'blacklist'})
        monkeypatch.setattr(testee.json, 'load', mock_load)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.update_blacklistfile = mock_update
        testobj.build_blacklist_if_needed()
        assert testobj.blacklist == {'x': 'y'}
        assert capsys.readouterr().out == ("called path.open with arg 'blacklistfile'\n"
                                           f"called json.load with arg '{blacklistfile}'\n")
        monkeypatch.setattr(testee.pathlib.Path, 'open', mock_open_2)
        testobj.build_blacklist_if_needed()
        assert testobj.blacklist == {'initial': 'blacklist'}
        assert capsys.readouterr().out == ("called path.open with arg 'blacklistfile'\n"
                                           "called LinterApp.update_blacklistfile\n")

    def test_set_mode(self, monkeypatch, capsys):
        """unittest for LinterApp.set_mode
        """
        def mock_get(name):
            print(f"called settings.get_project_dir with arg '{name}")
            return name
        # monkeypatch.setattr(testee, 'Mode', ...)  f of d of l
        monkeypatch.setattr(testee.settings, 'get_project_dir', mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        args = types.SimpleNamespace(c='linter', o='output_dest', s='skip_screen_switch',
                                     m='mode', r=None, f=None, d=None, l=None)
        assert testobj.set_mode(args) == ""
        assert testobj.linter_from_input == 'linter'
        assert testobj.dest_from_input == 'output_dest'
        assert testobj.skip_screen == 'skip_screen_switch'
        assert testobj.checking_type == 'mode'
        assert not testobj.repo_only
        assert capsys.readouterr().out == ""

        args = types.SimpleNamespace(c=None, o=None, s=None,
                                     m=None, r='reponame', f=None, d=None, l=None)
        assert testobj.set_mode(args) == "reponame"
        assert testobj.linter_from_input is None
        assert testobj.dest_from_input is None
        assert testobj.skip_screen is None
        assert testobj.checking_type is None
        assert testobj.repo_only
        assert capsys.readouterr().out == "called settings.get_project_dir with arg 'reponame\n"

        args = types.SimpleNamespace(c='linter', o='output_dest', s='skip_screen_switch',
                                     m='mode', f='filename', r=None, d=None, l=None)
        assert testobj.set_mode(args) == "filename"
        assert not testobj.repo_only
        assert capsys.readouterr().out == ""

        args = types.SimpleNamespace(c='linter', o='output_dest', s='skip_screen_switch',
                                     m='mode', d='dirname', f=None, r=None, l=None)
        assert testobj.set_mode(args) == "dirname"
        assert not testobj.repo_only
        assert capsys.readouterr().out == ""

        args = types.SimpleNamespace(c='linter', o='output_dest', s='skip_screen_switch',
                                     m='mode', l='listfilename', f=None, d=None, r=None)
        assert testobj.set_mode(args) == "listfilename"
        assert not testobj.repo_only
        assert capsys.readouterr().out == ""

    def test_set_parameters(self, monkeypatch, capsys):
        """unittest for LinterApp.set_parameters
        """
        def mock_readini(*args):
            print('called LinterApp.readini with args', args)
        def mock_expand(arg):
            print('called path.expanduser with arg', arg)
            return arg
        def mock_resolve(arg):
            print('called path.resolve with arg', arg)
            return arg
        def mock_get(arg):
            print('called testee.get_paths_from_file with arg', arg)
            return ['xxx', 'yyy']
        def mock_get_2(arg):
            print('called testee.get_paths_from_file with arg', arg)
            return []
        monkeypatch.setattr(testee.pathlib.Path, 'expanduser', mock_expand)
        monkeypatch.setattr(testee.pathlib.Path, 'resolve', mock_resolve)
        monkeypatch.setattr(testee, 'get_paths_from_file', mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.readini = mock_readini
        testobj.mode = testee.Mode.standard.value
        testobj.title = 'aaa'
        testobj.p = {}
        testobj.set_parameters('pathname')
        assert capsys.readouterr().out == (
            "called path.expanduser with arg pathname\n"
            "called path.resolve with arg pathname\n"
            "called LinterApp.readini with args (PosixPath('pathname'),)\n")
        testobj.set_parameters('')
        assert capsys.readouterr().out == "called LinterApp.readini with args ()\n"
        testobj.mode = testee.Mode.single.value
        testobj.set_parameters('pathname')
        assert capsys.readouterr().out == ("called path.resolve with arg pathname\n"
                                           "called LinterApp.readini with args (PosixPath('.'),)\n")
        with pytest.raises(ValueError) as exc:
            testobj.set_parameters('')
        assert str(exc.value) == 'Need filename for application type "single"'
        testobj.mode = testee.Mode.multi.value
        testobj.set_parameters(['pathname'])
        assert capsys.readouterr().out == ("called testee.get_paths_from_file with arg pathname\n"
                                           "called LinterApp.readini with args ('',)\n")
        monkeypatch.setattr(testee, 'get_paths_from_file', mock_get_2)
        with pytest.raises(ValueError) as exc:
            testobj.set_parameters(['pathname'])
        assert str(exc.value) == (
            'Input is not a usable file for multi mode: should contain (only) path names')
        testobj.set_parameters(['path/name1', 'path/name2'])
        assert capsys.readouterr().out == (
                "called testee.get_paths_from_file with arg pathname\n"
                "called LinterApp.readini with args ('path',)\n")
        with pytest.raises(ValueError) as exc:
            testobj.set_parameters([])
        assert str(exc.value) == (
            'Need filename or list of files for application type "multi"')
        testobj.mode = 'x'
        with pytest.raises(ValueError) as exc:
            testobj.set_parameters([])
        assert str(exc.value) == 'Execution mode could not be determined from input'

    def test_readini(self, monkeypatch, capsys, tmp_path):
        """unittest for LinterApp.readini
        """
        mock_iniloc = tmp_path / 'iniloc'
        def mock_get_iniloc(path):
            print(f"called get_iniloc with arg '{path}'")
            return mock_iniloc, mock_iniloc / 'mfile', mock_iniloc / 'ofile'
        counter = 0
        def mock_load(arg):
            nonlocal counter
            print(f"called json.load with arg '{arg.name}'")
            counter += 1
            if counter == 1:
                return {'x': 'y'}
            return {'a': 'aaa', 'b': 'bbb', 'ignore': '~xxx'}
        def mock_load_2(arg):
            nonlocal counter
            print(f"called json.load with arg '{arg.name}'")
            counter += 1
            if counter == 1:
                return {'x': 'y'}
            return {'a': 'aaa', 'b': 'bbb', 'ignore': 'xxx'}
        monkeypatch.setattr(testee, 'get_iniloc', mock_get_iniloc)
        monkeypatch.setattr(testee.json, 'load', mock_load)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._mru_items = {}
        testobj._optkeys = ['a', 'b', 'ignore']
        testobj.p = {}
        testobj.quiet_keys = ['a', 'ignore']
        testobj.quiet_options = {'a': 'c'}
        testobj.readini()
        assert testobj._mru_items == {}
        assert testobj.p == {}
        assert testobj.quiet_options == {'a': 'c'}
        assert capsys.readouterr().out == ("called get_iniloc with arg 'None'\n")

        mock_iniloc.mkdir(parents=True)
        testobj.p = {}
        testobj._mru_items = {}
        testobj.quiet_options = {'a': 'c'}
        testobj.readini('test')
        assert testobj._mru_items == {}
        assert testobj.p == {'a': False, 'b': False, 'ignore': False}
        assert testobj.quiet_options == {'a': 'c'}
        assert capsys.readouterr().out == ("called get_iniloc with arg 'test'\n")

        (mock_iniloc / 'mfile').touch()
        (mock_iniloc / 'ofile').touch()
        testobj.p = {}
        testobj._mru_items = {}
        testobj.quiet_options = {'a': 'c'}
        testobj.readini('test')
        assert testobj._mru_items == {'x': 'y'}
        assert testobj.p == {'a': 'aaa', 'b': 'bbb', 'ignore': '~xxx'}
        assert testobj.quiet_options == {'a': 'aaa'}
        assert capsys.readouterr().out == ("called get_iniloc with arg 'test'\n"
                                           f"called json.load with arg '{mock_iniloc / 'mfile'}'\n"
                                           f"called json.load with arg '{mock_iniloc / 'ofile'}'\n")

        counter = 0
        monkeypatch.setattr(testee.json, 'load', mock_load_2)
        testobj.p = {}
        testobj._mru_items = {}
        testobj.quiet_options = {'a': 'c'}
        testobj.readini('test')
        assert testobj._mru_items == {'x': 'y'}
        assert testobj.p == {'a': 'aaa', 'b': 'bbb', 'ignore': 'xxx'}
        assert testobj.quiet_options == {'a': 'aaa', 'ignore': 'xxx'}
        assert capsys.readouterr().out == ("called get_iniloc with arg 'test'\n"
                                           f"called json.load with arg '{mock_iniloc / 'mfile'}'\n"
                                           f"called json.load with arg '{mock_iniloc / 'ofile'}'\n")

    def test_schrijfini(self, monkeypatch, capsys, tmp_path):
        """unittest for LinterApp.schrijfini
        """
        mock_iniloc = tmp_path / 'iniloc'
        def mock_get_iniloc(path):
            print(f"called get_iniloc with arg '{path}'")
            return mock_iniloc, mock_iniloc / 'mfile', mock_iniloc / 'ofile'
        def mock_dump(data, file, **kwargs):
            print('called json.dump with args', data, file.name, kwargs)
        monkeypatch.setattr(testee, 'get_iniloc', mock_get_iniloc)
        monkeypatch.setattr(testee.json, 'dump', mock_dump)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._mru_items = {'q': 'qqq', 'r': 'rrr'}
        testobj.p = {'x': 'xxx', 'y': 'yyy'}
        testobj._optkeys = ['x']
        testobj.quiet_options = {'a': 'aaa', 'b': 'bbb'}
        testobj.quiet_keys = ['b']

        testobj.schrijfini()
        assert capsys.readouterr().out == ("called get_iniloc with arg 'None'\n"
                                           "called json.dump with args {'q': 'qqq', 'r': 'rrr'}"
                                           f" {mock_iniloc / 'mfile'} {{'indent': 4}}\n"
                                           "called json.dump with args {'x': 'xxx', 'b': 'bbb'}"
                                           f" {mock_iniloc / 'ofile'} {{'indent': 4}}\n")
        testobj.schrijfini('test')
        assert capsys.readouterr().out == ("called get_iniloc with arg 'test'\n"
                                           "called json.dump with args {'q': 'qqq', 'r': 'rrr'}"
                                           f" {mock_iniloc / 'mfile'} {{'indent': 4}}\n"
                                           "called json.dump with args {'x': 'xxx', 'b': 'bbb'}"
                                           f" {mock_iniloc / 'ofile'} {{'indent': 4}}\n")

    def test_update_blacklistfile(self, monkeypatch, capsys, tmp_path):
        """unittest for LinterApp.update_blacklistfile
        """
        original_open = testee.pathlib.Path.open
        def mock_open(arg, mode):
            print(f"called path.open with arg '{arg.name}' '{mode}'")
            return original_open(arg)
        def mock_dump(data, stream, **kwargs):
            print(f"called json.dump with args '{data}' '{stream.name}'", kwargs)
        blacklistfile = tmp_path / 'blacklistfile'
        blacklistfile.write_text('blacklisted items')
        monkeypatch.setattr(testee.pathlib.Path, 'open', mock_open)
        monkeypatch.setattr(testee, 'blacklist', blacklistfile)
        monkeypatch.setattr(testee.json, 'dump', mock_dump)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.blacklist = 'blacklistdata'
        testobj.update_blacklistfile()
        assert capsys.readouterr().out == (
            "called path.open with arg 'blacklistfile' 'w'\n"
            f"called json.dump with args 'blacklistdata' '{blacklistfile}' {{'indent': 4}}\n")

    def test_doe(self, monkeypatch, capsys, tmp_path):
        """unittest for LinterApp.doe
        """
        def mock_check():
            print('called LinterApp.check_screen_input')
            return 'screeninfo error'
        def mock_check_2():
            print('called LinterApp.check_screen_input')
            return ''
        def mock_meld_fout(*args):
            print('called Gui.meld_fout with args', args)
        def mock_meld_info(*args):
            print('called Gui.meld_info with args', args)
        def mock_schrijf(loc):
            print(f"called LinterApp.schrijfini with arg '{loc}'")
        def mock_init(self, **p):
            print('called Linter.__init__ with args', p)
            self.ok = False
            self.rpt = ["Something went", "wrong"]
        def mock_init_2(self, **p):
            print('called Linter.__init__ with args', p)
            self.ok = True
            self.filenames = []
        def mock_init_3(self, **p):
            print('called Linter.__init__ with args', p)
            self.ok = True
            self.filenames = [target]
        def mock_determine():
            print('called LinterApp.mock_determine_items_to_skip')
            return True
        def mock_determine_2():
            print('called LinterApp.mock_determine_items_to_skip')
            return False
        def mock_is_lintable(arg):
            print(f'called is_lintable with arg {arg}')
            return True
        def mock_is_lintable_2(arg):
            print(f'called is_lintable with arg {arg}')
            return False
        def mock_execute():
            print('called Gui.execute_action')
        def mock_init_results(self, *args):
            print('called Results.__init__ with args', args)
            self.gui = 'ResultsGui'
        def mock_show(*args, **kwargs):
            print('called show_dialog with args', args, kwargs)
        target = tmp_path / 'filename'
        target.touch()
        link = tmp_path / 'linkname'
        link.symlink_to(target)
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
        monkeypatch.setattr(testee, 'is_lintable', mock_is_lintable)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p = {}
        testobj.check_screen_input = mock_check
        testobj.gui.meld_fout = mock_meld_fout
        testobj.gui.meld_info = mock_meld_info
        testobj.check_options = 'check-options'
        testobj.linters = 'linters'
        testobj.vraag_dir = 'dir'
        testobj.vraag_repo = 'repo'
        testobj.vraag_subs = 'subdirs'
        testobj.vraag_links = 'links'
        testobj.vraag_diepte = 'depth'
        testobj.vraag_quiet = 'quiet'
        testobj.gui.execute_action = mock_execute
        testobj.schrijfini = mock_schrijf
        testobj.determine_items_to_skip = mock_determine
        monkeypatch.setattr(testee.Linter, '__init__', mock_init)
        monkeypatch.setattr(testee.Results, '__init__', mock_init_results)
        testobj.doe()
        assert capsys.readouterr().out == (
            "called LinterApp.check_screen_input\n"
            "called Gui.meld_fout with args ('screeninfo error',)\n")
        testobj.check_screen_input = mock_check_2
        testobj.blacklist = {'black': 'list'}
        testobj.p['filelist'] = [target]
        testobj.skip_screen = True
        testobj.doe()
        assert isinstance(testobj.do_checks, testee.Linter)
        assert not testobj.do_checks.ok
        # assert testobj.do_checks.filenames == []
        assert testobj.p['filelist'] == [target]
        assert capsys.readouterr().out == (
            "called LinterApp.check_screen_input\n"
            f"called Linter.__init__ with args {{'filelist': [{target!r}],"
            " 'blacklist': {'black': 'list'}}\n"
            "called Gui.meld_info with args ('Something went\\nwrong',)\n")
        monkeypatch.setattr(testee.Linter, '__init__', mock_init_2)

        testobj.skip_screen = False
        testobj.doe()
        assert isinstance(testobj.do_checks, testee.Linter)
        assert testobj.do_checks.ok
        assert testobj.do_checks.filenames == []
        assert testobj.p['filelist'] == [target]
        assert capsys.readouterr().out == (
            "called LinterApp.check_screen_input\n"
            f"called LinterApp.schrijfini with arg '{tmp_path}'\n"
            f"called Linter.__init__ with args {{'filelist': [{target!r}],"
            " 'blacklist': {'black': 'list'}}\n"
            "called Gui.meld_info with args ('Geen (lintbare) bestanden gevonden',)\n")
        monkeypatch.setattr(testee.Linter, '__init__', mock_init_3)
        testobj.common_part = 'common part'
        testobj.doe()
        assert isinstance(testobj.do_checks, testee.Linter)
        assert testobj.do_checks.ok
        assert testobj.do_checks.filenames == [target]
        assert testobj.p['filelist'] == [target]
        assert capsys.readouterr().out == (
            "called LinterApp.check_screen_input\n"
            f"called LinterApp.schrijfini with arg '{tmp_path}'\n"
            f"called Linter.__init__ with args {{'filelist': [{target!r}],"
            " 'blacklist': {'black': 'list'}}\n"
            f"called is_lintable with arg {target}\n"
            "called Gui.execute_action\n"
            f"called Results.__init__ with args ({testobj}, 'common part')\n"
            "called show_dialog with args ('ResultsGui',) {}\n")
        testobj.p['filelist'] = [tmp_path]
        testobj.doe()
        assert isinstance(testobj.do_checks, testee.Linter)
        assert testobj.do_checks.ok
        assert testobj.do_checks.filenames == [target]
        assert testobj.p['filelist'] == [target.parent]
        assert capsys.readouterr().out == (
            "called LinterApp.check_screen_input\n"
            f"called LinterApp.schrijfini with arg '{tmp_path.parent}'\n"
            f"called Linter.__init__ with args {{'filelist': [{tmp_path!r}],"
            " 'blacklist': {'black': 'list'}}\n"
            "called LinterApp.mock_determine_items_to_skip\n")
        testobj.p['filelist'] = [target, tmp_path]
        testobj.determine_items_to_skip = mock_determine_2
        testobj.doe()
        assert isinstance(testobj.do_checks, testee.Linter)
        assert testobj.do_checks.ok
        assert testobj.do_checks.filenames == [target]
        assert testobj.p['filelist'] == [target, target.parent]
        assert capsys.readouterr().out == (
            "called LinterApp.check_screen_input\n"
            f"called LinterApp.schrijfini with arg '{target.parent}'\n"
            f"called Linter.__init__ with args {{'filelist': [{target!r}, {tmp_path!r}],"
            " 'blacklist': {'black': 'list'}}\n"
            "called LinterApp.mock_determine_items_to_skip\n"
            f"called is_lintable with arg {target}\n"
            "called Gui.execute_action\n"
            f"called Results.__init__ with args ({testobj}, 'common part')\n"
            "called show_dialog with args ('ResultsGui',) {}\n")
        monkeypatch.setattr(testee, 'is_lintable', mock_is_lintable_2)
        testobj.doe()
        assert isinstance(testobj.do_checks, testee.Linter)
        assert testobj.do_checks.ok
        assert testobj.do_checks.filenames == []
        assert testobj.p['filelist'] == [target, target.parent]
        assert capsys.readouterr().out == (
            "called LinterApp.check_screen_input\n"
            f"called LinterApp.schrijfini with arg '{target.parent}'\n"
            f"called Linter.__init__ with args {{'filelist': [{target!r}, {tmp_path!r}],"
            " 'blacklist': {'black': 'list'}}\n"
            "called LinterApp.mock_determine_items_to_skip\n"
            f"called is_lintable with arg {target}\n"
            "called Gui.meld_info with args ('Geen (lintbare) bestanden gevonden',)\n")

    def test_screen_input_check_type(self, monkeypatch, capsys):
        """unittest for LinterApp.check_screen_input
        """
        def mock_check_radio(*args):
            print('called Gui.get_radiogroup_checked with args', args)
            return 'radiobutton'
        def mock_check_type(*args):
            print('called LinterApp.check_type with args', args)
            return 'check_type failed'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mode = ''
        testobj.check_options = 'options'
        testobj.gui.get_radiogroup_checked = mock_check_radio
        testobj.check_type = mock_check_type
        assert testobj.check_screen_input() == 'check_type failed'
        assert capsys.readouterr().out == (
            "called Gui.get_radiogroup_checked with args ('options',)\n"
            "called LinterApp.check_type with args ('radiobutton',)\n")

    def test_screen_input_check_linter(self, monkeypatch, capsys):
        """unittest for LinterApp.check_screen_input
        """
        def mock_check_radio(*args):
            print('called Gui.get_radiogroup_checked with args', args)
            return 'radiobutton'
        def mock_check_type(*args):
            print('called LinterApp.check_type with args', args)
            return ''
        def mock_check_linter(*args):
            print('called LinterApp.check_linter with args', args)
            return 'check_linter failed'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mode = ''
        testobj.check_options = 'options'
        testobj.linters = 'linters'
        testobj.gui.get_radiogroup_checked = mock_check_radio
        testobj.check_type = mock_check_type
        testobj.check_linter = mock_check_linter
        assert testobj.check_screen_input() == 'check_linter failed'
        assert capsys.readouterr().out == (
            "called Gui.get_radiogroup_checked with args ('options',)\n"
            "called LinterApp.check_type with args ('radiobutton',)\n"
            "called Gui.get_radiogroup_checked with args ('linters',)\n"
            "called LinterApp.check_linter with args ('radiobutton',)\n")

    def test_screen_input_check_path(self, monkeypatch, capsys):
        """unittest for LinterApp.check_screen_input
        """
        def mock_check_radio(*args):
            print('called Gui.get_radiogroup_checked with args', args)
            return 'radiobutton'
        def mock_check_type(*args):
            print('called LinterApp.check_type with args', args)
            return ''
        def mock_check_linter(*args):
            print('called LinterApp.check_linter with args', args)
            return ''
        def mock_check_combo(*args):
            print('called Gui.get_combobox_textvalue with args', args)
            return 'combobox'
        def mock_checkpath(*args):
            print('called LinterApp.checkpath with args', args)
            return 'checkpath failed'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mode = testee.Mode.standard.value
        testobj.check_options = 'options'
        testobj.linters = 'linters'
        testobj.vraag_dir = 'dir'
        testobj.gui.get_radiogroup_checked = mock_check_radio
        testobj.check_type = mock_check_type
        testobj.gui.get_combobox_textvalue = mock_check_combo
        testobj.check_linter = mock_check_linter
        testobj.checkpath = mock_checkpath
        assert testobj.check_screen_input() == 'checkpath failed'
        assert capsys.readouterr().out == (
            "called Gui.get_radiogroup_checked with args ('options',)\n"
            "called LinterApp.check_type with args ('radiobutton',)\n"
            "called Gui.get_radiogroup_checked with args ('linters',)\n"
            "called LinterApp.check_linter with args ('radiobutton',)\n"
            "called Gui.get_combobox_textvalue with args ('dir',)\n"
            "called LinterApp.checkpath with args ('combobox',)\n")

    def test_screen_input_check_repo(self, monkeypatch, capsys):
        """unittest for LinterApp.check_screen_input
        """
        def mock_check_radio(*args):
            print('called Gui.get_radiogroup_checked with args', args)
            return 'radiobutton'
        def mock_check_type(*args):
            print('called LinterApp.check_type with args', args)
            return ''
        def mock_check_linter(*args):
            print('called LinterApp.check_linter with args', args)
            return ''
        def mock_check_combo(*args):
            print('called Gui.get_combobox_textvalue with args', args)
            return 'combobox'
        def mock_checkpath(*args):
            print('called LinterApp.checkpath with args', args)
            return ''
        def mock_check_check(*args):
            print('called Gui.get_checkbox_value with args', args)
            return 'checkbox'
        def mock_checkrepo(*args):
            print('called LinterApp.checkrepo with args', args)
            return 'checkrepo failed'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mode = testee.Mode.standard.value
        testobj.check_options = 'options'
        testobj.linters = 'linters'
        testobj.vraag_dir = 'dir'
        testobj.vraag_repo = 'repo'
        testobj.gui.get_radiogroup_checked = mock_check_radio
        testobj.check_type = mock_check_type
        testobj.gui.get_combobox_textvalue = mock_check_combo
        testobj.check_linter = mock_check_linter
        testobj.checkpath = mock_checkpath
        testobj.gui.get_checkbox_value = mock_check_check
        testobj.checkrepo = mock_checkrepo
        assert testobj.check_screen_input() == 'checkrepo failed'
        assert capsys.readouterr().out == (
            "called Gui.get_radiogroup_checked with args ('options',)\n"
            "called LinterApp.check_type with args ('radiobutton',)\n"
            "called Gui.get_radiogroup_checked with args ('linters',)\n"
            "called LinterApp.check_linter with args ('radiobutton',)\n"
            "called Gui.get_combobox_textvalue with args ('dir',)\n"
            "called LinterApp.checkpath with args ('combobox',)\n"
            "called Gui.get_checkbox_value with args ('repo',)\n"
            "called Gui.get_combobox_textvalue with args ('dir',)\n"
            "called LinterApp.checkrepo with args ('checkbox', 'combobox')\n")

    def test_screen_input_check_quiet(self, monkeypatch, capsys, tmp_path):
        """unittest for LinterApp.check_screen_input
        """
        def mock_check_radio(*args):
            print('called Gui.get_radiogroup_checked with args', args)
            return 'radiobutton'
        def mock_check_type(*args):
            print('called LinterApp.check_type with args', args)
            return ''
        def mock_check_linter(*args):
            print('called LinterApp.check_linter with args', args)
            return ''
        def mock_check_combo(*args):
            print('called Gui.get_combobox_textvalue with args', args)
            return 'combobox'
        def mock_checkpath(*args):
            print('called LinterApp.checkpath with args', args)
            return ''
        def mock_check_check(*args):
            print('called Gui.get_checkbox_value with args', args)
            if args[0] == 'subs':
                return ''
            return 'checkbox'
        def mock_check_check_2(*args):
            print('called Gui.get_checkbox_value with args', args)
            return 'checkbox'
        def mock_checkrepo(*args):
            print('called LinterApp.checkrepo with args', args)
            return ''
        def mock_check_spin(*args):
            print('called Gui.get_spinbox_value with args', args)
            return 'spinbox'
        def mock_check_quiet_options(*args):
            print('called LinterApp.check_quiet_options with args', args)
            return 'check_quiet_options failed'
        def mock_check_quiet_options_2(*args):
            print('called LinterApp.check_quiet_options with args', args)
            return ''
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mode = testee.Mode.single.value
        target = tmp_path / 'filename'
        target.touch()
        link = tmp_path / 'linkname'
        link.symlink_to(target)
        testobj.p = {'filelist': [target]}
        testobj.s = ""
        testobj.check_options = 'options'
        testobj.linters = 'linters'
        testobj.vraag_dir = 'dir'
        testobj.vraag_repo = 'repo'
        testobj.vraag_subs = 'subs'
        testobj.vraag_links = 'links'
        testobj.vraag_diepte = 'depth'
        testobj.gui.get_radiogroup_checked = mock_check_radio
        testobj.check_type = mock_check_type
        testobj.gui.get_combobox_textvalue = mock_check_combo
        testobj.check_linter = mock_check_linter
        testobj.checkpath = mock_checkpath
        testobj.gui.get_checkbox_value = mock_check_check
        testobj.gui.get_spinbox_value = mock_check_spin
        testobj.checkrepo = mock_checkrepo
        testobj.check_quiet_options = mock_check_quiet_options
        assert testobj.check_screen_input() == 'check_quiet_options failed'
        assert capsys.readouterr().out == (
            "called Gui.get_radiogroup_checked with args ('options',)\n"
            "called LinterApp.check_type with args ('radiobutton',)\n"
            "called Gui.get_radiogroup_checked with args ('linters',)\n"
            "called LinterApp.check_linter with args ('radiobutton',)\n"
            # "called Gui.get_combobox_textvalue with args ('dir',)\n"
            # "called LinterApp.checkpath with args ('combobox',)\n"
            # "called Gui.get_checkbox_value with args ('repo',)\n"
            # "called Gui.get_combobox_textvalue with args ('dir',)\n"
            # "called LinterApp.checkrepo with args ('checkbox', 'combobox')\n"
            # "called Gui.get_checkbox_value with args ('subdirs',)\n"
            # "called Gui.get_checkbox_value with args ('links',)\n"
            # "called Gui.get_spinbox_value with args ('depth',)\n"
            # "called LinterApp.checksubs with args ('checkbox', 'checkbox', 'spinbox')\n"
            # "called Gui.get_checkbox_value with args ('quiet',)\n"
            "called LinterApp.check_quiet_options with args ()\n")
        testobj.check_quiet_options = mock_check_quiet_options_2
        assert testobj.check_screen_input() == ''
        assert capsys.readouterr().out == (
            "called Gui.get_radiogroup_checked with args ('options',)\n"
            "called LinterApp.check_type with args ('radiobutton',)\n"
            "called Gui.get_radiogroup_checked with args ('linters',)\n"
            "called LinterApp.check_linter with args ('radiobutton',)\n"
            # "called LinterApp.checksubs with args ('checkbox', 'checkbox', 'spinbox')\n"
            # "called Gui.get_checkbox_value with args ('quiet',)\n"
            "called LinterApp.check_quiet_options with args ()\n")
        # mode single em eerste filelist item is link
        testobj.p['filelist'] = [link]
        assert testobj.check_screen_input() == ''
        assert testobj.p['follow_symlinks']
        assert not testobj.s
        assert capsys.readouterr().out == (
            "called Gui.get_radiogroup_checked with args ('options',)\n"
            "called LinterApp.check_type with args ('radiobutton',)\n"
            "called Gui.get_radiogroup_checked with args ('linters',)\n"
            "called LinterApp.check_linter with args ('radiobutton',)\n"
            "called LinterApp.check_quiet_options with args ()\n")
        # mode single em eerste filelist item is dir
        testobj.p['filelist'] = [tmp_path]  # gegearandeerd een directory
        assert testobj.check_screen_input() == ''
        assert testobj.p['follow_symlinks']
        assert not testobj.s
        assert capsys.readouterr().out == (
            "called Gui.get_radiogroup_checked with args ('options',)\n"
            "called LinterApp.check_type with args ('radiobutton',)\n"
            "called Gui.get_radiogroup_checked with args ('linters',)\n"
            "called LinterApp.check_linter with args ('radiobutton',)\n"
            "called Gui.get_checkbox_value with args ('subs',)\n"
            "called Gui.get_checkbox_value with args ('links',)\n"
            "called Gui.get_spinbox_value with args ('depth',)\n"
            "called LinterApp.check_quiet_options with args ()\n")
        # mode niet single em eerste filelist item is dir
        testobj.mode = testee.Mode.standard.value
        testobj.p['follow_symlinks'] = False
        assert testobj.check_screen_input() == ''
        assert testobj.p['follow_symlinks'] == 'checkbox'
        assert not testobj.s
        assert capsys.readouterr().out == (
            "called Gui.get_radiogroup_checked with args ('options',)\n"
            "called LinterApp.check_type with args ('radiobutton',)\n"
            "called Gui.get_radiogroup_checked with args ('linters',)\n"
            "called LinterApp.check_linter with args ('radiobutton',)\n"
            "called Gui.get_combobox_textvalue with args ('dir',)\n"
            "called LinterApp.checkpath with args ('combobox',)\n"
            "called Gui.get_checkbox_value with args ('repo',)\n"
            "called Gui.get_combobox_textvalue with args ('dir',)\n"
            "called LinterApp.checkrepo with args ('checkbox', 'combobox')\n"
            "called Gui.get_checkbox_value with args ('subs',)\n"
            "called Gui.get_checkbox_value with args ('links',)\n"
            "called Gui.get_spinbox_value with args ('depth',)\n"
            "called LinterApp.check_quiet_options with args ()\n")
        # mode niet single em eerste filelist item is file
        testobj.p['filelist'] = [target]
        testobj.p['follow_symlinks'] = False
        assert testobj.check_screen_input() == ''
        assert testobj.p['follow_symlinks'] == 'checkbox'
        assert not testobj.s
        assert capsys.readouterr().out == (
            "called Gui.get_radiogroup_checked with args ('options',)\n"
            "called LinterApp.check_type with args ('radiobutton',)\n"
            "called Gui.get_radiogroup_checked with args ('linters',)\n"
            "called LinterApp.check_linter with args ('radiobutton',)\n"
            "called Gui.get_combobox_textvalue with args ('dir',)\n"
            "called LinterApp.checkpath with args ('combobox',)\n"
            "called Gui.get_checkbox_value with args ('repo',)\n"
            "called Gui.get_combobox_textvalue with args ('dir',)\n"
            "called LinterApp.checkrepo with args ('checkbox', 'combobox')\n"
            "called Gui.get_checkbox_value with args ('subs',)\n"
            "called Gui.get_checkbox_value with args ('links',)\n"
            "called Gui.get_spinbox_value with args ('depth',)\n"
            "called LinterApp.check_quiet_options with args ()\n")
        # vraag_subs "aangekruist"
        testobj.gui.get_checkbox_value = mock_check_check_2
        testobj.p['follow_symlinks'] = False
        assert testobj.check_screen_input() == ''
        assert testobj.p['follow_symlinks'] == 'checkbox'
        assert testobj.s == ' en onderliggende directories'
        assert capsys.readouterr().out == (
            "called Gui.get_radiogroup_checked with args ('options',)\n"
            "called LinterApp.check_type with args ('radiobutton',)\n"
            "called Gui.get_radiogroup_checked with args ('linters',)\n"
            "called LinterApp.check_linter with args ('radiobutton',)\n"
            "called Gui.get_combobox_textvalue with args ('dir',)\n"
            "called LinterApp.checkpath with args ('combobox',)\n"
            "called Gui.get_checkbox_value with args ('repo',)\n"
            "called Gui.get_combobox_textvalue with args ('dir',)\n"
            "called LinterApp.checkrepo with args ('checkbox', 'combobox')\n"
            "called Gui.get_checkbox_value with args ('subs',)\n"
            "called Gui.get_checkbox_value with args ('links',)\n"
            "called Gui.get_spinbox_value with args ('depth',)\n"
            "called LinterApp.check_quiet_options with args ()\n")

    def test_check_loc(self, monkeypatch, capsys, tmp_path):
        """unittest for LinterApp.check_loc
        """
        def mock_readini(arg):
            print(f'called LinterApp.readini with arg {arg}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p = {"subdirs": "x", "fromrepo": "y"}
        testobj.readini = mock_readini
        testobj.vraag_subs = "subs"
        testobj.vraag_repo = "repo"
        file = tmp_path / "test"
        txt = str(file)
        testobj.check_loc(txt)
        assert capsys.readouterr().out == ""
        file.touch()
        testobj.check_loc(txt + '/')
        assert capsys.readouterr().out == ""
        testobj.check_loc(txt)
        assert capsys.readouterr().out == (
            f"called LinterApp.readini with arg {txt}\n"
            "called LinterGui.set_checkbox_value with args ('subs', 'x')\n"
            "called LinterGui.set_checkbox_value with args ('repo', 'y')\n")

    def test_check_type(self, monkeypatch, capsys):
        """unittest for LinterApp.check_type
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p = {'mode': None}
        assert testobj.check_type('') == "Please select a check type"
        assert testobj.p["mode"] is None
        assert testobj.check_type('x') == ""
        assert testobj.p["mode"] == "x"

    def test_check_linter(self, monkeypatch, capsys):
        """unittest for LinterApp.check_linter
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p = {'linter': None}
        assert testobj.check_linter('') == "Please choose a linter to use"
        assert testobj.p["linter"] is None
        assert testobj.check_linter('x') == ""
        assert testobj.p["linter"] == "x"

    def test_checkpath(self, monkeypatch, capsys, tmp_path):
        """unittest for LinterApp.checkpath
        """
        def mock_expand(arg):
            print('called path.expanduser')
            return arg
        def mock_resolve(arg):
            print('called path.resolve')
            raise FileNotFoundError
        def mock_resolve_2(arg):
            print('called path.resolve')
            return arg
        monkeypatch.setattr(testee.pathlib.Path, 'expanduser', mock_expand)
        monkeypatch.setattr(testee.pathlib.Path, 'resolve', mock_resolve)
        path_to_check = ''
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._mru_items = {"dirs": []}
        testobj.s = 'xxx'
        testobj.p = {}
        assert testobj.checkpath(path_to_check) == "Please enter or select a directory"
        assert capsys.readouterr().out == ""
        path_to_check = tmp_path / 'test'
        assert not path_to_check.exists()
        assert testobj.checkpath(path_to_check) == "De opgegeven directory bestaat niet"
        assert capsys.readouterr().out == ("called path.expanduser\ncalled path.resolve\n")
        monkeypatch.setattr(testee.pathlib.Path, 'resolve', mock_resolve_2)
        assert testobj.checkpath(path_to_check) == ""
        assert testobj._mru_items == {"dirs": [str(path_to_check)]}
        assert testobj.s == f'xxx\nin {path_to_check}'
        assert testobj.p["filelist"] == [str(path_to_check)]
        assert capsys.readouterr().out == ("called path.expanduser\ncalled path.resolve\n")

    def test_check_quiet_options(self, monkeypatch, capsys):
        """unittest for LinterApp.check_quiet_options
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.quiet_options = {}
        assert testobj.check_quiet_options() == "Please configure all options for quiet mode"
        testobj.quiet_options['dest'] = 'xxx'
        testobj.quiet_options['pattern'] = 'yyy'
        assert testobj.check_quiet_options() == "Please configure all options for quiet mode"
        testobj.quiet_options['dest'] = 'single'
        testobj.quiet_options['pattern'] = 'yyy'
        assert testobj.check_quiet_options() == ""
        testobj.quiet_options['dest'] = 'multi'
        testobj.quiet_options['pattern'] = ''
        assert testobj.check_quiet_options() == "Please configure all options for quiet mode"
        testobj.quiet_options['dest'] = ''
        testobj.quiet_options['pattern'] = 'yyy'
        assert testobj.check_quiet_options() == "Please configure all options for quiet mode"

    def test_checkrepo(self, monkeypatch, capsys, tmp_path):
        """unittest for LinterApp.checkrepo
        """
        def mock_run(*args, **kwargs):
            print('called subprocess.run with args', args, kwargs)
            return types.SimpleNamespace(stdout=b'xxxx\nyyyy\nzzzz\n')
        def mock_is_lintable(arg):
            print(f"called is_lintable with arg '{arg}'")
            return not arg.name == 'yyyy'
        monkeypatch.setattr(testee, 'DO_NOT_LINT', ['no'])
        monkeypatch.setattr(testee, 'is_lintable', mock_is_lintable)
        monkeypatch.setattr(testee.subprocess, 'run', mock_run)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p = {}
        assert testobj.checkrepo(False, 'path/to/repo') == ""
        assert not testobj.p["fromrepo"]
        assert capsys.readouterr().out == ""

        assert testobj.checkrepo(True, 'no') == (
            "De opgegeven repository is aangemerkt als do-not-lint")
        assert testobj.p["fromrepo"]
        assert capsys.readouterr().out == ""

        repoloc = tmp_path / 'repo'
        repoloc.mkdir()
        assert testobj.checkrepo(True, repoloc) == (
            "De opgegeven directory is geen (hg of git) repository")
        assert testobj.p["fromrepo"]
        assert capsys.readouterr().out == ""

        testobj.p['filelist'] = []
        (repoloc / '.hg').mkdir()
        assert testobj.checkrepo(True, repoloc) == ""
        assert testobj.p["fromrepo"]
        assert testobj.p['filelist'] == [f"{repoloc / 'xxxx'}", f"{repoloc / 'zzzz'}"]
        assert capsys.readouterr().out == (
            f"called subprocess.run with args (['hg', 'manifest'],) {{'cwd': '{repoloc}',"
            " 'stdout': -1, 'check': False}\n"
            f"called is_lintable with arg '{repoloc}/xxxx'\n"
            f"called is_lintable with arg '{repoloc}/yyyy'\n"
            f"called is_lintable with arg '{repoloc}/zzzz'\n")
        testobj.p['filelist'] = []
        (repoloc / '.git').mkdir()
        assert testobj.checkrepo(True, repoloc) == ""
        assert testobj.p["fromrepo"]
        assert testobj.p['filelist'] == [f"{repoloc / 'xxxx'}", f"{repoloc / 'zzzz'}"]
        assert capsys.readouterr().out == (
            f"called subprocess.run with args (['git', 'ls-files'],) {{'cwd': '{repoloc}',"
            " 'stdout': -1, 'check': False}\n"
            f"called is_lintable with arg '{repoloc}/xxxx'\n"
            f"called is_lintable with arg '{repoloc}/yyyy'\n"
            f"called is_lintable with arg '{repoloc}/zzzz'\n")

    def test_configure_quiet(self, monkeypatch, capsys):
        """unittest for LinterApp.configure_quiet
        """
        def mock_show(*args):
            print('called gui.show_dialog with args', args)
            return False
        def mock_show_2(*args):
            print('called gui.show_dialog with args', args)
            return True
        def mock_init(self, *args):
            print('called QuietOptions.__init__ with args', args)
            self.gui = 'QuietOptionsGui'
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
        monkeypatch.setattr(testee.QuietOptions, '__init__', mock_init)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.quiet_options = {}
        testobj.gui.newquietoptions = {}
        testobj.configure_quiet()
        assert testobj.quiet_options == {}
        assert capsys.readouterr().out == (
            f"called QuietOptions.__init__ with args ({testobj},)\n"
            "called gui.show_dialog with args ('QuietOptionsGui',)\n")
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_2)
        testobj.gui.newquietoptions = {'single_file': False, 'fname': '', 'pattern': ''}
        testobj.configure_quiet()
        assert testobj.quiet_options == {'dest': testee.Mode.multi.name}
        assert capsys.readouterr().out == (
            f"called QuietOptions.__init__ with args ({testobj},)\n"
            "called gui.show_dialog with args ('QuietOptionsGui',)\n")
        testobj.quiet_options = {}
        testobj.gui.newquietoptions = {'single_file': True, 'fname': 'xxx', 'pattern': 'yyy'}
        testobj.configure_quiet()
        assert testobj.quiet_options == {'dest': testee.Mode.single.name, 'fname': 'xxx',
                                         'pattern': 'yyy'}
        assert capsys.readouterr().out == (
            f"called QuietOptions.__init__ with args ({testobj},)\n"
            "called gui.show_dialog with args ('QuietOptionsGui',)\n")

    def test_configure_filter(self, monkeypatch, capsys):
        """unittest for LinterApp.configure_filter
        """
        def mock_show(*args):
            print('called gui.show_dialog with args', args)
            return False
        def mock_show_2(*args):
            print('called gui.show_dialog with args', args)
            return True
        def mock_init(self, *args):
            print('called FilterOptions.__init__ with args', args)
            self.gui = 'FilterOptionsGui'
        def mock_update():
            print('called LinterApp.update_blacklistfile')
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
        monkeypatch.setattr(testee.FilterOptions, '__init__', mock_init)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.update_blacklistfile = mock_update
        testobj.configure_filter()
        assert capsys.readouterr().out == (
            f"called FilterOptions.__init__ with args ({testobj},)\n"
            "called gui.show_dialog with args ('FilterOptionsGui',)\n")
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_2)
        testobj.configure_filter()
        assert capsys.readouterr().out == (
            f"called FilterOptions.__init__ with args ({testobj},)\n"
            "called gui.show_dialog with args ('FilterOptionsGui',)\n"
            "called LinterApp.update_blacklistfile\n")

    def test_get_output_filename(self, monkeypatch, capsys):
        """unittest for LinterApp.get_output_filename
        """
        fixdate = testee.datetime.datetime(2000, 1, 1)
        class mock_datetime:
            "stub for datetime.datetime"
            def today():
                return fixdate
        monkeypatch.setattr(testee.datetime, 'datetime', mock_datetime)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.quiet_options = {'ignore': 'xxx'}
        testobj.p = {'linter': 'yyy'}
        name = 'test/<filename>x<ignore><linter>-<date>'
        assert testobj.get_output_filename(name) == 'test/xyyy-20000101000000'
        name = 'test//<filename>-ignore<linter>-<date>'
        assert testobj.get_output_filename(name, 'zzzxxx') == "test/zzzxxx-ignoreyyy-20000101000000"
        name = 'test//<filename>-<ignore><linter>-<date>'
        assert testobj.get_output_filename(name, 'zzzxxx') == "test/zzz-yyy-20000101000000"

    def test_configure_linter(self, monkeypatch, capsys):
        """unittest for LinterApp.configure_linter
        """
        def mock_check(*args):
            nonlocal counter
            print('called LinterGui.get_radiogroup_checked with args', args)
            return ''
        counter = 0
        def mock_check_2(*args):
            nonlocal counter
            print('called LinterGui.get_radiogroup_checked with args', args)
            counter += 1
            if counter == 1:
                return 'xxx'
            return ''
        def mock_check_3(*args):
            nonlocal counter
            print('called LinterGui.get_radiogroup_checked with args', args)
            counter += 1
            if counter == 1:
                return 'xxx'
            return 'default'
        def mock_check_4(*args):
            nonlocal counter
            print('called LinterGui.get_radiogroup_checked with args', args)
            counter += 1
            if counter == 1:
                return 'xxx'
            return 'yyy'
        def mock_run(*args):
            print('called subprocess.run with args', args)
        monkeypatch.setattr(testee, 'checktypes', {'yyy': {'xxx': ['qq', 'rr=ss']}})
        monkeypatch.setattr(testee.subprocess, 'run', mock_run)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.linters = 'qqq'
        testobj.gui.check_options = 'check'
        testobj.editor_option = (['aa'], '{} bb', 'cc')
        testobj.gui.get_radiogroup_checked = mock_check
        testobj.configure_linter()
        assert capsys.readouterr().out == "called LinterGui.get_radiogroup_checked with args ('qqq',)\n"
        testobj.gui.get_radiogroup_checked = mock_check_2
        testobj.configure_linter()
        assert capsys.readouterr().out == (
            "called LinterGui.get_radiogroup_checked with args ('qqq',)\n"
            "called LinterGui.get_radiogroup_checked with args ('check',)\n")
        counter = 0
        testobj.gui.get_radiogroup_checked = mock_check_3
        testobj.configure_linter()
        assert capsys.readouterr().out == (
            "called LinterGui.get_radiogroup_checked with args ('qqq',)\n"
            "called LinterGui.get_radiogroup_checked with args ('check',)\n")
        counter = 0
        testobj.gui.get_radiogroup_checked = mock_check_4
        # breakpoint()
        testobj.configure_linter()
        assert capsys.readouterr().out == (
            "called LinterGui.get_radiogroup_checked with args ('qqq',)\n"
            "called LinterGui.get_radiogroup_checked with args ('check',)\n"
            "called subprocess.run with args (['aa', 'ss bb'],)\n")

    def test_determine_items_to_skip(self, monkeypatch, capsys):
        """unittest for LinterApp.determine_items_to_skip
        """
        class MockCheckBox:
            """stub
            """
            def __init__(self, value):
                self._value = value
            def __str__(self):
                return self._value
        def mock_remove():
            print('called LinterApp.remove_files_in_selected_dirs')
        counter = 0
        def mock_get_value(arg):
            print(f"called Gui.get_checkbox_value with arg '{arg}'")
            return False
        def mock_get_value_2(arg):
            nonlocal counter
            print(f"called Gui.get_checkbox_value with arg '{arg}'")
            counter += 1
            return counter == 1
        def mock_get_value_3(arg):
            nonlocal counter
            print(f"called Gui.get_checkbox_value with arg '{arg}'")
            counter += 1
            return counter > 1
        def mock_get_value_4(arg):
            print(f"called Gui.get_checkbox_value with arg '{arg}'")
            return True
        def mock_show(*args):
            print('called gui.show_dialog with args', args)
            return True  # niet gecanceld
        def mock_show_2(*args, **kwargs):
            print('called gui.show_dialog with args', args)
            return False  # wel gecanceld)
        def mock_show_3(*args):
            nonlocal counter
            print('called gui.show_dialog with args', args)
            counter += 1
            if counter == 1:
                return True  # niet gecanceld
            return False  # wel gecanceld)
        def mock_init(self, *args, **kwargs):
            print('called SelectNames.__init__ with args', args, kwargs)
            self.gui = 'SelectNamesGui'
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
        monkeypatch.setattr(testee.SelectNames, '__init__', mock_init)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.remove_files_in_selected_dirs = mock_remove
        testobj.ask_skipdirs = MockCheckBox('ask_skipdirs')
        testobj.ask_skipfiles = MockCheckBox('ask_skipfiles')
        testobj.gui.get_checkbox_value = mock_get_value
        testobj.do_checks = types.SimpleNamespace(dirnames=['xxx', 'yyy'],
                                                  filenames=['aaa', 'bbb', 'ccc', 'ddd'])
        # dirnames en/of filenames leeg
        testobj.do_checks.dirnames = []
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
        assert not testobj.determine_items_to_skip()
        assert not capsys.readouterr().out
        testobj.do_checks.filenames = []
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
        assert not testobj.determine_items_to_skip()
        assert not capsys.readouterr().out
        testobj.do_checks.dirnames = ['xxx', 'yyy']
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
        assert not testobj.determine_items_to_skip()
        assert not capsys.readouterr().out
        # skip_dirs en skip_files False
        testobj.do_checks.dirnames = ['xxx', 'yyy']
        testobj.do_checks.filenames = ['aaa', 'bbb', 'ccc', 'ddd']
        assert not testobj.determine_items_to_skip()
        assert capsys.readouterr().out == (
            "called Gui.get_checkbox_value with arg 'ask_skipdirs'\n"
            "called Gui.get_checkbox_value with arg 'ask_skipfiles'\n")
        # skip_dirs True, skip_files False; show_dialog niet gecanceld
        counter = 0
        testobj.gui.get_checkbox_value = mock_get_value_2
        assert not testobj.determine_items_to_skip()
        assert capsys.readouterr().out == (
            "called Gui.get_checkbox_value with arg 'ask_skipdirs'\n"
            "called Gui.get_checkbox_value with arg 'ask_skipfiles'\n"
            f"called SelectNames.__init__ with args ({testobj},) {{'files': False}}\n"
            "called gui.show_dialog with args ('SelectNamesGui',)\n"
            # f"called gui.show_dialog with args ({testobj.gui},)\n"
            "called LinterApp.remove_files_in_selected_dirs\n")
        # idem; show_dialog gecanceld
        counter = 0
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_2)
        assert testobj.determine_items_to_skip()
        assert capsys.readouterr().out == (
            "called Gui.get_checkbox_value with arg 'ask_skipdirs'\n"
            "called Gui.get_checkbox_value with arg 'ask_skipfiles'\n"
            f"called SelectNames.__init__ with args ({testobj},) {{'files': False}}\n"
            "called gui.show_dialog with args ('SelectNamesGui',)\n")
            # f"called gui.show_dialog with args ({testobj.gui},)\n")
        # skip_dirs False, skip_files True; show_dialog niet gecanceld
        counter = 0
        testobj.gui.get_checkbox_value = mock_get_value_3
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
        assert not testobj.determine_items_to_skip()
        assert capsys.readouterr().out == (
            "called Gui.get_checkbox_value with arg 'ask_skipdirs'\n"
            "called Gui.get_checkbox_value with arg 'ask_skipfiles'\n"
            f"called SelectNames.__init__ with args ({testobj},) {{}}\n"
            "called gui.show_dialog with args ('SelectNamesGui',)\n")
            # f"called gui.show_dialog with args ({testobj.gui},)\n")
        # idem; show_dialog gecanceld
        counter = 0
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_2)
        assert testobj.determine_items_to_skip()
        assert capsys.readouterr().out == (
            "called Gui.get_checkbox_value with arg 'ask_skipdirs'\n"
            "called Gui.get_checkbox_value with arg 'ask_skipfiles'\n"
            f"called SelectNames.__init__ with args ({testobj},) {{}}\n"
            "called gui.show_dialog with args ('SelectNamesGui',)\n")
            # f"called gui.show_dialog with args ({testobj.gui},) {{}}\n")
        # skip_dirs True, skip_files True; show_dialog 2e keer gecanceld
        counter = 0
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_3)
        testobj.gui.get_checkbox_value = mock_get_value_4
        assert testobj.determine_items_to_skip()
        assert capsys.readouterr().out == (
            "called Gui.get_checkbox_value with arg 'ask_skipdirs'\n"
            "called Gui.get_checkbox_value with arg 'ask_skipfiles'\n"
            f"called SelectNames.__init__ with args ({testobj},) {{'files': False}}\n"
            "called gui.show_dialog with args ('SelectNamesGui',)\n"
            # f"called gui.show_dialog with args ({testobj.gui},)\n"
            "called LinterApp.remove_files_in_selected_dirs\n"
            f"called SelectNames.__init__ with args ({testobj},) {{}}\n"
            "called gui.show_dialog with args ('SelectNamesGui',)\n"
            # f"called gui.show_dialog with args ({testobj.gui},)\n"
            f"called SelectNames.__init__ with args ({testobj},) {{'files': False}}\n"
            "called gui.show_dialog with args ('SelectNamesGui',)\n")
            # f"called gui.show_dialog with args ({testobj.gui},)\n")

    def test_remove_files_in_selected_dirs(self, monkeypatch, capsys):
        """unittest for LinterApp.determine_items_to_skip
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.do_checks = types.SimpleNamespace(filenames=['aaa/xxx',
                                                             'aaa/yyy',
                                                             'bbb/xxx',
                                                             'bbb/yyy',
                                                             'ccc/xxx',
                                                             'ccc/yyy'])
        testobj.names = ['aaa', 'ccc']
        testobj.remove_files_in_selected_dirs()
        assert testobj.do_checks.filenames == ['bbb/xxx',
                                               'bbb/yyy']


def test_get_iniloc():
    """unittest for main.get_iniloc
    """
    basepath = testee.pathlib.Path('~/.mylinter').expanduser()
    mrufile = 'mru_items.json'
    optfile = 'options.json'
    path = basepath / '~projects_lintergui'
    assert testee.get_iniloc() == (path, path / mrufile, path / optfile)

    path = basepath / '~projects_lintergui_test'
    assert testee.get_iniloc('test') == (path, path / mrufile, path / optfile)
    assert testee.get_iniloc(testee.pathlib.Path('test')) == (path, path / mrufile, path / optfile)

    pathstr = str(testee.pathlib.Path.home())
    path = basepath / '~'
    assert testee.get_iniloc(pathstr) == (path, path / mrufile, path / optfile)
    assert testee.get_iniloc(testee.pathlib.Path(pathstr)) == (path, path / mrufile, path / optfile)

    pathstr = str(testee.pathlib.Path.home() / 'test')
    path = basepath / '~test'
    assert testee.get_iniloc(pathstr) == (path, path / mrufile, path / optfile)
    assert testee.get_iniloc(testee.pathlib.Path(pathstr)) == (path, path / mrufile, path / optfile)

    path = basepath / '~projects_lintergui'
    assert testee.get_iniloc(str(testee.pathlib.Path(''))) == (path, path / mrufile,
                                                               path / optfile)
    path = basepath / '~projects_lintergui_test'
    assert testee.get_iniloc(str(testee.pathlib.Path('test'))) == (path, path / mrufile,
                                                                   path / optfile)
    path = basepath / 'test'
    assert testee.get_iniloc(str(testee.pathlib.Path('/test'))) == (path, path / mrufile,
                                                                    path / optfile)


def test_get_paths_from_file(tmp_path):
    """unittest for main.get_paths_from_file
    """
    (tmp_path / 'test').touch()
    (tmp_path / 'test3').touch()
    fname = tmp_path / 'pathnames'
    fname.write_text('test\n'
                     'test2\\\n'
                     'test3/\n')
    origdir = testee.os.getcwd()
    testee.os.chdir(tmp_path)
    assert testee.get_paths_from_file(fname) == []
    (tmp_path / 'test2').touch()
    assert testee.get_paths_from_file(fname) == ['test', 'test2', 'test3']
    fname.write_text(f'{tmp_path}/test\n'
                     f'{tmp_path}/test2\\\n'
                     f'{tmp_path}/test3/\n')
    testee.os.chdir(tmp_path)
    assert testee.get_paths_from_file(fname) == [f'{tmp_path}/test',
                                                 f'{tmp_path}/test2',
                                                 f'{tmp_path}/test3']
    testee.os.chdir(origdir)


def test_is_lintable(monkeypatch, capsys, tmp_path):
    """unittest for main.is_lintable
    """
    def mock_is_not_link(*args):
        print('called path.is_symlink with args', args)
        return False
    def mock_islink(*args):
        print('called path.is_symlink with args', args)
        return True
    def mock_read_text(*args):
        print('called path.read_text with args', args)
        return '#!\nxxxxx'
    def mock_read_text_2(*args):
        print('called path.read_text with args', args)
        return '#! /bin/sh'
    def mock_read_text_3(*args):
        print('called path.read_text with args', args)
        return '#! /usr/bin/py'
    def mock_read_text_4(*args):
        print('called path.read_text with args', args)
        return '#! usr/bin/python\nyyyy'
    def mock_read_text_5(*args):
        print('called path.read_text with args', args)
        return '#! usr/bin/env  python3'
    def mock_read_text_6(*args):
        print('called path.read_text with args', args)
        return 'and now\nfor something completely different'
    monkeypatch.setattr(testee.pathlib.Path, 'is_symlink', mock_islink)
    monkeypatch.setattr(testee.pathlib.Path, 'read_text', mock_read_text)
    mypath = tmp_path / 'test'
    assert not testee.is_lintable(mypath)
    assert capsys.readouterr().out == f"called path.is_symlink with args ({mypath!r},)\n"
    monkeypatch.setattr(testee.pathlib.Path, 'is_symlink', mock_is_not_link)
    assert capsys.readouterr().out == ""
    mypath = tmp_path / 'test.sh'
    assert not testee.is_lintable(mypath)
    assert capsys.readouterr().out == f"called path.is_symlink with args ({mypath!r},)\n"
    mypath = tmp_path / 'test.py'
    assert testee.is_lintable(mypath)
    assert capsys.readouterr().out == f"called path.is_symlink with args ({mypath!r},)\n"
    mypath = tmp_path / 'test.pyw'
    assert testee.is_lintable(mypath)
    assert capsys.readouterr().out == f"called path.is_symlink with args ({mypath!r},)\n"
    monkeypatch.setattr(testee.pathlib.Path, 'read_text', mock_read_text_2)
    mypath = tmp_path / 'test'
    assert not testee.is_lintable(mypath)
    assert capsys.readouterr().out == (f"called path.is_symlink with args ({mypath!r},)\n"
                                       f"called path.read_text with args ({mypath!r},)\n")
    monkeypatch.setattr(testee.pathlib.Path, 'read_text', mock_read_text_3)
    assert not testee.is_lintable(mypath)
    assert capsys.readouterr().out == (f"called path.is_symlink with args ({mypath!r},)\n"
                                       f"called path.read_text with args ({mypath!r},)\n")
    monkeypatch.setattr(testee.pathlib.Path, 'read_text', mock_read_text_4)
    assert testee.is_lintable(mypath)
    assert capsys.readouterr().out == (f"called path.is_symlink with args ({mypath!r},)\n"
                                       f"called path.read_text with args ({mypath!r},)\n")
    monkeypatch.setattr(testee.pathlib.Path, 'read_text', mock_read_text_5)
    assert testee.is_lintable(mypath)
    assert capsys.readouterr().out == (f"called path.is_symlink with args ({mypath!r},)\n"
                                       f"called path.read_text with args ({mypath!r},)\n")
    monkeypatch.setattr(testee.pathlib.Path, 'read_text', mock_read_text_6)
    assert not testee.is_lintable(mypath)
    assert capsys.readouterr().out == (f"called path.is_symlink with args ({mypath!r},)\n"
                                       f"called path.read_text with args ({mypath!r},)\n")


class TestFilterOptions:
    """unittests for main.FilterOptions
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.FilterOptions object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called FilterOptions.__init__ with args', args)
        monkeypatch.setattr(testee.FilterOptions, '__init__', mock_init)
        testobj = testee.FilterOptions()
        assert capsys.readouterr().out == 'called FilterOptions.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for FilterOptions.__init__
        """
        class MockGui:
            def __init__(self, *args):
                print('called FilterOptionsGuiFilterOptionsGui.__init__ with args', args)
            def add_title_line(self, *args):
                print('called FilterOptionsGuiFilterOptionsGui.add_title_line with args', args)
            def add_textentry_line(self, *args, **kwargs):
                print('called FilterOptionsGuiFilterOptionsGui.add_textentry_line with args',
                      args, kwargs)
                return 'textentry'
            def add_buttons(self, *args):
                print('called FilterOptionsGuiFilterOptionsGui.add_buttons with args', args)
            def accept(self):
                "stub"
            def reject(self):
                "stub"
        monkeypatch.setattr(testee.gui, 'FilterOptionsGui', MockGui)
        parent = types.SimpleNamespace(gui='LinterGui', title='title',
                                       blacklist={'exclude_dirs': ['exclude'],
                                                  'exclude_exts': ['x', 'y'],
                                                  'exclude_files': ['qqq'],
                                                  'include_exts': ['a', 'b'],
                                                  'include_shebang': ['#!']})
        testobj = testee.FilterOptions(parent)
        assert isinstance(testobj.gui, testee.gui.FilterOptionsGui)
        assert testobj.parent == parent
        assert testobj.skipdirs == 'textentry'
        assert testobj.skipexts == 'textentry'
        assert testobj.skipfiles == 'textentry'
        assert testobj.do_exts == 'textentry'
        assert testobj.do_bangs == 'textentry'
        assert capsys.readouterr().out == (
                "called FilterOptionsGuiFilterOptionsGui.__init__ with args"
                f" ({testobj}, 'LinterGui', 'title')\n"
                "called FilterOptionsGuiFilterOptionsGui.add_title_line with args"
                " ('Blacklist (do no lint):',)\n"
                "called FilterOptionsGuiFilterOptionsGui.add_textentry_line with args"
                " ('Directory names:', 'exclude') {'width': 200}\n"
                "called FilterOptionsGuiFilterOptionsGui.add_textentry_line with args"
                " ('File extensions:', 'x, y') {}\n"
                "called FilterOptionsGuiFilterOptionsGui.add_textentry_line with args"
                " ('File names:', 'qqq') {}\n"
                "called FilterOptionsGuiFilterOptionsGui.add_title_line with args ('',)\n"
                "called FilterOptionsGuiFilterOptionsGui.add_title_line with args"
                " ('Whitelist (only lint):',)\n"
                "called FilterOptionsGuiFilterOptionsGui.add_textentry_line with args"
                " ('File extensions:', 'a, b') {}\n"
                "called FilterOptionsGuiFilterOptionsGui.add_textentry_line with args"
                " ('Shebang lines:', '#!') {}\n"
                "called FilterOptionsGuiFilterOptionsGui.add_title_line with args ('',)\n"
                "called FilterOptionsGuiFilterOptionsGui.add_buttons with args"
                f" ([('&Terug', {testobj.gui.reject}), ('&Klaar', {testobj.gui.accept})],)\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for FilterOptions.confirm
        """
        def mock_get(arg):
            print(f'called FilterOptions.get_text_from_gui with arg {arg}')
            return arg
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace()
        testobj.get_text_from_gui = mock_get
        testobj.skipdirs = 'skipdirs'
        testobj.skipexts = 'skipexts'
        testobj.skipfiles = 'skipfiles'
        testobj.do_exts = 'do_exts'
        testobj.do_bangs = 'do_bangs'
        testobj.confirm()
        assert testobj.parent.blacklist == {'exclude_dirs': 'skipdirs',
                                            'exclude_exts': 'skipexts',
                                            'exclude_files': 'skipfiles',
                                            'include_exts': 'do_exts',
                                            'include_shebang' :'do_bangs'}
        assert capsys.readouterr().out == (
                "called FilterOptions.get_text_from_gui with arg skipdirs\n"
                "called FilterOptions.get_text_from_gui with arg skipexts\n"
                "called FilterOptions.get_text_from_gui with arg skipfiles\n"
                "called FilterOptions.get_text_from_gui with arg do_exts\n"
                "called FilterOptions.get_text_from_gui with arg do_bangs\n")

    def test_get_text_from_gui(self, monkeypatch, capsys):
        """unittest for FilterOptions.get_text_from_gui
        """
        def mock_get(arg):
            print(f'called FilterOptionsGui.get_textentry_value with arg {arg}')
            return f'xxx{testee.SEP}yyy'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = types.SimpleNamespace(get_textentry_value=mock_get)
        assert testobj.get_text_from_gui('textfield') == ['xxx', 'yyy']
        assert capsys.readouterr().out == (
                "called FilterOptionsGui.get_textentry_value with arg textfield\n")


class TestQuietOptions:
    """unittests for main.QuietOptions
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.QuietOptions object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called QuietOptions.__init__ with args', args)
        monkeypatch.setattr(testee.QuietOptions, '__init__', mock_init)
        testobj = testee.QuietOptions()
        assert capsys.readouterr().out == 'called QuietOptions.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for QuietOptions.__init__
        """
        class MockGui:
            def __init__(self, *args):
                print('called QuietOptionsGui.__init__ with args', args)
            def start_line(self, *args):
                print('called QuietOptionsGui.start_line with args', args)
                return 'line'
            def add_text_to_line(self, *args, **kwargs):
                print('called QuietOptionsGui.add_text_to_line with args', args, kwargs)
            def add_radiobutton_to_line(self, *args):
                print('called QuietOptionsGui.add_radiobutton_to_line with args', args)
                return 'radiobutton'
            def add_textentry_to_line(self, *args, **kwargs):
                print('called QuietOptionsGui.add_textentry_to_line with args', args, kwargs)
                return 'textentry'
            def add_button_to_line(self, *args):
                print('called QuietOptionsGui.add_button_to_line with args', args)
            def end_line(self, *args):
                print('called QuietOptionsGui.end_line with args', args)
            def add_buttons(self, *args):
                print('called QuietOptionsGui.add_buttons with args', args)
            def set_radiobutton_value(self, *args):
                print('called QuietOptionsGui.set_radiobutton_value with args', args)
            def set_textentry_value(self, *args):
                print('called QuietOptionsGui.set_textentry_value with args', args)
            def browse(self):
                "stub"
            def accept(self):
                "stub"
            def reject(self):
                "stub"
        monkeypatch.setattr(testee.gui, 'QuietOptionsGui', MockGui)
        parent = types.SimpleNamespace(gui='QuietOptionsGui', title='title', dest_from_input='qqq',
                                       quiet_options={'dest': testee.Mode.standard.name,
                                                      'fname': 'xxx', 'pattern': 'yyy',
                                                      'ignore': 'zzz'}, )
        testobj = testee.QuietOptions(parent)
        assert isinstance(testobj.gui, testee.gui.QuietOptionsGui)
        assert testobj.single == 'radiobutton'
        assert testobj.fname == 'textentry'
        assert testobj.multi == 'radiobutton'
        assert testobj.pattern == 'textentry'
        assert testobj.ignore == 'textentry'
        assert capsys.readouterr().out == (
            f"called QuietOptionsGui.__init__ with args ({testobj}, 'QuietOptionsGui', 'title')\n"
            "called QuietOptionsGui.start_line with args ()\n"
            "called QuietOptionsGui.add_text_to_line with args ('line', 'Send output to:') {}\n"
            "called QuietOptionsGui.end_line with args ('line',)\n"
            "called QuietOptionsGui.start_line with args ()\n"
            "called QuietOptionsGui.add_radiobutton_to_line with args"
            " ('line', 'Single file:', False)\n"
            "called QuietOptionsGui.add_textentry_to_line with args"
            " ('line', 'xxx') {'width': 200}\n"
            "called QuietOptionsGui.add_button_to_line with args"
            f" ('line', 'Select', {testobj.gui.browse})\n"
            "called QuietOptionsGui.end_line with args ('line',)\n"
            "called QuietOptionsGui.start_line with args ()\n"
            "called QuietOptionsGui.add_radiobutton_to_line with args"
            " ('line', 'Multiple files like:', False)\n"
            "called QuietOptionsGui.add_textentry_to_line with args"
            " ('line', 'yyy') {'width': 300}\n"
            "called QuietOptionsGui.end_line with args ('line',)\n"
            "called QuietOptionsGui.start_line with args ()\n"
            "called QuietOptionsGui.add_text_to_line with args"
            " ('line', '<ignore> part of filename:') {'before': 26}\n"
            "called QuietOptionsGui.add_textentry_to_line with args"
            " ('line', 'zzz') {'width': 200}\n"
            "called QuietOptionsGui.end_line with args ('line',)\n"
            "called QuietOptionsGui.start_line with args ()\n"
            f"called QuietOptionsGui.add_text_to_line with args ('line', {testobj.text!r}) {{}}\n"
            "called QuietOptionsGui.end_line with args ('line',)\n"
            "called QuietOptionsGui.add_buttons with args"
            f" ([('&Terug', {testobj.gui.reject}), ('&Klaar', {testobj.gui.accept})],)\n"
            "called QuietOptionsGui.set_radiobutton_value with args ('radiobutton', True)\n"
            "called QuietOptionsGui.set_textentry_value with args ('textentry', 'qqq')\n")
        testobj.parent.dest_from_input = ''
        testobj = testee.QuietOptions(parent)
        assert isinstance(testobj.gui, testee.gui.QuietOptionsGui)
        assert testobj.single == 'radiobutton'
        assert testobj.fname == 'textentry'
        assert testobj.multi == 'radiobutton'
        assert testobj.pattern == 'textentry'
        assert testobj.ignore == 'textentry'
        assert capsys.readouterr().out == (
            f"called QuietOptionsGui.__init__ with args ({testobj}, 'QuietOptionsGui', 'title')\n"
            "called QuietOptionsGui.start_line with args ()\n"
            "called QuietOptionsGui.add_text_to_line with args ('line', 'Send output to:') {}\n"
            "called QuietOptionsGui.end_line with args ('line',)\n"
            "called QuietOptionsGui.start_line with args ()\n"
            "called QuietOptionsGui.add_radiobutton_to_line with args"
            " ('line', 'Single file:', False)\n"
            "called QuietOptionsGui.add_textentry_to_line with args"
            " ('line', 'xxx') {'width': 200}\n"
            "called QuietOptionsGui.add_button_to_line with args"
            f" ('line', 'Select', {testobj.gui.browse})\n"
            "called QuietOptionsGui.end_line with args ('line',)\n"
            "called QuietOptionsGui.start_line with args ()\n"
            "called QuietOptionsGui.add_radiobutton_to_line with args"
            " ('line', 'Multiple files like:', False)\n"
            "called QuietOptionsGui.add_textentry_to_line with args"
            " ('line', 'yyy') {'width': 300}\n"
            "called QuietOptionsGui.end_line with args ('line',)\n"
            "called QuietOptionsGui.start_line with args ()\n"
            "called QuietOptionsGui.add_text_to_line with args"
            " ('line', '<ignore> part of filename:') {'before': 26}\n"
            "called QuietOptionsGui.add_textentry_to_line with args"
            " ('line', 'zzz') {'width': 200}\n"
            "called QuietOptionsGui.end_line with args ('line',)\n"
            "called QuietOptionsGui.start_line with args ()\n"
            f"called QuietOptionsGui.add_text_to_line with args ('line', {testobj.text!r}) {{}}\n"
            "called QuietOptionsGui.end_line with args ('line',)\n"
            "called QuietOptionsGui.add_buttons with args"
            f" ([('&Terug', {testobj.gui.reject}), ('&Klaar', {testobj.gui.accept})],)\n")

    def _test_browse(self, monkeypatch, capsys):
        """unittest for QuietOptions.browse
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.browse() == "expected_result"
        assert capsys.readouterr().out == ("")
        # nog een TODO, dus ook nog geen testmethode

    def test_confirm(self, monkeypatch, capsys):
        """unittest for QuietOptions.confirm
        """
        def mock_get_radio(arg):
            print(f'called QuietOptionsGui.get_radiobutton_value with arg {arg}')
            return arg
        def mock_get_text(arg):
            print(f'called QuietOptionsGui.get_textentry_value with arg {arg}')
            return arg
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = types.SimpleNamespace(get_radiobutton_value=mock_get_radio,
                                            get_textentry_value=mock_get_text)
        testobj.parent = types.SimpleNamespace()
        testobj.single = "single"
        testobj.fname = "fname"
        testobj.pattern = "pattern"
        testobj.ignore = "ignore"
        testobj.confirm()
        assert testobj.parent.newquietoptions == {'single_file': 'single', 'fname': 'fname',
                                                  'pattern': 'pattern', 'ignore': 'ignore'}
        assert capsys.readouterr().out == (
                "called QuietOptionsGui.get_radiobutton_value with arg single\n"
                "called QuietOptionsGui.get_textentry_value with arg fname\n"
                "called QuietOptionsGui.get_textentry_value with arg pattern\n"
                "called QuietOptionsGui.get_textentry_value with arg ignore\n")


class TestSelectNames:
    """unittests for main.SelectNames
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.SelectNames object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SelectNames.__init__ with args', args)
        monkeypatch.setattr(testee.SelectNames, '__init__', mock_init)
        testobj = testee.SelectNames()
        assert capsys.readouterr().out == 'called SelectNames.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for SelectNames.__init__
        """
        class MockGui:
            def __init__(self, *args):
                print('called SelectNamesGui.__init__ with args', args)
            def start_line(self):
                print('called SelectNamesGui.start_line')
                return 'line'
            def add_text_to_line(self, *args):
                print('called SelectNamesGui.add_text_to_line with args', args)
            def add_checkbox_to_line(self, *args, **kwargs):
                print('called SelectNamesGui.add_checkbox_to_line with args', args, kwargs)
                return 'checkbox'
            def add_button_to_line(self, *args, **kwargs):
                print('called SelectNamesGui.add_button_to_line with args', args, kwargs)
                return 'button'
            def create_checkbox_list(self, *args):
                print('called SelectNamesGui.create_checkbox_list with args', args)
                return ['check', 'box']
            def create_button_bar(self, *args):
                print('called SelectNamesGui.create_button_bar with args', args)
            def accept(self):
                "stub"
            def reject(self):
                "stub"
        parent = types.SimpleNamespace(title='title', names=['x', 'y'])
        monkeypatch.setattr(testee.gui, 'SelectNamesGui', MockGui)
        testobj = testee.SelectNames(parent)
        assert testobj.parent == parent
        assert testobj.dofiles
        assert isinstance(testobj.gui, testee.gui.SelectNamesGui)
        assert capsys.readouterr().out == (
                "called SelectNamesGui.__init__ with args"
                f" ({testobj}, {parent}, 'title - file list')\n"
                "called SelectNamesGui.start_line\n"
                "called SelectNamesGui.add_text_to_line with args"
                " ('line', 'Selecteer de bestanden die je *niet* wilt verwerken')\n"
                "called SelectNamesGui.start_line\n"
                "called SelectNamesGui.add_checkbox_to_line with args"
                f" ('line', 'Select/Unselect All', {testobj.select_all}) {{'before': 10}}\n"
                "called SelectNamesGui.add_button_to_line with args"
                f" ('line', 'Invert selection', {testobj.invert_selection}) {{'before': 20}}\n"
                "called SelectNamesGui.create_checkbox_list with args (['x', 'y'],)\n"
                "called SelectNamesGui.create_button_bar with args"
                f" ([('&Terug', {testobj.gui.reject}), ('&Klaar', {testobj.gui.accept})],)\n")
        testobj = testee.SelectNames(parent, files=False)
        assert testobj.parent == parent
        assert not testobj.dofiles
        assert capsys.readouterr().out == (
                "called SelectNamesGui.__init__ with args"
                f" ({testobj}, {parent}, 'title - file list')\n"
                "called SelectNamesGui.start_line\n"
                "called SelectNamesGui.add_text_to_line with args"
                " ('line', 'Selecteer de directories die je *niet* wilt verwerken')\n"
                "called SelectNamesGui.start_line\n"
                "called SelectNamesGui.add_checkbox_to_line with args"
                f" ('line', 'Select/Unselect All', {testobj.select_all}) {{'before': 10}}\n"
                "called SelectNamesGui.add_button_to_line with args"
                f" ('line', 'Invert selection', {testobj.invert_selection}) {{'before': 20}}\n"
                "called SelectNamesGui.create_checkbox_list with args (['x', 'y'],)\n"
                "called SelectNamesGui.create_button_bar with args"
                f" ([('&Terug', {testobj.gui.reject}), ('&Klaar', {testobj.gui.accept})],)\n")

    def test_select_all(self, monkeypatch, capsys):
        """unittest for SelectNames.select_all
        """
        def mock_get(*args):
            print('called SelectNamesGui.get_checkbox_value with args', args)
            return 'value'
        def mock_set(*args):
            print('called SelectNamesGui.set_checkbox_value with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sel_all = 'sel_all'
        testobj.checklist = ['sel1', 'sel2']
        testobj.gui = types.SimpleNamespace(get_checkbox_value=mock_get,
                                            set_checkbox_value=mock_set)
        testobj.select_all()
        assert capsys.readouterr().out == (
                "called SelectNamesGui.get_checkbox_value with args ('sel_all',)\n"
                "called SelectNamesGui.set_checkbox_value with args ('sel1', 'value')\n"
                "called SelectNamesGui.set_checkbox_value with args ('sel2', 'value')\n")

    def test_invert_selection(self, monkeypatch, capsys):
        """unittest for SelectNames.invert_selection
        """
        def mock_get(*args):
            print('called SelectNamesGui.get_checkbox_value with args', args)
            if args[0] == 'sel1':
                return True
            return False
        def mock_set(*args):
            print('called SelectNamesGui.set_checkbox_value with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.checklist = ['sel1', 'sel2']
        testobj.gui = types.SimpleNamespace(get_checkbox_value=mock_get,
                                            set_checkbox_value=mock_set)
        testobj.invert_selection()
        assert capsys.readouterr().out == (
                "called SelectNamesGui.get_checkbox_value with args ('sel1',)\n"
                "called SelectNamesGui.set_checkbox_value with args ('sel1', False)\n"
                "called SelectNamesGui.get_checkbox_value with args ('sel2',)\n"
                "called SelectNamesGui.set_checkbox_value with args ('sel2', True)\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for SelectNames.confirm
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        def mock_get(*args):
            print('called SelectNamesGui.get_checkbox_value with args', args)
            if args[0] == 'sel1':
                return True
            return False
        def mock_get_text(*args):
            print('called SelectNamesGui.get_checkbox_text with args', args)
            return f'{args[0]}text'
        testobj.checklist = ['sel1', 'sel2']
        testobj.parent = types.SimpleNamespace(names=['sel1text', 'sel2text'])
        testobj.gui = types.SimpleNamespace(get_checkbox_value=mock_get,
                                            get_checkbox_text=mock_get_text)
        testobj.dofiles = False
        testobj.confirm()
        assert testobj.parent.names == ['sel1text']
        assert capsys.readouterr().out == (
                "called SelectNamesGui.get_checkbox_value with args ('sel1',)\n"
                "called SelectNamesGui.get_checkbox_text with args ('sel1',)\n"
                "called SelectNamesGui.get_checkbox_value with args ('sel2',)\n")
        testobj.parent.names = ['sel1text', 'sel2text']
        testobj.dofiles = True
        testobj.confirm()
        assert testobj.parent.names == ['sel2text']
        assert capsys.readouterr().out == (
                "called SelectNamesGui.get_checkbox_value with args ('sel1',)\n"
                "called SelectNamesGui.get_checkbox_text with args ('sel1',)\n"
                "called SelectNamesGui.get_checkbox_value with args ('sel2',)\n")


class TestResults:
    """unittests for main.Results
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.Results object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            print('called Results.__init__ with args', args)
        monkeypatch.setattr(testee.Results, '__init__', mock_init)
        testobj = testee.Results()
        assert capsys.readouterr().out == 'called Results.__init__ with args ()\n'
        return testobj


    def test_init(self, monkeypatch, capsys):
        """unittest for Results.__init__
        """
        class MockGui:
            def __init__(self, *args):
                print('called ResultsGui.__init__ with args', args)
            def add_top_text(self, *args):
                print('called ResultsGui.add_top_text with args', args)
                return args[0]
            def add_combobox_line(self, *args):
                print('called ResultsGui.add_combobox_line with args', args)
                return 'line', 'filelist'
            def add_button_to_line(self, *args):
                print('called ResultsGui.add_button_to_line with args', args)
            def add_buttons(self, *args):
                print('called ResultsGui.add_buttons with args', args)
            def add_results_list(self):
                print('called ResultsGui.add_results_list')
                return 'resultslist'
            def accept(self):
                "stub"
        def mock_populate_list(self):
            print('called Results.populate_list')
        parent = types.SimpleNamespace(resulttitel='title', gui='ResultsGui')
        parent.mode = testee.Mode.standard.value
        parent.do_checks = types.SimpleNamespace(filenames=['x', 'y'], rpt=['zz'],
                                                 results=['qq', 'rr'])
        monkeypatch.setattr(testee.gui, 'ResultsGui', MockGui)
        monkeypatch.setattr(testee.Results, 'populate_list', mock_populate_list)
        testobj = testee.Results(parent, common_path='')
        assert testobj.parent == parent
        assert testobj.common == ''
        assert isinstance(testobj.gui, testee.gui.ResultsGui)
        assert testobj.results == []
        assert testobj.filelist == 'filelist'
        assert testobj.lijst == 'resultslist'
        assert capsys.readouterr().out == (
                f"called ResultsGui.__init__ with args ({testobj}, 'ResultsGui', 'title', 150)\n"
                "called ResultsGui.add_top_text with args ('zz (2 items)',)\n"
                "called ResultsGui.add_combobox_line with args ('Files checked:', ['x', 'y'])\n"
                "called ResultsGui.add_button_to_line with args"
                f" ('line', '&Go To File', {testobj.goto_result})\n"
                "called ResultsGui.add_results_list\n"
                "called Results.populate_list\n"
                "called ResultsGui.add_buttons with args"
                f" ([('&Klaar', {testobj.gui.accept}), ('&Repeat Action', {testobj.refresh}),"
                f" ('Copy to &File(s)', {testobj.kopie}),"
                f" ('Copy to &Clipboard', {testobj.to_clipboard})],)\n")
        parent.mode = testee.Mode.single.value
        testobj = testee.Results(parent, common_path='')
        assert testobj.parent == parent
        assert testobj.common == ''
        assert isinstance(testobj.gui, testee.gui.ResultsGui)
        assert testobj.results == []
        assert testobj.filelist == 'filelist'
        assert testobj.lijst == 'resultslist'
        assert capsys.readouterr().out == (
                f"called ResultsGui.__init__ with args ({testobj}, 'ResultsGui', 'title', 50)\n"
                f"called ResultsGui.add_top_text with args ('zz (2 items)',)\n"
                "called ResultsGui.add_combobox_line with args ('Files checked:', ['x', 'y'])\n"
                "called ResultsGui.add_button_to_line with args"
                f" ('line', '&Go To File', {testobj.goto_result})\n"
                "called ResultsGui.add_results_list\n"
                "called Results.populate_list\n"
                "called ResultsGui.add_buttons with args"
                f" ([('&Klaar', {testobj.gui.accept}), ('&Repeat Action', {testobj.refresh}),"
                f" ('Copy to &File(s)', {testobj.kopie}),"
                f" ('Copy to &Clipboard', {testobj.to_clipboard})],)\n")
        parent.mode = testee.Mode.multi.value
        monkeypatch.setattr(testee.Results, 'common_path_txt', 'common={}')
        testobj = testee.Results(parent, common_path=f'xxx{testee.os.sep}')
        assert testobj.parent == parent
        assert testobj.common == 'xxx/'
        assert isinstance(testobj.gui, testee.gui.ResultsGui)
        assert testobj.results == []
        assert testobj.filelist == 'filelist'
        assert testobj.lijst == 'resultslist'
        assert capsys.readouterr().out == (
                f"called ResultsGui.__init__ with args ({testobj}, 'ResultsGui', 'title', 150)\n"
                f"called ResultsGui.add_top_text with args ('zz (2 items)\\ncommon=xxx',)\n"
                "called ResultsGui.add_combobox_line with args ('Files checked:', ['x', 'y'])\n"
                "called ResultsGui.add_button_to_line with args"
                f" ('line', '&Go To File', {testobj.goto_result})\n"
                "called ResultsGui.add_results_list\n"
                "called Results.populate_list\n"
                "called ResultsGui.add_buttons with args"
                f" ([('&Klaar', {testobj.gui.accept}), ('&Repeat Action', {testobj.refresh}),"
                f" ('Copy to &File(s)', {testobj.kopie}),"
                f" ('Copy to &Clipboard', {testobj.to_clipboard})],)\n")

    def test_populate_list(self, monkeypatch, capsys):
        """unittest for Results.populate_list
        """
        def mock_get(*args):
            print('called ResultsGui.get_combobox_value with args', args)
            return 'qqq'
        def mock_set(*args):
            print('called ResultsGui.set_textbox_value with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = types.SimpleNamespace(get_combobox_value=mock_get,
                                            set_textbox_value=mock_set)
        testobj.parent = types.SimpleNamespace(
                do_checks=types.SimpleNamespace(results={'qqq': 'xx'}))
        testobj.filelist = 'filelist'
        testobj.lijst = 'lijst'
        testobj.populate_list()
        assert capsys.readouterr().out == (
                "called ResultsGui.get_combobox_value with args ('filelist',)\n"
                "called ResultsGui.set_textbox_value with args ('lijst', 'xx')\n")

    # def _test_klaar(self, monkeypatch, capsys):
    #     """unittest for Results.klaar
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.klaar() == "expected_result"
    #     assert capsys.readouterr().out == ("")

    def test_refresh(self, monkeypatch, capsys):
        """unittest for Results.refresh
        """
        def mock_set(*args):
            print('called ResultsGui.set_combobox_value with args', args)
        def mock_set_text(*args):
            print('called ResultsGui.set_textbox_value with args', args)
        def mock_exec():
            print('called LinterGui.execute_action')
        def mock_populate():
            print('called Results.populate_list')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = types.SimpleNamespace(set_combobox_value=mock_set,
                                            set_textbox_value=mock_set_text)
        testobj.parent = types.SimpleNamespace(
                do_checks=types.SimpleNamespace(specs=['qqq', 'rrr']),
                gui=types.SimpleNamespace(execute_action=mock_exec))
        testobj.populate_list = mock_populate
        testobj.lijst = 'lijst'
        testobj.filelist = 'filelist'
        testobj.refresh()
        assert testobj.results == []
        assert testobj.parent.do_checks.rpt == ['qqqrrr']
        assert capsys.readouterr().out == (
                "called ResultsGui.set_textbox_value with args ('lijst', '')\n"
                "called LinterGui.execute_action\n"
                "called Results.populate_list\n"
                "called ResultsGui.set_combobox_value with args ('filelist', 0)\n")

    def test_kopie(self, monkeypatch, capsys, tmp_path):
        """unittest for Results.kopie
        """
        class MockQuiet:
            def __init__(self, *args):
                print('called QuietOptions.__init__ with args', args)
                self.gui = 'QuietOptionsGui'
        def mock_dialog(*args):
            print('called gui.dialog_message with args', args)
            return False
        def mock_dialog_2(*args):
            print('called gui.dialog_message with args', args)
            return True
        def mock_get(*args):
            print('called LinterApp.get_output_filename with args', args)
            return args[0]
        def mock_show(*args):
            print('called gui.show_message with args', args)
        monkeypatch.setattr(testee, 'QuietOptions', MockQuiet)
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = 'ResultsGui'
        testobj.parent = types.SimpleNamespace(
                title='title', gui='LinterGui', get_output_filename=mock_get,
                newquietoptions={'single_file': True, 'fname': tmp_path / 'outfile'},
                do_checks=types.SimpleNamespace(results={'x': 'xxxx', 'y': 'yyyy'}))
        testobj.kopie()
        assert capsys.readouterr().out == (
                f"called QuietOptions.__init__ with args ({testobj},)\n"
                "called gui.dialog_message with args ('QuietOptionsGui',)\n")
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_2)
        testobj.kopie()
        assert capsys.readouterr().out == (
                f"called QuietOptions.__init__ with args ({testobj},)\n"
                "called gui.dialog_message with args ('QuietOptionsGui',)\n"
                f"called LinterApp.get_output_filename with args ({tmp_path / 'outfile'!r},)\n"
                "called gui.show_message with args"
                f" ('ResultsGui', 'title', 'Output saved as {tmp_path}/outfile')\n")
        testobj.parent.newquietoptions = {'single_file': False, 'pattern': 'outfilepattern'}
        testobj.kopie()
        assert capsys.readouterr().out == (
                f"called QuietOptions.__init__ with args ({testobj},)\n"
                "called gui.dialog_message with args ('QuietOptionsGui',)\n"
                "called LinterApp.get_output_filename with args ('outfilepattern', 'x')\n"
                "called LinterApp.get_output_filename with args ('outfilepattern', 'y')\n"
                "called gui.show_message with args"
                " ('ResultsGui', 'title', 'Last output saved as outfilepattern')\n")

    def test_help(self, monkeypatch, capsys):
        """unittest for Results.help
        """
        def mock_show(*args):
            print('called gui.show_message with args', args)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(title='title')
        testobj.gui = 'ResultsGui'
        testobj.helpinfo = 'xxx'
        testobj.help()
        assert capsys.readouterr().out == (
                "called gui.show_message with args ('ResultsGui', 'title', 'xxx')\n")

    def test_to_clipboard(self, monkeypatch, capsys):
        """unittest for Results.to_clipboard
        """
        def mock_copy(*args):
            print('called ResultsGui.copy_to_clipboard')
        def mock_show(*args):
            print('called gui.show_message with args', args)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = types.SimpleNamespace(copy_to_clipboard=mock_copy)
        testobj.parent = types.SimpleNamespace(
                title='title',
                do_checks=types.SimpleNamespace(results={'x': 'xxxx', 'y': 'yyyy'}))
        testobj.to_clipboard()
        assert capsys.readouterr().out == (
                "called ResultsGui.copy_to_clipboard\n"
                "called gui.show_message with args"
                f" ({testobj.gui}, 'title', 'Output copied to clipboard')\n")

    def test_goto_result(self, monkeypatch, capsys):
        """unittest for Results.goto_result
        """
        def mock_get(*args):
            print('called ResultsGui.get_combobox_value with args', args)
            return 'qqq'
        def mock_run(*args, **kwargs):
            print('called subprocess.run with args', args, kwargs)
        monkeypatch.setattr(testee.subprocess, 'run', mock_run)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = types.SimpleNamespace(get_combobox_value=mock_get)
        testobj.parent = types.SimpleNamespace(editor_option=[['x'], 'y{}', 'z', 'q'])
        testobj.filelist = 'filelist'
        testobj.goto_result()
        assert capsys.readouterr().out == (
                "called ResultsGui.get_combobox_value with args ('filelist',)\n"
                "called subprocess.run with args (['x', 'yqqq'],) {'check': False}\n")
