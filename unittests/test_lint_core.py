"""unittests for ./lint_core.py
"""
import lint_core as testee


def _test_lint_all(monkeypatch, capsys):
    """unittest for lint_core.lint_all
    """
    assert testee.lint_all(args) == "expected_result"


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

    def _test_init(self, monkeypatch, capsys):
        """unittest for Main.__init__
        """
        testobj = testee.Main(args, repo_only=True)
        assert capsys.readouterr().out == ("")

    def _test_determine_files(self, monkeypatch, capsys):
        """unittest for Main.determine_files
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.determine_files(filter_repo) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_lint(self, monkeypatch, capsys):
        """unittest for Main.lint
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.lint(item, out='auto') == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_scan(self, monkeypatch, capsys):
        """unittest for Main.scan
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.scan(here, recursive=False) == "expected_result"
        assert capsys.readouterr().out == ("")
