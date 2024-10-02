"""unittests for ./app/qtgui.py
"""
import types
import pytest
from mockgui import mockqtwidgets as mockqtw
from app import qtgui as testee
from output_fixture import expected_output


class MockBase:
    """stub for main.Base object
    """
    def __init__(self, *args, **kwargs):
        print('called Base.__init__ with args', args, kwargs)
    def get_output_filename(self, *args):
        "stub"
        print("called Base.get_output_filename with args", args)
        if len(args) == 1:
            return args[0]
        return args[0].format(args[1])
    def configure_linter(self):
        "empty because we only need the reference to the method"
    def configure_filter(self):
        "empty because we only need the reference to the method"
    def configure_quiet(self):
        "empty because we only need the reference to the method"
    def check_loc(self):
        "empty because we only need the reference to the method"
    def doe(self):
        "empty because we only need the reference to the method"


class MockMainGui:
    """stub for qtgui.MainGui object
    """
    def __init__(self, *args, **kwargs):
        "stub"
        print('called MainGui.__init__ with args', args, kwargs)
    def execute_action(self):
        "stub"
        print('called MainGui.execute_action')


class MockFinder:
    """stub for findr_files.Finder
    """
    rpt = ['rpttitel']
    results = {'xxx': ['line0', 'line1'], 'yyy': ['aaa', 'bbb'], 'current text': 'abcd'}
    filenames = ['xxx', 'yyy']
    fname = 'qqq'
    specs = ['specs', 'and more specs']

    def do_action(self):
        "stub"
        print('called Finder.do_action')


def _test_waiting_cursor(monkeypatch, capsys):
    """unittest for qtgui.waiting_cursor
    """
    @testee.waiting_cursor
    def wrapped(arg):
        print('called wrapped function with arg', arg)
    assert testee.waiting_cursor(wrapped) == "expected_result"
    assert capsys.readouterr().out == ("")
    # wordt meegetest met MainGui.execute_action


def test_show_dialog(monkeypatch, capsys):
    """unittest for qtgui.show_dialog
    """
    def mock_exec(cls):
        print('called Dialog.exec')
        return True
    mockparent = 'parent'
    monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
    monkeypatch.setattr(testee.qtw.QDialog, 'exec', mockqtw.MockDialog.exec)
    cls = testee.qtw.QDialog
    assert not testee.show_dialog(cls, mockparent)
    assert capsys.readouterr().out == ("called Dialog.__init__ with args parent () {}\n"
                                       "called Dialog.exec\n")
    monkeypatch.setattr(testee.qtw.QDialog, 'exec', mock_exec)
    cls = testee.qtw.QDialog
    assert testee.show_dialog(cls, mockparent)
    assert capsys.readouterr().out == ("called Dialog.__init__ with args parent () {}\n"
                                       "called Dialog.exec\n")


