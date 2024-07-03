"""unittests for ./lint_core.py
"""
import types
import lint_core as testee

FIXDATE = testee.datetime.datetime(2020, 1, 1)
class MockDatetime:
    """stub for datetime.Datetime object
    """
    @classmethod
    def today(cls):
        """stub
        """
        return FIXDATE

class MockMain:
    """stub for lint_core.Main
    """
    def __init__(self, args):
        print('called Main.__init__ with arg', args)
    def determine_files(self, arg):
        print('called Main.determine_files with arg', arg)
    def lint(self, *args):
        print('called Main.lint with args', args)
    def scan(self, *args):
        print('called Main.scan with args', args)

def test_lint_all(monkeypatch, capsys, tmp_path):
    """unittest for lint_core.lint_all
    """
    def mock_chdir(arg):
        print(f"called os.chdir with arg '{arg}'")
    monkeypatch.setattr(testee.settings, 'all_repos', ['xxxx', 'yyyy', 'zzzz'])
    monkeypatch.setattr(testee.settings, 'DO_NOT_LINT', ['yyyy'])
    monkeypatch.setattr(testee.settings, 'PROJECTS_BASE', str(tmp_path))
    monkeypatch.setattr(testee.os, 'chdir', mock_chdir)
    (tmp_path / 'xxxx').mkdir()
    (tmp_path / 'yyyy').mkdir()
    (tmp_path / 'zzzz').mkdir()
    monkeypatch.setattr(testee, 'Main', MockMain)
    args = types.SimpleNamespace()
    args.project = ['qqqq']
    testee.lint_all(args)
    assert capsys.readouterr().out == "Unknown project name qqqq\n"
    args.project = ['qqqq', 'xxxx']
    testee.lint_all(args)
    assert capsys.readouterr().out == (
            "Unknown project name qqqq\n"
            f"called os.chdir with arg '{tmp_path}/xxxx'\n"
            "called Main.__init__ with arg namespace(linter='ruff', file=None, recursive=True)\n"
            ".called Main.__init__ with arg namespace(linter='flake8', file=None, recursive=True)\n"
            ".called Main.__init__ with arg namespace(linter='pylint', file=None, recursive=True)\n"
            ".ready.\n")
    args.project = ['xxxx']
    testee.lint_all(args)
    assert capsys.readouterr().out == (
            f"called os.chdir with arg '{tmp_path}/xxxx'\n"
            "called Main.__init__ with arg namespace(linter='ruff', file=None, recursive=True)\n"
            ".called Main.__init__ with arg namespace(linter='flake8', file=None, recursive=True)\n"
            ".called Main.__init__ with arg namespace(linter='pylint', file=None, recursive=True)\n"
            ".ready.\n")
    args.project = ['yyyy']
    testee.lint_all(args)
    assert capsys.readouterr().out == "yyyy is marked as do-not-lint\n"
    args.project = []
    testee.lint_all(args)
    assert capsys.readouterr().out == (
            f"called os.chdir with arg '{tmp_path}/xxxx'\n"
            "called Main.__init__ with arg namespace(linter='ruff', file=None, recursive=True)\n"
            ".called Main.__init__ with arg namespace(linter='flake8', file=None, recursive=True)\n"
            ".called Main.__init__ with arg namespace(linter='pylint', file=None, recursive=True)\n"
            ".yyyy is marked as do-not-lint\n"
            f"called os.chdir with arg '{tmp_path}/zzzz'\n"
            "called Main.__init__ with arg namespace(linter='ruff', file=None, recursive=True)\n"
            ".called Main.__init__ with arg namespace(linter='flake8', file=None, recursive=True)\n"
            ".called Main.__init__ with arg namespace(linter='pylint', file=None, recursive=True)\n"
            ".ready.\n")

