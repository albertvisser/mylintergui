"""unittests for ./app/qtgui.py
"""
import pytest
from mockgui import mockqtwidgets as mockqtw
from app import qtgui as testee

o_filter = """\
called Dialog.__init__ with args {parent} () {{}}
called Dialog.setWindowTitle with args ('Title - configure',)
called Dialog.setWindowIcon with args ('app icon',)
called VBox.__init__
called Grid.__init__
called Label.__init__ with args ('Blacklist (do no lint):', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (1, 0, 1, 2)
called Label.__init__ with args ('Directory names:', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (2, 0)
called LineEdit.__init__
called LineEdit.setMinimumWidth with arg `200`
called LineEdit.setText with arg `xxx, yyy`
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'> at (2, 1)
called Label.__init__ with args ('File extensions:', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (3, 0)
called LineEdit.__init__
called LineEdit.setText with arg `a, b`
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'> at (3, 1)
called Label.__init__ with args ('File names:', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (4, 0)
called LineEdit.__init__
called LineEdit.setText with arg `f, g`
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'> at (4, 1)
called Label.__init__ with args ('', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (5, 0)
called Label.__init__ with args ('Whitelist (only lint):', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (6, 0, 1, 2)
called Label.__init__ with args ('File extensions:', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (7, 0)
called LineEdit.__init__
called LineEdit.setText with arg `aa, bb`
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'> at (7, 1)
called Label.__init__ with args ('Shebang lines:', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (8, 0)
called LineEdit.__init__
called LineEdit.setText with arg `#!x, #!y`
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'> at (8, 1)
called Label.__init__ with args ('', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (9, 0)
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockGridLayout'>
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Terug', {testobj}) {{}}
called Signal.connect with args ({testobj.reject},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Klaar', {testobj}) {{}}
called Signal.connect with args ({testobj.accept},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Dialog.setLayout
"""
o_quiet = """\
called Dialog.__init__ with args {parent} () {{}}
called Dialog.setWindowTitle with args ('Title - configure',)
called Dialog.setWindowIcon with args ('app icon',)
called VBox.__init__
called Label.__init__ with args ('Send output to:', {testobj})
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called HBox.__init__
called RadioButton.__init__ with args ('Single file:', {testobj}) {{}}
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockRadioButton'>
called LineEdit.__init__
called LineEdit.setMaximumWidth with arg `200`
called LineEdit.setMinimumWidth with arg `200`
called LineEdit.setText with arg `xxx`
"""
o_quiet_pt2 = """\
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'>
called PushButton.__init__ with args ('Select', {testobj}) {{}}
called Signal.connect with args ({testobj.browse},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called RadioButton.__init__ with args ('Multiple files like:', {testobj}) {{}}
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockRadioButton'>
called LineEdit.__init__
called LineEdit.setMaximumWidth with arg `300`
called LineEdit.setMinimumWidth with arg `300`
"""
o_quiet_pt3 = """\
called LineEdit.setText with arg `yyy`
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called HBox.addSpacing
called Label.__init__ with args ('<ignore> part of filename:', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called LineEdit.__init__
called LineEdit.setMaximumWidth with arg `200`
called LineEdit.setMinimumWidth with arg `200`
called LineEdit.setText with arg `zzz`
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Label.__init__ with args ("        <linter>: replace linter name in path\\n        <ignore>: part of source filename not to include in target name\\n        <filename>: (remainder of) source filename\\n        <date>: datetime.datetime.today().strftime('%Y%m%d%H%M%S')\\n        ", {testobj})
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Terug', {testobj}) {{}}
called Signal.connect with args ({testobj.reject},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Klaar', {testobj}) {{}}
called Signal.connect with args ({testobj.accept},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Dialog.setLayout
"""
o_quiet_multi = "called RadioButton.setChecked with arg `True`\n"
o_quiet_single = "called RadioButton.setChecked with arg `True`\n"
o_quiet_end = ("called RadioButton.setChecked with arg `True`\n"
               "called LineEdit.setText with arg `True`\n")
o_names = """\
called Dialog.__init__ with args {testobj.parent} () {{}}
called Dialog.setWindowTitle with args ('Title - file list',)
called Dialog.setWindowIcon with args ('app icon',)
called VBox.__init__
called Label.__init__ with args ('Selecteer de bestanden die je *niet* wilt verwerken', {testobj})
called HBox.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called CheckBox.__init__
called Signal.connect with args ({testobj.select_all},)
called HBox.__init__
called HBox.addSpacing
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called PushButton.__init__ with args ('Invert selection', {testobj}) {{}}
called Signal.connect with args ({testobj.invert_selection},)
called HBox.addStretch
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addSpacing
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Frame.__init__
called VBox.__init__
called CheckBox.__init__
called HBox.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called CheckBox.__init__
called HBox.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Frame.setLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>
called ScrollArea.__init__ with args ({testobj},)
called ScrollArea.setWidget with arg of type `<class 'mockgui.mockqtwidgets.MockFrame'>`
called HBox.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockScrollArea'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called PushButton.__init__ with args ('&Terug', {testobj}) {{}}
called Signal.connect with args ({testobj.reject},)
called PushButton.__init__ with args ('&Klaar', {testobj}) {{}}
called Signal.connect with args ({testobj.accept},)
called HBox.__init__
called HBox.addStretch
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Dialog.setLayout
"""


@pytest.fixture
def expected_output():
    """provide test output generated for methods that setup screens
    """
    return {'filteroptions': o_filter,
            'quietoptions': o_quiet + o_quiet_pt2 + o_quiet_pt3,
            'quietoptions2': o_quiet + o_quiet_single + o_quiet_pt2 + o_quiet_pt3 + o_quiet_end,
            'quietoptions3': o_quiet + o_quiet_pt2 + o_quiet_multi + o_quiet_pt3 + o_quiet_end,
            'selectnames': o_names, 'selectnames_2': o_names.replace('bestanden', 'directories')}


class MockBase:
    """stub for main.Base object
    """
    def __init__(self, *args, **kwargs):
        print('called Base.__init__ with args', args, kwargs)


class MockMainGui:
    """stub for qtgui.MainGui object
    """
    def __init__(self, *args, **kwargs):
        print('called MainGui.__init__ with args', args, kwargs)


def _test_waiting_cursor(monkeypatch, capsys):
    """unittest for qtgui.waiting_cursor
    """
    @testee.waiting_cursor
    def wrapped(arg):
        print('called wrapped function with arg', arg)
    assert testee.waiting_cursor(func) == "expected_result"
    assert capsys.readouterr().out == ("")


def test_show_dialog(monkeypatch, capsys):
    """unittest for qtgui.show_dialog
    """
    def mock_exec(cls):
        print('called Dialog.exec_')
        return True
    mockparent = 'parent'
    monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
    monkeypatch.setattr(testee.qtw.QDialog, 'exec_', mockqtw.MockDialog.exec_)
    cls = testee.qtw.QDialog
    assert not testee.show_dialog(cls, mockparent)
    assert capsys.readouterr().out == ("called Dialog.__init__ with args parent () {}\n"
                                       "called Dialog.exec_\n")
    monkeypatch.setattr(testee.qtw.QDialog, 'exec_', mock_exec)
    cls = testee.qtw.QDialog
    assert testee.show_dialog(cls, mockparent)
    assert capsys.readouterr().out == ("called Dialog.__init__ with args parent () {}\n"
                                       "called Dialog.exec_\n")


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