class TestFilterOptions:
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
        monkeypatch.setattr(testee.FilterOptions, '__init__', mock_init)
        testobj = testee.FilterOptions()
        testobj.parent = MockMainGui()
        testobj.parent.master = MockBase()
        assert capsys.readouterr().out == ('called FilterOptions.__init__ with args ()\n'
                                           "called MainGui.__init__ with args () {}\n"
                                           "called Base.__init__ with args () {}\n")
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for FilterOptions.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        parent = MockMainGui()
        parent.master = MockBase()
        assert capsys.readouterr().out == ("called MainGui.__init__ with args () {}\n"
                                           "called Base.__init__ with args () {}\n")
        parent.master.title = 'Title'
        parent.master.blacklist = {'exclude_dirs': ['xxx', 'yyy'], 'exclude_exts': ['a', 'b'],
                                   'exclude_files': ['f', 'g'], 'include_exts': ['aa', 'bb'],
                                   'include_shebang': ['#!x', '#!y']}
        parent.appicon = "app icon"
        testobj = testee.FilterOptions(parent)
        assert capsys.readouterr().out == expected_output["filteroptions"].format(testobj=testobj,
                                                                                  parent=parent)

    def test_accept(self, monkeypatch, capsys):
        """unittest for FilterOptions.accept
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.skipdirs = mockqtw.MockLineEdit('x, y')
        testobj.skipexts = mockqtw.MockLineEdit('a, b')
        testobj.do_exts = mockqtw.MockLineEdit('c, d')
        testobj.skipfiles = mockqtw.MockLineEdit('p, q')
        testobj.do_bangs = mockqtw.MockLineEdit('#, @')
        assert capsys.readouterr().out == 'called LineEdit.__init__\n' * 5
        testobj.accept()
        assert testobj.parent.master.blacklist == {'exclude_dirs': ['x', 'y'],
                                                   'exclude_exts': ['a', 'b'],
                                                   'include_exts': ['c', 'd'],
                                                   'exclude_files': ['p', 'q'],
                                                   'include_shebang': ['#', '@']}
        assert capsys.readouterr().out == 'called LineEdit.text\n' * 5 + 'called Dialog.accept\n'


class TestQuietOptions:
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
        monkeypatch.setattr(testee.QuietOptions, '__init__', mock_init)
        testobj = testee.QuietOptions()
        testobj.parent = MockMainGui()
        testobj.parent.master = MockBase()
        assert capsys.readouterr().out == ('called QuietOptions.__init__ with args ()\n'
                                           "called MainGui.__init__ with args () {}\n"
                                           "called Base.__init__ with args () {}\n")
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for QuietOptions.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QRadioButton', mockqtw.MockRadioButton)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        parent = MockMainGui()
        parent.master = MockBase()
        assert capsys.readouterr().out == ("called MainGui.__init__ with args () {}\n"
                                           "called Base.__init__ with args () {}\n")
        parent.master.title = 'Title'
        parent.appicon = "app icon"
        parent.master.quiet_options = {'fname': 'xxx', 'pattern': 'yyy', 'ignore': 'zzz', 'dest': ''}
        parent.master.dest_from_input = False
        testobj = testee.QuietOptions(parent)
        assert isinstance(testobj.single, testee.qtw.QRadioButton)
        assert isinstance(testobj.fname, testee.qtw.QLineEdit)
        assert isinstance(testobj.multi, testee.qtw.QRadioButton)
        assert isinstance(testobj.pattern, testee.qtw.QLineEdit)
        assert isinstance(testobj.ignore, testee.qtw.QLineEdit)
        assert capsys.readouterr().out == expected_output['quietoptions'].format(testobj=testobj,
                                                                                 parent=parent)
        parent.master.quiet_options = {'fname': 'xxx', 'pattern': 'yyy', 'ignore': 'zzz',
                                       'dest': testee.Mode.single.name}
        parent.master.dest_from_input = True
        testobj = testee.QuietOptions(parent)
        assert isinstance(testobj.single, testee.qtw.QRadioButton)
        assert isinstance(testobj.fname, testee.qtw.QLineEdit)
        assert isinstance(testobj.multi, testee.qtw.QRadioButton)
        assert isinstance(testobj.pattern, testee.qtw.QLineEdit)
        assert isinstance(testobj.ignore, testee.qtw.QLineEdit)
        assert capsys.readouterr().out == expected_output['quietoptions2'].format(testobj=testobj,
                                                                                  parent=parent)

        parent.master.quiet_options = {'fname': 'xxx', 'pattern': 'yyy', 'ignore': 'zzz',
                                       'dest': testee.Mode.multi.name}
        testobj = testee.QuietOptions(parent)
        assert isinstance(testobj.single, testee.qtw.QRadioButton)
        assert isinstance(testobj.fname, testee.qtw.QLineEdit)
        assert isinstance(testobj.multi, testee.qtw.QRadioButton)
        assert isinstance(testobj.pattern, testee.qtw.QLineEdit)
        assert isinstance(testobj.ignore, testee.qtw.QLineEdit)
        assert capsys.readouterr().out == expected_output['quietoptions3'].format(testobj=testobj,
                                                                                  parent=parent)

    def _test_browse(self, monkeypatch, capsys):
        """unittest for QuietOptions.browse
        """
        # not implemented, no test necessary
        # testobj = self.setup_testobj(monkeypatch, capsys)
        # assert testobj.browse() == "expected_result"
        # assert capsys.readouterr().out == ("")

    def test_accept(self, monkeypatch, capsys):
        """unittest for QuietOptions.accept
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.single = mockqtw.MockRadioButton()
        testobj.fname = mockqtw.MockLineEdit('xxx')
        testobj.pattern = mockqtw.MockLineEdit('yyy')
        testobj.ignore = mockqtw.MockLineEdit('zzz')
        assert capsys.readouterr().out == ("called RadioButton.__init__ with args () {}\n"
                                           + 'called LineEdit.__init__\n' * 3)
        testobj.accept()
        assert capsys.readouterr().out == ('called RadioButton.isChecked\n'
                                           + 'called LineEdit.text\n' * 3 + 'called Dialog.accept\n')


