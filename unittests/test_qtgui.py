"""unittests for ./app/qtgui.py
"""
from app import qtgui as testee


def _test_waiting_cursor(monkeypatch, capsys):
    """unittest for qtgui.waiting_cursor
    """
    assert testee.waiting_cursor(func) == "expected_result"

    def _test_wrap_operation(self, monkeypatch, capsys):
        """unittest for .wrap_operation
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.wrap_operation() == "expected_result"
        assert capsys.readouterr().out == ("")


def _test_show_dialog(monkeypatch, capsys):
    """unittest for qtgui.show_dialog
    """
    assert testee.show_dialog(cls, *args, **kwargs) == "expected_result"


class _TestFilterOptions:
    """unittest for qtgui.FilterOptions
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.FilterOptions object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called FilterOptions.__init__ with args', args)
        testobj = testee.FilterOptions()
        assert capsys.readouterr().out == 'called FilterOptions.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for FilterOptions.__init__
        """
        testobj = testee.FilterOptions(parent)
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for FilterOptions.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class _TestQuietOptions:
    """unittest for qtgui.QuietOptions
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.QuietOptions object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called QuietOptions.__init__ with args', args)
        testobj = testee.QuietOptions()
        assert capsys.readouterr().out == 'called QuietOptions.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for QuietOptions.__init__
        """
        testobj = testee.QuietOptions(parent)
        assert capsys.readouterr().out == ("")

    def _test_browse(self, monkeypatch, capsys):
        """unittest for QuietOptions.browse
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.browse() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for QuietOptions.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class _TestSelectNames:
    """unittest for qtgui.SelectNames
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.SelectNames object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SelectNames.__init__ with args', args)
        testobj = testee.SelectNames()
        assert capsys.readouterr().out == 'called SelectNames.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for SelectNames.__init__
        """
        testobj = testee.SelectNames(parent, files=True)
        assert capsys.readouterr().out == ("")

    def _test_select_all(self, monkeypatch, capsys):
        """unittest for SelectNames.select_all
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.select_all() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_invert_selection(self, monkeypatch, capsys):
        """unittest for SelectNames.invert_selection
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.invert_selection() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for SelectNames.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class _TestResults:
    """unittest for qtgui.Results
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.Results object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Results.__init__ with args', args)
        testobj = testee.Results()
        assert capsys.readouterr().out == 'called Results.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for Results.__init__
        """
        testobj = testee.Results(parent, common_path='')
        assert capsys.readouterr().out == ("")

    def _test_populate_list(self, monkeypatch, capsys):
        """unittest for Results.populate_list
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.populate_list() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_klaar(self, monkeypatch, capsys):
        """unittest for Results.klaar
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.klaar() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_refresh(self, monkeypatch, capsys):
        """unittest for Results.refresh
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.refresh() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_kopie(self, monkeypatch, capsys):
        """unittest for Results.kopie
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.kopie() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_help(self, monkeypatch, capsys):
        """unittest for Results.help
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.help() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_to_clipboard(self, monkeypatch, capsys):
        """unittest for Results.to_clipboard
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.to_clipboard() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_goto_result(self, monkeypatch, capsys):
        """unittest for Results.goto_result
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.goto_result() == "expected_result"
        assert capsys.readouterr().out == ("")


class _TestMainGui:
    """unittest for qtgui.MainGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.MainGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called MainGui.__init__ with args', args)
        testobj = testee.MainGui()
        assert capsys.readouterr().out == 'called MainGui.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for MainGui.__init__
        """
        testobj = testee.MainGui(master=None)
        assert capsys.readouterr().out == ("")

    def _test_add_combobox_row(self, monkeypatch, capsys):
        """unittest for MainGui.add_combobox_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_combobox_row(labeltext, itemlist, initial='', button=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_checkbox_row(self, monkeypatch, capsys):
        """unittest for MainGui.add_checkbox_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_checkbox_row(text, toggle=False, spinner=None, button=None) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_check_case(self, monkeypatch, capsys):
        """unittest for MainGui.check_case
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.check_case(inp) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_keyPressEvent(self, monkeypatch, capsys):
        """unittest for MainGui.keyPressEvent
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.keyPressEvent(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_radiogroup_checked(self, monkeypatch, capsys):
        """unittest for MainGui.get_radiogroup_checked
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_radiogroup_checked(group) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_meld_fout(self, monkeypatch, capsys):
        """unittest for MainGui.meld_fout
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.meld_fout(mld) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_meld_info(self, monkeypatch, capsys):
        """unittest for MainGui.meld_info
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.meld_info(msg) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_combobox_textvalue(self, monkeypatch, capsys):
        """unittest for MainGui.get_combobox_textvalue
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_combobox_textvalue(widget) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_set_checkbox_value(self, monkeypatch, capsys):
        """unittest for MainGui.set_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.set_checkbox_value(widget, value) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for MainGui.get_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_checkbox_value(widget) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_get_spinbox_value(self, monkeypatch, capsys):
        """unittest for MainGui.get_spinbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_spinbox_value(widget) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_execute_action(self, monkeypatch, capsys):
        """unittest for MainGui.execute_action
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.execute_action() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_zoekdir(self, monkeypatch, capsys):
        """unittest for MainGui.zoekdir
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.zoekdir() == "expected_result"
        assert capsys.readouterr().out == ("")
