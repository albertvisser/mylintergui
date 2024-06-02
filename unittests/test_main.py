"""unitt'ests for ./app/main.py
"""
from app import main as testee


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


class MockMainGui:
    "stub for gui.MainGui"
    def __init__(self, *args, **kwargs):
        print('called MainGui.__init__ with args', args, kwargs)
    def setup_screen(self):
        "stub"
        print('called MainGui.setup_screen')
    def set_checkbox_value(self, *args):
        "stub"
        print('called MainGui.set_checkbox_value with args', args)


class TestBase:
    """unittest for main.Base
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.Base object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Base.__init__ with args', args)
        monkeypatch.setattr(testee.Base, '__init__', mock_init)
        testobj = testee.Base()
        testobj.gui = MockMainGui()
        assert capsys.readouterr().out == ('called Base.__init__ with args ()\n'
                                           "called MainGui.__init__ with args () {}\n")
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for Base.__init__
        """
        def mock_get_option(self):
            print('called Base.get_editor_option')
        def mock_blacklist(self):
            print('called Base.build_blacklist')
        def mock_set_mode(self, *args):
            print('called Base.set_mode with args', args)
        monkeypatch.setattr(testee.Base, 'get_editor_option', mock_get_option)
        monkeypatch.setattr(testee.Base, 'build_blacklist', mock_blacklist)
        monkeypatch.setattr(testee.Base, 'set_mode', mock_set_mode)
        monkeypatch.setattr(testee.gui, 'MainGui', MockMainGui)
        testobj = testee.Base({'args': 'dict'})
        assert testobj.title == "Albert's linter GUI frontend"
        assert testobj.iconame == testee.iconame
        assert testobj.fouttitel == testobj.title + "- fout"
        assert testobj.resulttitel == testobj.title + " - Resultaten"
        assert testobj.hier == ""
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
        assert testobj.fnames == []
        assert capsys.readouterr().out == (
                "called Base.get_editor_option\n"
                "called Base.build_blacklist\n"
                "called Base.set_mode with args ({'args': 'dict'},)\n"
                f"called MainGui.__init__ with args () {{'master': {testobj}}}\n"
                "called MainGui.setup_screen\n")

    def _test_set_mode(self, monkeypatch, capsys):
        """unittest for Base.set_mode
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_mode('args') == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_readini(self, monkeypatch, capsys, tmp_path):
        """unittest for Base.readini
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
        """unittest for Base.schrijfini
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

    def test_get_editor_option(self, monkeypatch, capsys, tmp_path):
        """unittest for Base.get_editor_option
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

    def test_build_blacklist(self, monkeypatch, capsys, tmp_path):
        """unittest for Base.build_blacklist
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
            print('called Base.update_blacklistfile')
        blacklistfile = tmp_path / 'blacklistfile'
        blacklistfile.write_text('blacklisted items')
        monkeypatch.setattr(testee.pathlib.Path, 'open', mock_open)
        monkeypatch.setattr(testee, 'blacklist', blacklistfile)
        monkeypatch.setattr(testee, 'initial_blacklist', {'initial': 'blacklist'})
        monkeypatch.setattr(testee.json, 'load', mock_load)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.update_blacklistfile = mock_update
        testobj.build_blacklist()
        assert testobj.blacklist == {'x': 'y'}
        assert capsys.readouterr().out == ("called path.open with arg 'blacklistfile'\n"
                                           f"called json.load with arg '{blacklistfile}'\n")
        monkeypatch.setattr(testee.pathlib.Path, 'open', mock_open_2)
        testobj.build_blacklist()
        assert testobj.blacklist == {'initial': 'blacklist'}
        assert capsys.readouterr().out == ("called path.open with arg 'blacklistfile'\n"
                                           "called Base.update_blacklistfile\n")

    def test_update_blacklistfile(self, monkeypatch, capsys, tmp_path):
        """unittest for Base.update_blacklistfile
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

    def _test_doe(self, monkeypatch, capsys):
        """unittest for Base.doe
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.doe() == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_check_loc(self, monkeypatch, capsys, tmp_path):
        """unittest for Base.check_loc
        """
        def mock_readini(arg):
            print(f'called Base.readini with arg {arg}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p = {"subdirs": "x", "fromrepo": "y"}
        testobj.readini = mock_readini
        testobj.gui.vraag_subs = "subs"
        testobj.gui.vraag_repo = "repo"
        file = tmp_path / "test"
        txt = str(file)
        testobj.check_loc(txt)
        assert capsys.readouterr().out == ""
        file.touch()
        testobj.check_loc(txt + '/')
        assert capsys.readouterr().out == ""
        testobj.check_loc(txt)
        assert capsys.readouterr().out == (
                f"called Base.readini with arg {txt}\n"
                "called MainGui.set_checkbox_value with args ('subs', 'x')\n"
                "called MainGui.set_checkbox_value with args ('repo', 'y')\n")

    def test_check_type(self, monkeypatch, capsys):
        """unittest for Base.check_type
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p = {'mode': None}
        assert testobj.check_type('') == "Please select a check type"
        assert testobj.p["mode"] is None
        assert testobj.check_type('x') == ""
        assert testobj.p["mode"] == "x"

    def test_check_linter(self, monkeypatch, capsys):
        """unittest for Base.check_linter
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p = {'linter': None}
        assert testobj.check_linter('') == "Please choose a linter to use"
        assert testobj.p["linter"] is None
        assert testobj.check_linter('x') == ""
        assert testobj.p["linter"] == "x"

    def test_checkpath(self, monkeypatch, capsys, tmp_path):
        """unittest for Base.checkpath
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
        assert testobj.p["pad"] == str(path_to_check)
        assert testobj.p["filelist"] == ''
        assert capsys.readouterr().out == ("called path.expanduser\ncalled path.resolve\n")

    def test_checksubs(self, monkeypatch, capsys):
        """unittest for Base.checksubs
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.s = 'xxx'
        testobj.p = {}
        testobj.checksubs(False, True, 3)
        assert testobj.s == 'xxx'
        assert not testobj.p['subdirs']
        assert testobj.p['follow_symlinks']
        assert testobj.p['maxdepth'] == 3
        testobj.checksubs(True, True, 3)
        assert testobj.s == 'xxx en onderliggende directories'
        assert testobj.p['subdirs']
        assert testobj.p['follow_symlinks']
        assert testobj.p['maxdepth'] == 3

    def test_check_quiet_options(self, monkeypatch, capsys):
        """unittest for Base.check_quiet_options
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

    def _test_checkrepo(self, monkeypatch, capsys):
        """unittest for Base.checkrepo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.checkrepo('is_checked', 'path') == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_configure_quiet(self, monkeypatch, capsys):
        """unittest for Base.configure_quiet
        """
        def mock_show(*args):
            print('called gui.show_dialog with args', args)
            return False
        def mock_show_2(*args):
            print('called gui.show_dialog with args', args)
            return True
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.quiet_options = {}
        testobj.gui.newquietoptions = {}
        testobj.configure_quiet()
        assert testobj.quiet_options == {}
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testee.gui.QuietOptions}, {testobj.gui})\n")
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_2)
        testobj.gui.newquietoptions = {'single_file': False, 'fname': '', 'pattern': ''}
        testobj.configure_quiet()
        assert testobj.quiet_options == {'dest': testee.Mode.multi.name}
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testee.gui.QuietOptions}, {testobj.gui})\n")
        testobj.quiet_options = {}
        testobj.gui.newquietoptions = {'single_file': True, 'fname': 'xxx', 'pattern': 'yyy'}
        testobj.configure_quiet()
        assert testobj.quiet_options == {'dest': testee.Mode.single.name, 'fname': 'xxx',
                                         'pattern': 'yyy'}
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testee.gui.QuietOptions}, {testobj.gui})\n")

    def test_configure_filter(self, monkeypatch, capsys):
        """unittest for Base.configure_filter
        """
        def mock_show(*args):
            print('called gui.show_dialog with args', args)
            return False
        def mock_show_2(*args):
            print('called gui.show_dialog with args', args)
            return True
        def mock_update():
            print('called Base.update_blacklistfile')
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.update_blacklistfile = mock_update
        testobj.configure_filter()
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testee.gui.FilterOptions}, {testobj.gui})\n")
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_2)
        testobj.configure_filter()
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testee.gui.FilterOptions}, {testobj.gui})\n"
                "called Base.update_blacklistfile\n")

    def test_get_output_filename(self, monkeypatch, capsys):
        """unittest for Base.get_output_filename
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
        """unittest for Base.configure_linter
        """
        def mock_check(*args):
            nonlocal counter
            print('called MainGui.get_radiogroup_checked with args', args)
            return ''
        counter = 0
        def mock_check_2(*args):
            nonlocal counter
            print('called MainGui.get_radiogroup_checked with args', args)
            counter += 1
            if counter == 1:
                return 'x&xx'
            return ''
        def mock_check_3(*args):
            nonlocal counter
            print('called MainGui.get_radiogroup_checked with args', args)
            counter += 1
            if counter == 1:
                return 'x&xx'
            return '&Default'
        def mock_check_4(*args):
            nonlocal counter
            print('called MainGui.get_radiogroup_checked with args', args)
            counter += 1
            if counter == 1:
                return 'X&xx'
            return 'yyyy'
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
        assert capsys.readouterr().out == "called MainGui.get_radiogroup_checked with args ('qqq',)\n"
        testobj.gui.get_radiogroup_checked = mock_check_2
        testobj.configure_linter()
        assert capsys.readouterr().out == (
                "called MainGui.get_radiogroup_checked with args ('qqq',)\n"
                "called MainGui.get_radiogroup_checked with args ('check',)\n")
        counter = 0
        testobj.gui.get_radiogroup_checked = mock_check_3
        testobj.configure_linter()
        assert capsys.readouterr().out == (
                "called MainGui.get_radiogroup_checked with args ('qqq',)\n"
                "called MainGui.get_radiogroup_checked with args ('check',)\n")
        counter = 0
        testobj.gui.get_radiogroup_checked = mock_check_4
        # breakpoint()
        testobj.configure_linter()
        assert capsys.readouterr().out == (
                "called MainGui.get_radiogroup_checked with args ('qqq',)\n"
                "called MainGui.get_radiogroup_checked with args ('check',)\n"
                "called subprocess.run with args (['aa', 'ss bb'],)\n")

    def test_determine_common(self, monkeypatch, capsys):
        """unittest for Base.determine_common
        """
        # monkeypatch.setattr(testee.os.path, 'commonpath', mock_commonpath)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.mode = testee.Mode.single.value
        testobj.fnames = ['hello']
        assert testobj.determine_common() == "hello"
        testobj.mode = testee.Mode.multi.value
        testobj.fnames = ['hello/xx', 'hello/yy']
        monkeypatch.setattr(testee.os.path, 'isfile', lambda *x: False)
        assert testobj.determine_common() == "hello"
        testobj.fnames = ['hello/world/xx', 'hello/world/yy']
        monkeypatch.setattr(testee.os.path, 'isfile', lambda *x: True)
        assert testobj.determine_common() == "hello" + testee.os.sep
        testobj.mode = None
        testobj.p = {"pad": 'hello'}
        assert testobj.determine_common() == "hello" + testee.os.sep