class TestMain:
    """unittest for lint_core.Main
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for lint_core.Main object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Main.__init__ with args', args)
        monkeypatch.setattr(testee.Main, '__init__', mock_init)
        testobj = testee.Main()
        assert capsys.readouterr().out == 'called Main.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for Main.__init__
        """
        monkeypatch.setattr(testee.Main, 'determine_files', MockMain.determine_files)
        monkeypatch.setattr(testee.Main, 'lint', MockMain.lint)
        monkeypatch.setattr(testee.Main, 'scan', MockMain.scan)
        cwd = testee.pathlib.Path.cwd()
        args = types.SimpleNamespace(linter='xxx', file='yyy', out='zzz', recursive=False)
        testobj = testee.Main(args)
        assert capsys.readouterr().out == (
                "called Main.determine_files with arg True\n"
                f"called Main.lint with args ({cwd / 'yyy'!r}, 'zzz')\n")
        args = types.SimpleNamespace(linter='xxx', file='', out='zzz', recursive=True)
        testobj = testee.Main(args, repo_only=False)
        assert testobj.linter == args.linter
        assert capsys.readouterr().out == (
                "called Main.determine_files with arg False\n"
                f"called Main.scan with args ({cwd!r}, True)\n")

    def test_determine_files(self, monkeypatch, capsys, tmp_path):
        """unittest for Main.determine_files
        """
        def mock_cwd():
            return tmp_path
        def mock_run(*args, **kwargs):
            print('called subprocess.run with args', args, kwargs)
            return types.SimpleNamespace(stdout=b'xxx.py\nyyy.py')
        monkeypatch.setattr(testee.pathlib.Path, 'cwd', mock_cwd)
        monkeypatch.setattr(testee.subprocess, 'run', mock_run)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.files = []
        testobj.determine_files(False)
        assert testobj.files == []
        assert capsys.readouterr().out == ""

        testobj.determine_files(True)
        assert testobj.files == []
        assert capsys.readouterr().out == ""

        (tmp_path / '.hg').mkdir()
        testobj.determine_files(True)
        assert testobj.files == [tmp_path / 'xxx.py', tmp_path / 'yyy.py']
        assert capsys.readouterr().out == ("called subprocess.run with args (['hg', 'manifest'],)"
                                           " {'stdout': -1, 'check': False}\n")

        (tmp_path / '.hg').rmdir()
        (tmp_path / '.git').mkdir()
        testobj.determine_files(True)
        assert testobj.files == [tmp_path / 'xxx.py', tmp_path / 'yyy.py']
        assert capsys.readouterr().out == ("called subprocess.run with args (['git', 'ls-files'],)"
                                           " {'stdout': -1, 'check': False}\n")

    def test_lint(self, monkeypatch, capsys, tmp_path):
        """unittest for Main.lint
        """
        def mock_home():
            return tmp_path
        def mock_run(*args, **kwargs):
            print('called subprocess.run with args', args, kwargs)
            return types.SimpleNamespace(stdout=b'xxx.py\nyyy.py')
        # monkeypatch.setattr(testee.datetime.datetime, 'today', mock_today)
        monkeypatch.setattr(testee.datetime, 'datetime', MockDatetime)
        monkeypatch.setattr(testee.subprocess, 'run', mock_run)
        monkeypatch.setattr(testee.pathlib.Path, 'home', mock_home)
        monkeypatch.setattr(testee, 'CMD', {'xxx': ('yyy', '<src>')})
        monkeypatch.setattr(testee, 'ROOT', tmp_path / '.linters')
        testfilename = tmp_path / 'projects' / 'testdir' / 'testfile.py'
        testfilename.parent.mkdir(parents=True)
        testfilename.touch()
        otherfilename = tmp_path / 'testdir' / 'testdir' / 'testfile.py'
        otherfilename.parent.mkdir(parents=True)
        otherfilename.touch()

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.linter = 'xxx'
        testobj.lint(testee.pathlib.Path('item'), out='')
        assert capsys.readouterr().out == (
                "called subprocess.run with args (['yyy', 'item'],) {'check': False}\n")
        outfilename = tmp_path / 'outfile'
        testobj.lint(testee.pathlib.Path('item'), out=outfilename)
        assert capsys.readouterr().out == (
                "called subprocess.run with args (['yyy', 'item'],)"
                f" {{'stdout': <_io.TextIOWrapper name='{tmp_path}/outfile'"
                " mode='w' encoding='UTF-8'>}\n")

        testobj.lint(testfilename)
        # PosixPath('/home/albert/.linters/xxx/testdir/testfile.py-20200101000000')
        # testee.ROOT / testobj.linter /
        assert capsys.readouterr().out == (
                "called subprocess.run with args (['yyy',"
                f" '{tmp_path}/projects/testdir/testfile.py'],)"
                f" {{'stdout': <_io.TextIOWrapper name='{tmp_path}/.linters/xxx/testdir/"
                "testfile.py-20200101000000' mode='w' encoding='UTF-8'>}\n")

        testobj.lint(otherfilename)
        # PosixPath('/home/albert/.linters/xxx/testdir/testdir/testfile.py-20200101000000')
        assert capsys.readouterr().out == (
                "called subprocess.run with args (['yyy',"
                f" '{tmp_path}/testdir/testdir/testfile.py'],)"
                f" {{'stdout': <_io.TextIOWrapper name='{tmp_path}/.linters/xxx/testdir/"
                "testdir/testfile.py-20200101000000' mode='w' encoding='UTF-8'>}\n")

    def test_scan(self, monkeypatch, capsys, tmp_path):
        """unittest for Main.scan
        """
        (tmp_path / 'test').touch()
        (tmp_path / 'test.x').touch()
        (tmp_path / 'test.py').touch()
        (tmp_path / 'testing.py').touch()
        (tmp_path / '.tested.py').touch()
        (tmp_path / 'testdir').mkdir()
        (tmp_path / 'testdir' / 'testing.pyw').touch()
        (tmp_path / 'testdir' / 'test.pyw').touch()
        (tmp_path / 'testdir' / 'test.p').touch()
        (tmp_path / 'testdir' / 'testing').mkdir()
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.files = []
        monkeypatch.setattr(testee.Main, 'lint', MockMain.lint)
        testobj.scan(tmp_path)
        assert capsys.readouterr().out == (
                f"called Main.lint with args ({tmp_path / 'test'!r},)\n"
                f"called Main.lint with args ({tmp_path / 'test.py'!r},)\n"
                f"called Main.lint with args ({tmp_path / 'testing.py'!r},)\n")

        # breakpoint()
        testobj.scan(tmp_path, True)
        assert capsys.readouterr().out == (
                f"called Main.lint with args ({tmp_path / 'test'!r},)\n"
                f"called Main.lint with args ({tmp_path / 'test.py'!r},)\n"
                f"called Main.lint with args ({tmp_path / 'testing.py'!r},)\n"
                f"called Main.lint with args ({tmp_path / 'testdir' / 'testing.pyw'!r},)\n"
                f"called Main.lint with args ({tmp_path / 'testdir' / 'test.pyw'!r},)\n")

        testobj.files = [tmp_path / 'test.py', tmp_path / 'testdir' / 'testing.pyw']
        testobj.scan(tmp_path, recursive=True)
        assert capsys.readouterr().out == (
                f"called Main.lint with args ({tmp_path / 'test.py'!r},)\n"
                f"called Main.lint with args ({tmp_path / 'testdir' / 'testing.pyw'!r},)\n")