class TestSelectNames:
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
        monkeypatch.setattr(testee.SelectNames, '__init__', mock_init)
        testobj = testee.SelectNames()
        testobj.parent = MockMainGui()
        testobj.parent.master = MockBase()
        assert capsys.readouterr().out == ('called SelectNames.__init__ with args ()\n'
                                           "called MainGui.__init__ with args () {}\n"
                                           "called Base.__init__ with args () {}\n")
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for SelectNames.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.gui, 'QIcon', mockqtw.MockIcon)
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QScrollArea', mockqtw.MockScrollArea)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        parent = MockMainGui()
        parent.master = MockBase()
        assert capsys.readouterr().out == ("called MainGui.__init__ with args () {}\n"
                                           "called Base.__init__ with args () {}\n")
        parent.master.title = 'Title'
        parent.master.names = ['xxx', 'yyy']
        parent.appicon = "app icon"
        testobj = testee.SelectNames(parent)
        assert testobj.dofiles
        assert testobj.parent == parent
        assert isinstance(testobj.sel_all, testee.qtw.QCheckBox)
        assert isinstance(testobj.flip_sel, testee.qtw.QPushButton)
        assert len(testobj.checklist) == 2
        assert isinstance(testobj.checklist[0], testee.qtw.QCheckBox)
        assert isinstance(testobj.checklist[1], testee.qtw.QCheckBox)
        assert capsys.readouterr().out == expected_output['selectnames'].format(testobj=testobj)
        parent.master.names = ['xxx', 'yyy']
        testobj = testee.SelectNames(parent, files=False)
        assert not testobj.dofiles
        assert testobj.parent == parent
        assert isinstance(testobj.sel_all, testee.qtw.QCheckBox)
        assert isinstance(testobj.flip_sel, testee.qtw.QPushButton)
        assert len(testobj.checklist) == 2
        assert isinstance(testobj.checklist[0], testee.qtw.QCheckBox)
        assert isinstance(testobj.checklist[1], testee.qtw.QCheckBox)
        assert capsys.readouterr().out == expected_output['selectnames_2'].format(testobj=testobj)

    def test_select_all(self, monkeypatch, capsys):
        """unittest for SelectNames.select_all
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sel_all = mockqtw.MockCheckBox()
        testobj.checklist = [mockqtw.MockCheckBox(), mockqtw.MockCheckBox()]
        assert capsys.readouterr().out == "called CheckBox.__init__\n" * 3
        testobj.select_all()
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n")

    def test_invert_selection(self, monkeypatch, capsys):
        """unittest for SelectNames.invert_selection
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.checklist = [mockqtw.MockCheckBox(), mockqtw.MockCheckBox()]
        testobj.checklist[0].setChecked(False)
        testobj.checklist[1].setChecked(False)
        assert capsys.readouterr().out == ("called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.setChecked with arg False\n"
                                           "called CheckBox.setChecked with arg False\n")
        testobj.invert_selection()
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.setChecked with arg True\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for SelectNames.accept
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.checklist = [mockqtw.MockCheckBox('xxx'), mockqtw.MockCheckBox('yyy')]
        testobj.checklist[0].setChecked(True)
        testobj.checklist[1].setChecked(False)
        assert capsys.readouterr().out == ("called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.setChecked with arg False\n")

        testobj.parent.master.names = ['xxx', 'yyy']
        testobj.dofiles = False
        testobj.accept()
        assert testobj.parent.master.names == ['xxx']
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called Dialog.accept\n")

        testobj.parent.master.names = ['xxx', 'yyy']
        testobj.dofiles = True
        testobj.accept()
        assert testobj.parent.master.names == ['yyy']
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called Dialog.accept\n")


