"""unittests for ./app/exec.py
"""
import pytest
import types
from app import exec as testee


class TestLinter:
    """unittest for exec.Linter
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for exec.Linter object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Linter.__init__ with args', args)
        monkeypatch.setattr(testee.Linter, '__init__', mock_init)
        testobj = testee.Linter()
        assert capsys.readouterr().out == 'called Linter.__init__ with args ()\n'
        testobj.p = {}
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for Linter.__init__
        """
        def mock_get(self):
            print('called Linter.get_from_repo')
        def mock_subdirs(self, *args, **kwargs):
            print('called Linter.subdirs with args', args, kwargs)
        p_start = {'linter': '', 'pad': '', 'filelist': [], 'subdirs': False,
                   "follow_symlinks": False, "maxdepth": 5, 'fromrepo': False, 'mode': '',
                   'blacklist': {}}
        monkeypatch.setattr(testee.Linter, 'get_from_repo', mock_get)
        monkeypatch.setattr(testee.Linter, 'subdirs', mock_subdirs)
        with pytest.raises(ValueError) as err:
            testobj = testee.Linter(qqq='xxx')
        assert str(err.value) == 'Onbekende optie qqq'

        testobj = testee.Linter(filelist=[], pad='')
        assert testobj.p == p_start
        assert not testobj.ok
        assert testobj.rpt == ["Fout: geen lijst bestanden en geen directory opgegeven"]

        testobj = testee.Linter(filelist=['x'], pad='y')
        assert testobj.p['filelist'] == ['x']
        assert testobj.p['pad'] == 'y'
        assert not testobj.ok
        assert testobj.rpt == ["Fout: lijst bestanden én directory opgegeven"]

        testobj = testee.Linter(linter='', pad='x')
        assert testobj.p['pad'] == 'x'
        assert not testobj.ok
        assert testobj.rpt == ['Fout: geen linter opgegeven']

        testobj = testee.Linter(fromrepo='x', pad='yyy', linter='z')
        assert testobj.p['pad'] == 'yyy'
        assert testobj.p['fromrepo']
        assert testobj.ok
        assert testobj.rpt == ["Gecontroleerd met 'z' from repo manifest in yyy"]
        assert testobj.filenames == []
        assert testobj.dirnames == set()
        assert testobj.results == {}
        assert testobj.specs == ["Gecontroleerd met 'z'", ' from repo manifest in yyy']
        assert capsys.readouterr().out == "called Linter.get_from_repo\n"

        testobj = testee.Linter(pad='xxx', linter='z')
        assert testobj.ok
        assert testobj.rpt == ["Gecontroleerd met 'z' in xxx"]
        assert testobj.filenames == []
        assert testobj.dirnames == set()
        assert testobj.results == {}
        assert testobj.specs == ["Gecontroleerd met 'z'", " in xxx"]
        assert capsys.readouterr().out == "called Linter.subdirs with args ('xxx',) {}\n"

        testobj = testee.Linter(filelist=['xxx'], linter='z')
        assert testobj.ok
        assert testobj.rpt == ["Gecontroleerd met 'z' in xxx"]
        assert testobj.filenames == []
        assert testobj.dirnames == set()
        assert testobj.results == {}
        assert testobj.specs == ["Gecontroleerd met 'z'", " in xxx"]
        assert capsys.readouterr().out == (
                "called Linter.subdirs with args ('xxx',) {}\n")

        testobj = testee.Linter(filelist=['xxx', 'yyy'], linter='z')
        assert testobj.ok
        assert testobj.rpt == ["Gecontroleerd met 'z' in opgegeven bestanden/directories"]
        assert testobj.filenames == []
        assert testobj.dirnames == set()
        assert testobj.results == {}
        assert testobj.specs == ["Gecontroleerd met 'z'", " in opgegeven bestanden/directories"]
        assert capsys.readouterr().out == (
                "called Linter.subdirs with args ('xxx',) {}\n"
                "called Linter.subdirs with args ('yyy',) {}\n")

        testobj = testee.Linter(filelist=['xxx', 'yyy'], linter='z', subdirs=True)
        assert testobj.ok
        assert testobj.rpt == ["Gecontroleerd met 'z' in opgegeven bestanden/directories"
                               " en onderliggende directories"]
        assert testobj.filenames == []
        assert testobj.dirnames == set()
        assert testobj.results == {}
        assert testobj.specs == ["Gecontroleerd met 'z'", " in opgegeven bestanden/directories",
                                 " en onderliggende directories"]
        assert capsys.readouterr().out == (
                "called Linter.subdirs with args ('xxx',) {}\n"
                "called Linter.subdirs with args ('yyy',) {}\n")

    def test_get_from_repo(self, monkeypatch, capsys):
        """unittest for Linter.get_from_repo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p['blacklist'] = {'exclude_files': [], 'include_exts': ['py', 'pyw', '']}
        testobj.p['filelist'] = []
        testobj.get_from_repo()
        assert testobj.filenames == []

        testobj.p['filelist'] = ['this', 'not-this', 'only-this.py']
        testobj.get_from_repo()
        assert testobj.filenames == ['this', 'not-this', 'only-this.py']

        testobj.p['blacklist'] = {'exclude_files': ['not-this'], 'include_exts': ['py', 'pyw', '']}
        testobj.p['filelist'] = ['this', 'not-this', 'only-this.py']
        testobj.get_from_repo()
        assert testobj.filenames == ['this', 'only-this.py']

        testobj.p['blacklist'] = {'exclude_files': [], 'include_exts': ['py']}
        testobj.p['filelist'] = ['this', 'not-this.py', 'only-this.py']
        testobj.get_from_repo()
        assert testobj.filenames == ['not-this.py', 'only-this.py']

    def test_dir_is_blacklisted(self, monkeypatch, capsys):
        """unittest for Linter.dir_is_blacklisted
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p["blacklist"] = {"exclude_dirs": ["xxx", "yyy"]}
        assert not testobj.dir_is_blacklisted(testee.pathlib.Path('zzz'))
        assert testobj.dir_is_blacklisted(testee.pathlib.Path('xxx'))
        assert testobj.dir_is_blacklisted(testee.pathlib.Path('here/xxx'))

    def test_file_is_blacklisted(self, monkeypatch, capsys, tmp_path):
        """unittest for Linter.file_is_blacklisted
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p["blacklist"] = {"exclude_files": ['xxx', '.yyy']}
        assert testobj.file_is_blacklisted(testee.pathlib.Path('xxx'))
        assert testobj.file_is_blacklisted(testee.pathlib.Path('.yyy'))
        testobj.p["blacklist"] = {"exclude_files": [],
                                  "include_exts": [],
                                  "exclude_exts": ['b', 'c'],
                                  "include_shebang": []}
        assert not testobj.file_is_blacklisted(testee.pathlib.Path('xxx.a'))
        assert testobj.file_is_blacklisted(testee.pathlib.Path('zzz.b'))
        path = testee.pathlib.Path('zzz')
        assert not testobj.file_is_blacklisted(path)
        testobj.p["blacklist"] = {"exclude_files": [],
                                  "include_exts": ['a', 'b'],
                                  "exclude_exts": ['b', 'c'],
                                  "include_shebang": ['bin', 'rrr']}
        assert not testobj.file_is_blacklisted(testee.pathlib.Path('xxx.a'))
        assert testobj.file_is_blacklisted(testee.pathlib.Path('zzz.b'))
        assert testobj.file_is_blacklisted(testee.pathlib.Path('xxx.c'))
        assert testobj.file_is_blacklisted(testee.pathlib.Path('zzz.d'))
        testfile = tmp_path / 'zzz'
        testfile.touch()
        assert not testobj.file_is_blacklisted(testfile)
        testfile.write_text('#! bin\ndo_something')
        assert testobj.file_is_blacklisted(testfile)
        testfile.write_text('#! /qqq/rrr')
        assert testobj.file_is_blacklisted(testfile)
        testfile.write_text('#! qqq\n')
        assert not testobj.file_is_blacklisted(testfile)

    def test_subdirs(self, monkeypatch, capsys):
        """unittest for Linter.subdirs
        """
        class MockDirEntry:
            def __init__(self, name):
                self.path = name
        def mock_isfile(*args):
            print('called path.is_file')
            return True
        def mock_is_not_file(*args):
            print('called path.is_file')
            return False
        counter_d = 0
        def mock_is_dir(*args):
            nonlocal counter_d
            print('called path.is_dir')
            counter_d += 1
            return counter_d == 1
        def mock_is_not_dir(*args):
            print('called path.is_dir')
            return False
        def mock_issymlink(*args):
            print('called path.is_symlink')
            return True
        def mock_is_not_symlink(*args):
            print('called path.is_symlink')
            return False
        def mock_scandir(pad):
            print(f"called os.scandir with arg '{pad}'")
            return [MockDirEntry('xxx')]
        def mock_scandir_err(pad):
            print(f"called os.scandir with arg '{pad}'")
            raise PermissionError("access denied")
        def mock_dir_blacklisted(entry):
            print(f"called Linter.dir_is_blacklisted with arg '{entry}'")
            return True
        def mock_dir_not_blacklisted(entry):
            print(f"called Linter.dir_is_blacklisted with arg '{entry}'")
            return False
        counter_d_b = 0
        def mock_dir_not_blacklisted_2(entry):
            nonlocal counter_d_b
            print(f"called Linter.dir_is_blacklisted with arg '{entry}'")
            counter_d_b += 1
            return not counter_d_b == 1
        def mock_file_blacklisted(entry):
            print(f"called Linter.file_is_blacklisted with arg '{entry}'")
            return True
        def mock_file_not_blacklisted(entry):
            print(f"called Linter.file_is_blacklisted with arg '{entry}'")
            return False
        def mock_read(self):
            "stub"
        def mock_read_err(self):
            raise PermissionError("access denied")

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p['maxdepth'] = 1
        testobj.p['follow_symlinks'] = False
        testobj.p['subdirs'] = True
        testobj.dirnames = set()
        testobj.filenames = []
        testobj.rpt = []
        testobj.dir_is_blacklisted = mock_dir_blacklisted
        testobj.file_is_blacklisted = mock_file_blacklisted
        monkeypatch.setattr(testee.pathlib.Path, 'is_symlink', mock_issymlink)
        monkeypatch.setattr(testee.pathlib.Path, 'is_dir', mock_is_not_dir)
        monkeypatch.setattr(testee.pathlib.Path, 'is_file', mock_isfile)
        monkeypatch.setattr(testee.os, 'scandir', mock_scandir_err)
        testobj.dirnames = set()
        testobj.filenames = []
        testobj.rpt = []
        testobj.subdirs('mypath', level=1)
        assert testobj.dirnames == set()
        assert testobj.filenames == []
        assert testobj.rpt == ['mypath: below maximum scanlevel']
        assert capsys.readouterr().out == ""

        testobj.dirnames = set()
        testobj.filenames = []
        testobj.rpt = []
        testobj.subdirs('mypath')
        assert testobj.dirnames == set()
        assert testobj.filenames == []
        assert testobj.rpt == []
        assert capsys.readouterr().out == "called path.is_symlink\n"

        testobj.p['follow_symlinks'] = True
        testobj.dirnames = set()
        testobj.filenames = []
        testobj.rpt = []
        testobj.subdirs('myfile')
        assert testobj.dirnames == set()
        assert testobj.filenames == []
        assert testobj.rpt == []
        assert capsys.readouterr().out == ("called path.is_symlink\n"
                                           "called path.is_dir\n"
                                           "called path.is_file\n"
                                           "called Linter.file_is_blacklisted with arg 'myfile'\n")

        testobj.p['maxdepth'] = -1
        monkeypatch.setattr(testee.pathlib.Path, 'is_symlink', mock_is_not_symlink)
        monkeypatch.setattr(testee.pathlib.Path, 'read_text', mock_read)
        testobj.file_is_blacklisted = mock_file_not_blacklisted
        testobj.dirnames = set()
        testobj.filenames = []
        testobj.rpt = []
        testobj.subdirs('myfile')
        assert testobj.dirnames == set()
        assert testobj.filenames == ['myfile']
        assert testobj.rpt == []
        assert capsys.readouterr().out == ("called path.is_symlink\n"
                                           "called path.is_dir\n"
                                           "called path.is_file\n"
                                           "called Linter.file_is_blacklisted with arg 'myfile'\n")

        monkeypatch.setattr(testee.pathlib.Path, 'read_text', mock_read_err)
        testobj.dirnames = set()
        testobj.filenames = []
        testobj.rpt = []
        testobj.subdirs('myfile')
        assert testobj.dirnames == set()
        assert testobj.filenames == ['myfile']
        assert testobj.rpt == ['could not read myfile: access denied']
        assert capsys.readouterr().out == ("called path.is_symlink\n"
                                           "called path.is_dir\n"
                                           "called path.is_file\n"
                                           "called Linter.file_is_blacklisted with arg 'myfile'\n")

        monkeypatch.setattr(testee.pathlib.Path, 'is_dir', mock_is_dir)
        monkeypatch.setattr(testee.pathlib.Path, 'is_file', mock_is_not_file)
        testobj.dirnames = set()
        testobj.filenames = []
        testobj.rpt = []
        testobj.subdirs('mydir')
        assert testobj.dirnames == set()
        assert testobj.filenames == []
        assert testobj.rpt == []
        assert capsys.readouterr().out == ("called path.is_symlink\n"
                                           "called path.is_dir\n"
                                           "called Linter.dir_is_blacklisted with arg 'mydir'\n"
                                           "called path.is_file\n")

        counter_d = 0
        testobj.dir_is_blacklisted = mock_dir_not_blacklisted
        testobj.dirnames = set()
        testobj.filenames = []
        testobj.rpt = []
        testobj.subdirs('mydir')
        assert testobj.dirnames == {'mydir'}
        assert testobj.filenames == []
        assert testobj.rpt == ['could not scan mydir: access denied']
        assert capsys.readouterr().out == ("called path.is_symlink\n"
                                           "called path.is_dir\n"
                                           "called Linter.dir_is_blacklisted with arg 'mydir'\n"
                                           "called os.scandir with arg 'mydir'\n")

        counter_d = 0
        monkeypatch.setattr(testee.os, 'scandir', mock_scandir)
        testobj.dir_is_blacklisted = mock_dir_not_blacklisted_2
        testobj.dirnames = set()
        testobj.filenames = []
        testobj.rpt = []
        testobj.subdirs('mydir')
        assert testobj.dirnames == {'mydir'}
        assert testobj.filenames == []
        assert testobj.rpt == []
        assert capsys.readouterr().out == ("called path.is_symlink\n"
                                           "called path.is_dir\n"
                                           "called Linter.dir_is_blacklisted with arg 'mydir'\n"
                                           "called os.scandir with arg 'mydir'\n"
                                           "called path.is_symlink\n"
                                           "called path.is_dir\n"
                                           "called path.is_file\n")

    def test_do_action(self, monkeypatch, capsys):
        """unittest for Linter.do_action
        """
        def mock_run(*args, **kwargs):
            print('called subprocess.go with args', args, kwargs)
            return types.SimpleNamespace(stdout='')
        def mock_run_2(*args, **kwargs):
            print('called subprocess.go with args', args, kwargs)
            return types.SimpleNamespace(stdout=b'results')
        monkeypatch.setattr(testee.subprocess, 'run', mock_run)
        monkeypatch.setattr(testee, 'cmddict', {'x': {'command': ['qqq']}})
        monkeypatch.setattr(testee, 'checktypes', {'y': {'x': ['Rrr']}})
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p['linter'] = 'X'
        testobj.p['mode'] = 'y'
        testobj.filenames = ['xxx', 'yyy']
        testobj.results = {}
        testobj.do_action()
        assert testobj.results == {'xxx': 'No results for xxx', 'yyy': 'No results for yyy'}
        assert capsys.readouterr().out == (
                "called subprocess.go with args (['qqq', 'Rrr'],) {'stdout': -1, 'check': False}\n"
                "called subprocess.go with args (['qqq', 'Rrr'],) {'stdout': -1, 'check': False}\n")
        monkeypatch.setattr(testee.subprocess, 'run', mock_run_2)
        testobj.results = {}
        testobj.do_action()
        assert testobj.results == {'xxx': 'results', 'yyy': 'results'}
        assert capsys.readouterr().out == (
                "called subprocess.go with args (['qqq', 'Rrr'],) {'stdout': -1, 'check': False}\n"
                "called subprocess.go with args (['qqq', 'Rrr'],) {'stdout': -1, 'check': False}\n")
