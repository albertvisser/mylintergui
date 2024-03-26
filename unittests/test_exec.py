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
        def mock_get():
            print('called Linter.get_from_repo')
        def mock_subdirs(*args, **kwargs):
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
        assert capsys.readouterr().out == f"called Linter.subdirs with args ({testobj}, 'xxx') {{}}\n"

        testobj = testee.Linter(filelist=['xxx'], linter='z')
        assert testobj.ok
        assert testobj.rpt == ["Gecontroleerd met 'z' in xxx"]
        assert testobj.filenames == []
        assert testobj.dirnames == set()
        assert testobj.results == {}
        assert testobj.specs == ["Gecontroleerd met 'z'", " in xxx"]
        assert capsys.readouterr().out == (
                f"called Linter.subdirs with args ({testobj}, 'xxx') {{'is_list': False}}\n")

        testobj = testee.Linter(filelist=['xxx', 'yyy'], linter='z')
        assert testobj.ok
        assert testobj.rpt == ["Gecontroleerd met 'z' in opgegeven bestanden/directories"]
        assert testobj.filenames == []
        assert testobj.dirnames == set()
        assert testobj.results == {}
        assert testobj.specs == ["Gecontroleerd met 'z'", " in opgegeven bestanden/directories"]
        assert capsys.readouterr().out == (
                f"called Linter.subdirs with args ({testobj}, 'xxx') {{'is_list': False}}\n"
                f"called Linter.subdirs with args ({testobj}, 'yyy') {{'is_list': False}}\n")

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
                f"called Linter.subdirs with args ({testobj}, 'xxx') {{'is_list': False}}\n"
                f"called Linter.subdirs with args ({testobj}, 'yyy') {{'is_list': False}}\n")

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

    def _test_subdirs(self, monkeypatch, capsys):
        """unittest for Linter.subdirs
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.subdirs('pad', is_list=True, level=0) == "expected_result"
        assert capsys.readouterr().out == ("")

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