class TestResults:
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
        monkeypatch.setattr(testee.Results, '__init__', mock_init)
        testobj = testee.Results()
        testobj.parent = MockMainGui()
        testobj.parent.master = MockBase()
        testobj.parent.master.do_checks = MockFinder()
        assert capsys.readouterr().out == ('called Results.__init__ with args ()\n'
                                           "called MainGui.__init__ with args () {}\n"
                                           "called Base.__init__ with args () {}\n")
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for Results.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw.QWidget, 'resize', mockqtw.MockWidget.resize)
        monkeypatch.setattr(testee.qtw.QDialog, 'exec', mockqtw.MockDialog.exec)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.gui, 'QFont', mockqtw.MockFont)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(testee.qtw, 'QTextEdit', mockqtw.MockEditorWidget)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        parent = MockMainGui()
        parent.master = MockBase()
        parent.master.do_checks = MockFinder()
        assert capsys.readouterr().out == ("called MainGui.__init__ with args () {}\n"
                                           "called Base.__init__ with args () {}\n")
        parent.master.resulttitel = 'Title'
        parent.master.names = ['xxx', 'yyy']
        parent.appicon = "app icon"
        parent.master.mode = ''
        testobj = testee.Results(parent, common_path='')
        assert testobj.parent == parent
        assert testobj.common == ''
        assert testobj.results == []
        assert isinstance(testobj.txt, testee.qtw.QLabel)
        assert isinstance(testobj.filelist, testee.qtw.QComboBox)
        assert isinstance(testobj.lijst, testee.qtw.QTextEdit)
        assert capsys.readouterr().out == expected_output['results'].format(testobj=testobj)
        parent.master.mode = testee.Mode.multi.value
        monkeypatch.setattr(testee, 'common_path_txt', '{} yyy')
        testobj = testee.Results(parent, common_path='xxx')
        assert testobj.parent == parent
        assert testobj.common == 'xxx'
        assert testobj.results == []
        assert isinstance(testobj.txt, testee.qtw.QLabel)
        assert isinstance(testobj.filelist, testee.qtw.QComboBox)
        assert isinstance(testobj.lijst, testee.qtw.QTextEdit)
        assert capsys.readouterr().out == expected_output['results2'].format(testobj=testobj)

    def test_populate_list(self, monkeypatch, capsys):
        """unittest for Results.populate_list
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.filelist = mockqtw.MockComboBox()
        testobj.filelist.setCurrentText('text')
        testobj.lijst = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called ComboBox.setCurrentText with arg `text`\n"
                                           "called Editor.__init__\n")
        testobj.populate_list()
        assert capsys.readouterr().out == ("called ComboBox.currentText\n"
                                           "called Editor.setText with arg `abcd`\n")

    def test_klaar(self, monkeypatch, capsys):
        """unittest for Results.klaar
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'done', mockqtw.MockDialog.done)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.klaar()
        assert capsys.readouterr().out == ("called Dialog.done with arg `0`\n")

    def test_refresh(self, monkeypatch, capsys):
        """unittest for Results.refresh
        """
        def mock_populate():
            print('called Results.populate_list')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.populate_list = mock_populate
        testobj.lijst = mockqtw.MockEditorWidget()
        testobj.filelist = mockqtw.MockComboBox()
        testobj.refresh()
        assert capsys.readouterr().out == ("called Editor.__init__\n"
                                           "called ComboBox.__init__\n"
                                           "called Editor.clear\n"
                                           "called MainGui.execute_action\n"
                                           "called Results.populate_list\n"
                                           "called ComboBox.setCurrentIndex with arg `0`\n")

    def test_kopie(self, monkeypatch, capsys, tmp_path):
        """unittest for Results.kopie
        """
        def mock_exec(self):
            print('called Dialog.exec')
            return True
        def mock_out(*args):
            print("called Base.get_output_filename with args", args)
            if len(args) == 1:
                return str(tmp_path / args[0])
            return str(tmp_path / args[0].format(args[1]))
        monkeypatch.setattr(testee, 'QuietOptions', mockqtw.MockDialog)
        monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mockqtw.MockMessageBox.information)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.master.title = 'title'
        testobj.parent.master.do_checks.results = {'xx': 'abcdefg', 'yy': 'hijklmn'}
        testobj.parent.master.get_output_filename = mock_out
        testobj.parent.newquietoptions = {'single_file': True, 'fname': 'filename'}
        testobj.kopie()
        assert capsys.readouterr().out == (
                f"called Dialog.__init__ with args {testobj.parent} () {{}}\n"
                "called Dialog.exec\n")
        monkeypatch.setattr(testee.QuietOptions, 'exec', mock_exec)
        # breakpoint()
        testobj.kopie()
        assert (tmp_path / 'filename').read_text() == ('results for xx\n\nabcdefg\n\n\n'
                                                       'results for yy\n\nhijklmn\n')
        assert capsys.readouterr().out == (
                f"called Dialog.__init__ with args {testobj.parent} () {{}}\n"
                "called Dialog.exec\n"
                f"called Base.get_output_filename with args ('filename',)\n"
                f"called MessageBox.information with args `{testobj}` `title`"
                f" `Output saved as {tmp_path}/filename`\n")
        testobj.parent.newquietoptions = {'single_file': False, 'pattern': '{}z'}
        testobj.kopie()
        assert (tmp_path / 'xxz').read_text() == 'results for xx\n\nabcdefg\n'
        assert (tmp_path / 'yyz').read_text() == 'results for yy\n\nhijklmn\n'
        assert capsys.readouterr().out == (
                f"called Dialog.__init__ with args {testobj.parent} () {{}}\n"
                "called Dialog.exec\n"
                f"called Base.get_output_filename with args ('{{}}z', 'xx')\n"
                f"called Base.get_output_filename with args ('{{}}z', 'yy')\n"
                f"called MessageBox.information with args `{testobj}` `title`"
                f" `Last output saved as {tmp_path}/yyz`\n")

    def test_help(self, monkeypatch, capsys):
        """unittest for Results.help
        """
        monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mockqtw.MockMessageBox.information)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.master.title = 'title'
        testobj.helpinfo = "help info"
        testobj.help()
        assert capsys.readouterr().out == (
                f"called MessageBox.information with args `{testobj}` `title` `help info`\n")

    def test_to_clipboard(self, monkeypatch, capsys):
        """unittest for Results.to_clipboard
        """
        monkeypatch.setattr(testee.qtw.QApplication, 'clipboard',
                            mockqtw.MockApplication.clipboard)
        monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mockqtw.MockMessageBox.information)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.master.title = 'title'
        testobj.parent.master.do_checks.results = {'xx': 'abcdefg', 'yy': 'hijklmn'}
        testobj.to_clipboard()
        assert capsys.readouterr().out == (
                "called Application.clipboard\n"
                "called ClipBoard.__init__\n"
                "called Clipboard.setText with arg 'results for xx\n\nabcdefg\n\n\n"
                "results for yy\n\nhijklmn'\n"
                "called MessageBox.information with args"
                f" `{testobj}` `title` `Output copied to clipboard`\n")

    def test_goto_result(self, monkeypatch, capsys):
        """unittest for Results.goto_result
        """
        def mock_run(*args, **kwargs):
            print('called subprocess.run with args', args, kwargs)
        monkeypatch.setattr(testee.subprocess, 'run', mock_run)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.master.editor_option = [['x', 'y'], '{}', 'a', 'b']
        testobj.filelist = mockqtw.MockComboBox()
        testobj.goto_result()
        assert capsys.readouterr().out == (
                "called ComboBox.__init__\n"
                "called ComboBox.currentText\n"
                "called subprocess.run with args (['x', 'y', 'current text'],) {'check': False}\n")


