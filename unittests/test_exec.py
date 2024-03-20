"""unittests for ./app/exec.py
"""
from app import exec as testee


class _TestLinter:
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
        testobj = testee.Linter()
        assert capsys.readouterr().out == 'called Linter.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for Linter.__init__
        """
        testobj = testee.Linter(**parms)
        assert capsys.readouterr().out == ("")

    def _test_get_from_repo(self, monkeypatch, capsys):
        """unittest for Linter.get_from_repo
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_from_repo() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_subdirs(self, monkeypatch, capsys):
        """unittest for Linter.subdirs
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.subdirs(pad, is_list=True, level=0) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_do_action(self, monkeypatch, capsys):
        """unittest for Linter.do_action
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.do_action() == "expected_result"
        assert capsys.readouterr().out == ("")