class TestMainGui:
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
        monkeypatch.setattr(testee.MainGui, '__init__', mock_init)
        testobj = testee.MainGui()
        testobj.app = mockqtw.MockApplication()
        testobj.master = MockBase()
        assert capsys.readouterr().out == ("called MainGui.__init__ with args ()\n"
                                           "called Application.__init__\n"
                                           "called Base.__init__ with args () {}\n")
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for MainGui.__init__
        """
        monkeypatch.setattr(testee.qtw.QApplication, '__init__', mockqtw.MockApplication.__init__)
        monkeypatch.setattr(testee.qtw.QWidget, '__init__', mockqtw.MockWidget.__init__)
        monkeypatch.setattr(testee.qtw.QWidget, 'setWindowTitle', mockqtw.MockWidget.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QWidget, 'setWindowIcon', mockqtw.MockWidget.setWindowIcon)
        monkeypatch.setattr(testee.gui.QIcon, '__init__', mockqtw.MockIcon.__init__)
        master = MockBase()
        master.title = 'A title'
        master.iconame = 'icon name'
        testobj = testee.MainGui(master)
        assert testobj.master == master
        assert isinstance(testobj.appicon, testee.gui.QIcon)
        assert capsys.readouterr().out == ("called Base.__init__ with args () {}\n"
                                           "called Application.__init__\n"
                                           "called Widget.__init__\n"
                                           "called Widget.setWindowTitle with arg `A title`\n"
                                           "called Icon.__init__ with arg `icon name`\n"
                                           "called Widget.setWindowIcon\n")

    def test_setup_screen(self, monkeypatch, capsys, tmp_path, expected_output):
        """unittest for MainGui.setup_screen
        """
        def mock_add_combo(*args, **kwargs):
            print('called Base.add_combobox_line with args', args, kwargs)
            return mockqtw.MockComboBox()
        def mock_add_check(*args, **kwargs):
            print('called Base.add_checkbox_line with args', args, kwargs)
            return mockqtw.MockCheckBox()
        def mock_setlayout(arg):
            print(f'called MainGui.setLayout with arg of type {type(arg)}')
        def mock_doe():
            print('called Base.doe')
        def mock_show():
            print('called MainGui.show')
        def mock_close():
            print('called MainGui.close')
        monkeypatch.setattr(testee, 'checktypes', ['xxx', 'yyy'])
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.gui, 'QFont', mockqtw.MockFont)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QButtonGroup', mockqtw.MockButtonGroup)
        monkeypatch.setattr(testee.qtw, 'QRadioButton', mockqtw.MockRadioButton)
        monkeypatch.setattr(testee.qtw, 'QListWidget', mockqtw.MockListBox)
        monkeypatch.setattr(testee.qtw, 'QSpinBox', mockqtw.MockSpinBox)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(mockqtw.MockComboBox, 'editTextChanged', {str: mockqtw.MockSignal()})
        assert capsys.readouterr().out == "called Signal.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_combobox_row = mock_add_combo
        testobj.add_checkbox_row = mock_add_check
        testobj.master.mode = testee.Mode.standard.value
        testobj.master.linter_from_input = 'ruff'
        testobj.master.dest_from_input = False
        testobj.master._mru_items = {'dirs': ['aaa']}
        testobj.master.checking_type = 'xxx'
        testobj.master.repo_only = False
        testobj.master.p = {'subdirs': False, 'filelist': []}
        testobj.master.doe = mock_doe
        testobj.setLayout = mock_setlayout
        testobj.show = mock_show
        testobj.close = mock_close
        testobj.master.skip_screen = False
        with pytest.raises(SystemExit):
            testobj.setup_screen()
        assert isinstance(testobj.grid, testee.qtw.QGridLayout)
        lastrow = 8
        assert testobj.row == lastrow
        assert isinstance(testobj.check_options, testee.qtw.QButtonGroup)
        assert isinstance(testobj.linters, testee.qtw.QButtonGroup)
        assert capsys.readouterr().out == expected_output['maingui_standard'].format(testobj=testobj,
                                                                                     fname='',
                                                                                     extra='',
                                                                                     row=lastrow)
        fname = tmp_path / 'xxx'
        testobj.master.p['filelist'] = [str(fname)]
        with pytest.raises(SystemExit):
            testobj.setup_screen()
        assert isinstance(testobj.grid, testee.qtw.QGridLayout)
        lastrow = 8
        assert testobj.row == lastrow
        assert isinstance(testobj.check_options, testee.qtw.QButtonGroup)
        assert isinstance(testobj.linters, testee.qtw.QButtonGroup)
        assert capsys.readouterr().out == expected_output['maingui_standard2'].format(testobj=testobj,
                                                                                      fname=fname,
                                                                                      extra='',
                                                                                      row=lastrow)

        testobj.master.mode = testee.Mode.single.value
        testobj.master.checking_type = 'zzz'
        testobj.master.linter_from_input = ''
        # fname.touch()
        with pytest.raises(SystemExit):
            testobj.setup_screen()
        assert isinstance(testobj.grid, testee.qtw.QGridLayout)
        lastrow = 6
        assert testobj.row == lastrow
        assert isinstance(testobj.check_options, testee.qtw.QButtonGroup)
        assert isinstance(testobj.linters, testee.qtw.QButtonGroup)
        assert capsys.readouterr().out == expected_output['maingui_single1'].format(testobj=testobj,
                                                                                    fname=fname,
                                                                                    row=lastrow)

        # fname.unlink()
        fname.mkdir()
        with pytest.raises(SystemExit):
            testobj.setup_screen()
        assert isinstance(testobj.grid, testee.qtw.QGridLayout)
        lastrow = 6
        assert testobj.row == lastrow
        assert isinstance(testobj.check_options, testee.qtw.QButtonGroup)
        assert isinstance(testobj.linters, testee.qtw.QButtonGroup)
        assert capsys.readouterr().out == expected_output['maingui_single2'].format(testobj=testobj,
                                                                                    fname=fname,
                                                                                    extra='',
                                                                                    row=lastrow)

        testobj.master.mode = testee.Mode.multi.value
        testobj.master.p['filelist'] = ['xxx', 'yyy']
        with pytest.raises(SystemExit):
            testobj.setup_screen()
        assert isinstance(testobj.grid, testee.qtw.QGridLayout)
        lastrow = 8
        assert testobj.row == lastrow
        assert isinstance(testobj.check_options, testee.qtw.QButtonGroup)
        assert isinstance(testobj.linters, testee.qtw.QButtonGroup)
        extra = 'van geselecteerde directories '
        assert capsys.readouterr().out == expected_output['maingui_multi'].format(testobj=testobj,
                                                                                  extra=extra,
                                                                                  row=lastrow)

        testobj.master.skip_screen = True
        testobj.setup_screen()
        assert isinstance(testobj.grid, testee.qtw.QGridLayout)
        lastrow = 8
        assert testobj.row == lastrow
        assert isinstance(testobj.check_options, testee.qtw.QButtonGroup)
        assert isinstance(testobj.linters, testee.qtw.QButtonGroup)
        assert capsys.readouterr().out == expected_output['maingui_nogui'].format(testobj=testobj,
                                                                                  extra=extra,
                                                                                  row=lastrow)

    def test_add_combobox_row(self, monkeypatch, capsys, expected_output):
        """unittest for MainGui.add_combobox_row
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockqtw.MockGridLayout()
        button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called Grid.__init__\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.row = 1
        result = testobj.add_combobox_row('label text', ['item', 'list'])
        assert isinstance(result, testee.qtw.QComboBox)
        assert testobj.row == 2
        assert capsys.readouterr().out == expected_output['combobox_row1'].format(row=testobj.row)
        result = testobj.add_combobox_row('label text', ['item', 'list'], 'start', button)
        assert isinstance(result, testee.qtw.QComboBox)
        assert testobj.row == 3
        assert capsys.readouterr().out == expected_output['combobox_row2'].format(row=testobj.row)

    def test_add_checkbox_row(self, monkeypatch, capsys, expected_output):
        """unittest for MainGui.add_checkbox_row
        """
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockqtw.MockGridLayout()
        button = mockqtw.MockPushButton()
        spinner = mockqtw.MockSpinBox()
        assert capsys.readouterr().out == ("called Grid.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called SpinBox.__init__\n")
        testobj.row = 1
        result = testobj.add_checkbox_row('text')
        assert isinstance(result, testee.qtw.QCheckBox)
        assert testobj.row == 2
        assert capsys.readouterr().out == expected_output['checkbox_row'].format(row=testobj.row)
        result = testobj.add_checkbox_row('text', spinner=spinner)
        assert isinstance(result, testee.qtw.QCheckBox)
        assert testobj.row == 3
        assert capsys.readouterr().out == expected_output['checkbox_row2'].format(row=testobj.row)
        result = testobj.add_checkbox_row('text', True, button=button)
        assert isinstance(result, testee.qtw.QCheckBox)
        assert testobj.row == 4
        assert capsys.readouterr().out == expected_output['checkbox_row3'].format(row=testobj.row)

    # def _test_check_case(self, monkeypatch, capsys):
    #     """unittest for MainGui.check_case
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     assert testobj.check_case(inp) == "expected_result"
    #     assert capsys.readouterr().out == ("")

    def test_keyPressEvent(self, monkeypatch, capsys):
        """unittest for MainGui.keyPressEvent
        """
        def mock_close():
            print('called MainGui.close')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.close = mock_close
        event = types.SimpleNamespace(key=lambda: 'anything')
        testobj.keyPressEvent(event)
        assert capsys.readouterr().out == ""
        event = types.SimpleNamespace(key=lambda: testee.core.Qt.Key.Key_Escape)
        testobj.keyPressEvent(event)
        assert capsys.readouterr().out == "called MainGui.close\n"

    def test_get_radiogroup_checked(self, monkeypatch, capsys):
        """unittest for MainGui.get_radiogroup_checked
        """
        button = mockqtw.MockRadioButton('x&Xx')
        assert capsys.readouterr().out == ("called RadioButton.__init__ with args ('x&Xx',) {}\n")
        def mock_checked():
            print('called ButtonGroup.checkedButton')
            return button
        testobj = self.setup_testobj(monkeypatch, capsys)
        group = mockqtw.MockButtonGroup()
        assert capsys.readouterr().out == ("called ButtonGroup.__init__ with args ()\n")
        assert testobj.get_radiogroup_checked(group) is None
        assert capsys.readouterr().out == ("called ButtonGroup.checkedButton\n")
        group.checkedButton = mock_checked
        assert testobj.get_radiogroup_checked(group) == "xxx"
        assert capsys.readouterr().out == ("called ButtonGroup.checkedButton\n")

    def test_meld_fout(self, monkeypatch, capsys):
        """unittest for MainGui.meld_fout
        """
        monkeypatch.setattr(testee.qtw.QMessageBox, 'critical', mockqtw.MockMessageBox.critical)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.fouttitel = 'xxx'
        testobj.meld_fout('message')
        assert capsys.readouterr().out == (
                f"called MessageBox.critical with args `{testobj}` `xxx` `message`\n")

    def test_meld_info(self, monkeypatch, capsys):
        """unittest for MainGui.meld_info
        """
        monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mockqtw.MockMessageBox.information)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.resulttitel = 'xxx'
        testobj.meld_info('message')
        assert capsys.readouterr().out == (
                f"called MessageBox.information with args `{testobj}` `xxx` `message`\n")

    def test_get_combobox_textvalue(self, monkeypatch, capsys):
        """unittest for MainGui.get_combobox_textvalue
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        widget = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        assert testobj.get_combobox_textvalue(widget) == "current text"
        assert capsys.readouterr().out == ("called ComboBox.currentText\n")

    def test_set_checkbox_value(self, monkeypatch, capsys):
        """unittest for MainGui.set_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        widget = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        testobj.set_checkbox_value(widget, True)
        assert capsys.readouterr().out == "called CheckBox.setChecked with arg True\n"

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for MainGui.get_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        widget = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        assert not testobj.get_checkbox_value(widget)
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n")

    def test_get_spinbox_value(self, monkeypatch, capsys):
        """unittest for MainGui.get_spinbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        widget = mockqtw.MockSpinBox()
        assert capsys.readouterr().out == "called SpinBox.__init__\n"
        assert testobj.get_spinbox_value(widget) == 0
        assert capsys.readouterr().out == ("called SpinBox.value\n")

    def test_execute_action(self, monkeypatch, capsys):
        """unittest for MainGui.execute_action
        """
        monkeypatch.setattr(testee.gui, 'QCursor', mockqtw.MockCursor)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.app = mockqtw.MockApplication()
        assert capsys.readouterr().out == "called Application.__init__\n"
        testobj.master.do_checks = MockFinder()
        testobj.execute_action()
        assert capsys.readouterr().out == (
                f"called Cursor.__init__ with arg {testee.core.Qt.CursorShape.WaitCursor}\n"
                "called Application.setOverrideCursor with arg of type"
                " <class 'mockgui.mockqtwidgets.MockCursor'>\n"
                "called Finder.do_action\n"
                "called Application.restoreOverrideCursor\n")

    def test_zoekdir(self, monkeypatch, capsys):
        """unittest for MainGui.zoekdir
        """
        def mock_get_dir(parent, *args, **kwargs):
            print('called FileDialog.getExistingDirectory with args', parent, args, kwargs)
            return 'xyz'
        monkeypatch.setattr(testee.qtw, 'QFileDialog', mockqtw.MockFileDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vraag_dir = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.zoekdir()
        assert capsys.readouterr().out == (
                "called ComboBox.currentText\n"
                "called FileDialog.getExistingDirectory with args"
                f" {testobj} ('Choose a directory:', 'current text') {{}}\n")

        monkeypatch.setattr(testee.qtw.QFileDialog, 'getExistingDirectory', mock_get_dir)
        testobj.zoekdir()
        assert capsys.readouterr().out == (
                "called ComboBox.currentText\n"
                "called FileDialog.getExistingDirectory with args"
                f" {testobj} ('Choose a directory:', 'current text') {{}}\n"
                "called ComboBox.setEditText with arg `xyz`\n")
