"""unittests for ./app/qtgui.py
"""
import types
import pytest
from mockgui import mockqtwidgets as mockqtw
from app import qtgui as testee


class MockLinterApp:
    """stub for main.LinterApp object
    """
    def __init__(self, *args, **kwargs):
        print('called LinterApp.__init__ with args', args, kwargs)
    def get_output_filename(self, *args):
        "stub"
        print("called LinterApp.get_output_filename with args", args)
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


class MockLinterGui:
    """stub for qtgui.LinterGui object
    """
    def __init__(self, *args, **kwargs):
        "stub"
        print('called LinterGui.__init__ with args', args, kwargs)
    def execute_action(self):
        "stub"
        print('called LinterGui.execute_action')


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
    # wordt meegetest met LinterGui.execute_action


def test_show_dialog(monkeypatch, capsys):
    """unittest for qtgui.show_dialog
    """
    def mock_exec():
        print('called Dialog.exec')
        return 'Anything'
    def mock_exec_2():
        print('called Dialog.exec')
        return testee.qtw.QDialog.DialogCode.Accepted
    dialog = types.SimpleNamespace(exec=mock_exec)
    assert not testee.show_dialog(dialog)
    assert capsys.readouterr().out == "called Dialog.exec\n"
    dialog.exec = mock_exec_2
    assert testee.show_dialog(dialog)
    assert capsys.readouterr().out == "called Dialog.exec\n"


def test_show_message(monkeypatch, capsys):
    """unittest for qtgui.show_message
    """
    monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
    testee.show_message('parent', 'title', 'message')
    assert capsys.readouterr().out == (
            "called MessageBox.information with args `parent` `title` `message`\n")


# waar komt deze vandaan?
    def _test_wrap_operation(self, monkeypatch, capsys):
        """unittest for .wrap_operation
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.wrap_operation() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestLinterGui:
    """unittest for qtgui.LinterGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.LinterGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called LinterGui.__init__ with args', args)
        monkeypatch.setattr(testee.LinterGui, '__init__', mock_init)
        testobj = testee.LinterGui()
        testobj.app = mockqtw.MockApplication()
        testobj.master = MockLinterApp()
        assert capsys.readouterr().out == ("called LinterGui.__init__ with args ()\n"
                                           "called Application.__init__\n"
                                           "called LinterApp.__init__ with args () {}\n")
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for LinterGui.__init__
        """
        monkeypatch.setattr(testee.qtw.QApplication, '__init__', mockqtw.MockApplication.__init__)
        monkeypatch.setattr(testee.qtw.QWidget, '__init__', mockqtw.MockWidget.__init__)
        monkeypatch.setattr(testee.qtw.QWidget, 'setWindowTitle', mockqtw.MockWidget.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QWidget, 'setWindowIcon', mockqtw.MockWidget.setWindowIcon)
        monkeypatch.setattr(testee.gui.QIcon, '__init__', mockqtw.MockIcon.__init__)
        master = MockLinterApp()
        master.title = 'A title'
        master.iconame = 'icon name'
        testobj = testee.LinterGui(master)
        assert testobj.master == master
        assert isinstance(testobj.appicon, testee.gui.QIcon)
        assert capsys.readouterr().out == ("called LinterApp.__init__ with args () {}\n"
                                           "called Application.__init__\n"
                                           "called Widget.__init__\n"
                                           "called Widget.setWindowTitle with arg `A title`\n"
                                           "called Icon.__init__ with arg `icon name`\n"
                                           "called Widget.setWindowIcon\n")

    def test_start_display(self, monkeypatch, capsys):
        """unittest for LinterGui.start_display
        """
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.start_display()
        assert isinstance(testobj.grid, testee.qtw.QGridLayout)
        assert testobj.row == -1
        assert capsys.readouterr().out == "called Grid.__init__\n"

    def test_build_radiobutton_row(self, monkeypatch, capsys):
        """unittest for LinterGui.build_radiobutton_row
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QButtonGroup', mockqtw.MockButtonGroup)
        monkeypatch.setattr(testee.qtw, 'QRadioButton', mockqtw.MockRadioButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockqtw.MockGridLayout()
        testobj.row = 0
        result = testobj.build_radiobutton_row('title', [('xx', False), ('yy', True)])
        assert testobj.row == 1
        assert isinstance(result, testee.qtw.QButtonGroup)
        assert capsys.readouterr().out == (
                "called Grid.__init__\n"
                f"called Label.__init__ with args ('title', {testobj})\n"
                "called Grid.addWidget with arg MockLabel at (1, 0)\n"
                "called ButtonGroup.__init__ with args ()\n"
                "called HBox.__init__\n"
                f"called RadioButton.__init__ with args ('xx', {testobj}) {{}}\n"
                "called ButtonGroup.addButton with arg MockRadioButton\n"
                "called HBox.addWidget with arg MockRadioButton\n"
                f"called RadioButton.__init__ with args ('yy', {testobj}) {{}}\n"
                "called ButtonGroup.addButton with arg MockRadioButton\n"
                "called HBox.addWidget with arg MockRadioButton\n"
                "called RadioButton.setChecked with arg `True`\n"
                "called Grid.addLayout with arg MockHBoxLayout at (1, 1, 1, 2)\n")

    def test_build_radiobutton_block(self, monkeypatch, capsys):
        """unittest for LinterGui.build_radiobutton_block
        """
        def mock_configure():
            "dummy callback"
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QButtonGroup', mockqtw.MockButtonGroup)
        monkeypatch.setattr(testee.qtw, 'QRadioButton', mockqtw.MockRadioButton)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockqtw.MockGridLayout()
        testobj.master = types.SimpleNamespace(configure_linter=mock_configure)
        testobj.row = 0
        result = testobj.build_radiobutton_block('title', [('xx', False), ('yy', True)])
        assert testobj.row == 3
        assert isinstance(result, testee.qtw.QButtonGroup)
        assert capsys.readouterr().out == (
                "called Grid.__init__\n"
                f"called Label.__init__ with args ('title', {testobj})\n"
                "called Grid.addWidget with arg MockLabel at (1, 0)\n"
                "called ButtonGroup.__init__ with args ()\n"
                "called HBox.__init__\n"
                f"called RadioButton.__init__ with args ('Xx', {testobj}) {{}}\n"
                "called ButtonGroup.addButton with arg MockRadioButton\n"
                "called HBox.addWidget with arg MockRadioButton\n"
                f"called PushButton.__init__ with args ('Configure', {testobj}) {{}}\n"
                f"called Signal.connect with args ({testobj.master.configure_linter},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called Grid.addLayout with arg MockHBoxLayout at (1, 1)\n"
                "called HBox.__init__\n"
                f"called RadioButton.__init__ with args ('Yy', {testobj}) {{}}\n"
                "called ButtonGroup.addButton with arg MockRadioButton\n"
                "called HBox.addWidget with arg MockRadioButton\n"
                "called RadioButton.setChecked with arg `True`\n"
                f"called PushButton.__init__ with args ('Configure', {testobj}) {{}}\n"
                f"called Signal.connect with args ({testobj.master.configure_linter},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called Grid.addLayout with arg MockHBoxLayout at (2, 1)\n")

    def test_add_combobox_row(self, monkeypatch, capsys):
        """unittest for LinterGui.add_combobox_row
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(mockqtw.MockComboBox, 'editTextChanged', {str: mockqtw.MockSignal()})
        assert capsys.readouterr().out == "called Signal.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockqtw.MockGridLayout()
        button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called Grid.__init__\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.row = 1
        result = testobj.add_combobox_row('label text', ['item', 'list'])
        assert isinstance(result, testee.qtw.QComboBox)
        assert testobj.row == 2
        assert capsys.readouterr().out == (
            "called Label.__init__ with args ('label text',)\n"
            f"called Grid.addWidget with arg MockLabel at ({testobj.row}, 0)\n"
            "called ComboBox.__init__\n"
            "called ComboBox.insertItems with args (0, ['item', 'list'])\n"
            "called ComboBox.setEditable with arg `True`\n"
            "called ComboBox.clearEditText\n"
            "called ComboBox.setCompleter with arg None\n"
            f"called Grid.addWidget with arg MockComboBox at ({testobj.row}, 1)\n")
        result = testobj.add_combobox_row('label text', ['item', 'list'], 'start', 100, 'callback',
                                          ['button', 'callback'])
        assert isinstance(result, testee.qtw.QComboBox)
        assert testobj.row == 3
        assert capsys.readouterr().out == (
            "called Label.__init__ with args ('label text',)\n"
            f"called Grid.addWidget with arg MockLabel at ({testobj.row}, 0)\n"
            "called ComboBox.__init__\n"
            "called ComboBox.setMaximumWidth with arg `100`\n"
            "called ComboBox.setMinimumWidth with arg `100`\n"
            "called ComboBox.insertItems with args (0, ['item', 'list'])\n"
            "called ComboBox.setEditable with arg `True`\n"
            "called ComboBox.clearEditText\n"
            "called ComboBox.setEditText with arg `start`\n"
            "called ComboBox.setCompleter with arg None\n"
            "called Signal.connect with args ('callback',)\n"
            "called HBox.__init__\n"
            "called PushButton.__init__ with args ('button',) {}\n"
            "called Signal.connect with args ('callback',)\n"
            "called HBox.addWidget with arg MockComboBox\n"
            "called HBox.addWidget with arg MockPushButton\n"
            "called HBox.addStretch\n"
            f"called Grid.addLayout with arg MockHBoxLayout at ({testobj.row}, 1)\n")

    def test_show_single_mode_info(self, monkeypatch, capsys):
        """unittest for LinterGui.show_single_mode_info
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.row = 0
        testobj.show_single_mode_info('locationtext', 'filename')
        assert testobj.row == 1
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('locationtext', {testobj})\n"
                "called Grid.addWidget with arg MockLabel at (1, 0)\n"
                "called HBox.__init__\n"
                f"called Label.__init__ with args ('filename', {testobj})\n"
                "called HBox.addWidget with arg MockLabel\n"
                "called Grid.addLayout with arg MockHBoxLayout at (1, 1, 1, 2)\n")

    def test_show_multi_mode_info(self, monkeypatch, capsys):
        """unittest for LinterGui.show_multi_mode_info
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QListWidget', mockqtw.MockListBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.row = 0
        testobj.show_multi_mode_info('locationtext', ['file', 'dir', 'file2'])
        assert testobj.row == 1
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('locationtext', {testobj})\n"
                "called Grid.addWidget with arg MockLabel at (1, 0, 1, 3)\n"
                "called List.__init__\n"
                "called List.insertItems with args (0, ['file', 'dir', 'file2'])\n"
                "called Grid.addWidget with arg MockListBox at (1, 0, 1, 3)\n")

    def test_add_checkbox_line(self, monkeypatch, capsys):
        """unittest for LinterGui.add_checkbox_line
        """
        def callback():
            "empty function needed for reference"
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QSpinBox', mockqtw.MockSpinBox)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.row = 1
        result = testobj.add_checkbox_line('text')
        assert isinstance(result[0], testee.qtw.QCheckBox)
        assert result[1] is None
        assert testobj.row == 2
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ('text', {testobj})\n"
                "called Grid.addWidget with arg MockCheckBox at (2, 1)\n")
        testobj.row = 1
        result = testobj.add_checkbox_line('text', True, (1, 2), ('btn', callback))
        assert isinstance(result[0], testee.qtw.QCheckBox)
        assert isinstance(result[1], testee.qtw.QSpinBox)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                f"called CheckBox.__init__ with args ('text', {testobj})\n"
                "called CheckBox.toggle\n"
                "called HBox.addWidget with arg MockCheckBox\n"
                "called SpinBox.__init__\n"
                "called SpinBox.setMinimum with arg '1'\n"
                "called SpinBox.setValue with arg '2'\n"
                "called HBox.addWidget with arg MockSpinBox\n"
                f"called PushButton.__init__ with args ('btn', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called Grid.addLayout with arg MockHBoxLayout at (2, 1)\n")

    def test_add_buttons(self, monkeypatch, capsys):
        """unittest for LinterGui.add_buttons
        """
        def callback1():
            "empty function needed for reference"
        def callback2():
            "empty function needed for reference"
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.row = 0
        testobj.add_buttons([('xx', callback1), ('yy', callback2)])
        assert testobj.row == 1
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                f"called PushButton.__init__ with args ('xx', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback1},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                f"called PushButton.__init__ with args ('yy', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback2},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called Grid.addLayout with arg MockHBoxLayout at (1, 0, 1, 2)\n")

    def test_finalize_display(self, monkeypatch, capsys):
        """unittest for LinterGui.finalize_display
        """
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw.QWidget, 'setLayout', mockqtw.MockWidget.setLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        buttongroup = mockqtw.MockButtonGroup()
        buttongroup.addButton(mockqtw.MockPushButton('xxx'))
        testobj.grid = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == ("called ButtonGroup.__init__ with args ()\n"
                                           "called PushButton.__init__ with args ('xxx',) {}\n"
                                           "called ButtonGroup.addButton with arg MockPushButton\n"
                                           "called Grid.__init__\n")
        testobj.finalize_display(buttongroup)
        assert capsys.readouterr().out == ("called VBox.__init__\n"
                                           "called VBox.addLayout with arg MockGridLayout\n"
                                           "called Widget.setLayout with arg MockVBoxLayout\n"
                                           "called ButtonGroup.buttons\n"
                                           "called PushButton.setFocus\n")

    def test_go(self, monkeypatch, capsys):
        """unittest for LinterGui.go
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.app = mockqtw.MockApplication()
        assert capsys.readouterr().out == "called Application.__init__\n"
        with pytest.raises(SystemExit):
            testobj.go()
        assert capsys.readouterr().out == ("called Application.exec\n")

    def test_keyPressEvent(self, monkeypatch, capsys):
        """unittest for LinterGui.keyPressEvent
        """
        def mock_close():
            print('called LinterGui.close')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.close = mock_close
        event = types.SimpleNamespace(key=lambda: 'anything')
        testobj.keyPressEvent(event)
        assert capsys.readouterr().out == ""
        event = types.SimpleNamespace(key=lambda: testee.core.Qt.Key.Key_Escape)
        testobj.keyPressEvent(event)
        assert capsys.readouterr().out == "called LinterGui.close\n"

    def test_get_radiogroup_checked(self, monkeypatch, capsys):
        """unittest for LinterGui.get_radiogroup_checked
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
        assert capsys.readouterr().out == ("called ButtonGroup.checkedButton\n"
                                           "called RadioButton.text\n")

    def test_meld_fout(self, monkeypatch, capsys):
        """unittest for LinterGui.meld_fout
        """
        monkeypatch.setattr(testee.qtw.QMessageBox, 'critical', mockqtw.MockMessageBox.critical)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.fouttitel = 'xxx'
        testobj.meld_fout('message')
        assert capsys.readouterr().out == (
                f"called MessageBox.critical with args `{testobj}` `xxx` `message`\n")

    def test_meld_info(self, monkeypatch, capsys):
        """unittest for LinterGui.meld_info
        """
        monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mockqtw.MockMessageBox.information)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.resulttitel = 'xxx'
        testobj.meld_info('message')
        assert capsys.readouterr().out == (
                f"called MessageBox.information with args `{testobj}` `xxx` `message`\n")

    def test_get_combobox_textvalue(self, monkeypatch, capsys):
        """unittest for LinterGui.get_combobox_textvalue
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        widget = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        assert testobj.get_combobox_textvalue(widget) == "current text"
        assert capsys.readouterr().out == ("called ComboBox.currentText\n")

    def test_set_checkbox_value(self, monkeypatch, capsys):
        """unittest for LinterGui.set_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        widget = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        testobj.set_checkbox_value(widget, True)
        assert capsys.readouterr().out == "called CheckBox.setChecked with arg True\n"

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for LinterGui.get_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        widget = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        assert not testobj.get_checkbox_value(widget)
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n")

    def test_get_spinbox_value(self, monkeypatch, capsys):
        """unittest for LinterGui.get_spinbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        widget = mockqtw.MockSpinBox()
        assert capsys.readouterr().out == "called SpinBox.__init__\n"
        assert testobj.get_spinbox_value(widget) == 0
        assert capsys.readouterr().out == ("called SpinBox.value\n")

    def test_execute_action(self, monkeypatch, capsys):
        """unittest for LinterGui.execute_action
        """
        monkeypatch.setattr(testee.gui, 'QCursor', mockqtw.MockCursor)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.app = mockqtw.MockApplication()
        assert capsys.readouterr().out == "called Application.__init__\n"
        testobj.master.do_checks = MockFinder()
        testobj.execute_action()
        assert capsys.readouterr().out == (
                f"called Cursor.__init__ with arg {testee.core.Qt.CursorShape.WaitCursor}\n"
                "called Application.setOverrideCursor with arg MockCursor\n"
                "called Finder.do_action\n"
                "called Application.restoreOverrideCursor\n")

    def test_zoekdir(self, monkeypatch, capsys):
        """unittest for LinterGui.zoekdir
        """
        def mock_get_dir(parent, *args, **kwargs):
            print('called FileDialog.getExistingDirectory with args', parent, args, kwargs)
            return 'xyz'
        monkeypatch.setattr(testee.qtw, 'QFileDialog', mockqtw.MockFileDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(vraag_dir=mockqtw.MockComboBox())
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


class TestFilterOptionsGui:
    """unittests for qtgui.FilterOptionsGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.FilterOptionsGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called FilterOptionsGui.__init__ with args', args)
        monkeypatch.setattr(testee.FilterOptionsGui, '__init__', mock_init)
        testobj = testee.FilterOptionsGui()
        assert capsys.readouterr().out == 'called FilterOptionsGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for FilterOptionsGui.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        master = 'master'
        parent = types.SimpleNamespace(appicon='icon')
        testobj = testee.FilterOptionsGui('master', parent, 'title')
        assert testobj.master == 'master'
        assert isinstance(testobj.vbox, testee.qtw.QVBoxLayout)
        assert isinstance(testobj.gbox, testee.qtw.QGridLayout)
        assert testobj.row == 0
        assert capsys.readouterr().out == (f"called Dialog.__init__ with args {parent} () {{}}\n"
                                           "called Dialog.setWindowTitle with args ('title',)\n"
                                           "called Dialog.setWindowIcon with args ('icon',)\n"
                                           "called VBox.__init__\n"
                                           "called Grid.__init__\n"
                                           "called VBox.addLayout with arg MockGridLayout\n"
                                           "called Dialog.setLayout with arg MockVBoxLayout\n")

    def test_add_title_line(self, monkeypatch, capsys):
        """unittest for FilterOptionsGui.add_title_line
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gbox = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.row = 0
        testobj.add_title_line('text')
        assert testobj.row == 1
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('text', {testobj})\n"
                "called Grid.addWidget with arg MockLabel at (1, 0, 1, 2)\n")

    def test_add_textentry_line(self, monkeypatch, capsys):
        """unittest for FilterOptionsGui.add_textentry_line
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gbox = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.row = 0
        result = testobj.add_textentry_line('caption', 'initialtext')
        assert testobj.row == 1
        assert isinstance(result, testee.qtw.QLineEdit)
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('caption', {testobj})\n"
                "called Grid.addWidget with arg MockLabel at (1, 0)\n"
                "called LineEdit.__init__\n"
                "called LineEdit.setText with arg `initialtext`\n"
                "called Grid.addWidget with arg MockLineEdit at (1, 1)\n")
        testobj.row = 0
        result = testobj.add_textentry_line('caption', 'initialtext', 50)
        assert testobj.row == 1
        assert isinstance(result, testee.qtw.QLineEdit)
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('caption', {testobj})\n"
                "called Grid.addWidget with arg MockLabel at (1, 0)\n"
                "called LineEdit.__init__\n"
                "called LineEdit.setMinimumWidth with arg `50`\n"
                "called LineEdit.setText with arg `initialtext`\n"
                "called Grid.addWidget with arg MockLineEdit at (1, 1)\n")

    def test_add_buttons(self, monkeypatch, capsys):
        """unittest for FilterOptionsGui.add_buttons
        """
        def callback1():
            "empty function for reference"
        def callback2():
            "empty function for reference"
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_buttons([('xxx', callback1), ('yyy', callback2)])
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                f"called PushButton.__init__ with args ('xxx', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback1},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                f"called PushButton.__init__ with args ('yyy', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback2},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for FilterOptionsGui.accept
        """
        def mock_confirm():
            print('called FilterOptions.confirm')
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.accept()
        assert capsys.readouterr().out == ("called FilterOptions.confirm\n"
                                           "called Dialog.accept\n")

    def test_get_textentry_value(self, monkeypatch, capsys):
        """unittest for FilterOptionsGui.get_textentry_value
        """
        textfield = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textentry_value(textfield) == ""
        assert capsys.readouterr().out == ("called LineEdit.text\n")


class TestQuietOptionsGui:
    """unittests for qtgui.QuietOptionsGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.QuietOptionsGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called QuietOptionsGui.__init__ with args', args)
        monkeypatch.setattr(testee.QuietOptionsGui, '__init__', mock_init)
        testobj = testee.QuietOptionsGui()
        assert capsys.readouterr().out == 'called QuietOptionsGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for QuietOptionsGui.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        master = 'master'
        parent = types.SimpleNamespace(appicon='icon')
        testobj = testee.QuietOptionsGui('master', parent, 'title')
        assert testobj.parent == parent
        assert isinstance(testobj.vbox, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == (f"called Dialog.__init__ with args {parent} () {{}}\n"
                                           "called Dialog.setWindowTitle with args ('title',)\n"
                                           "called Dialog.setWindowIcon with args ('icon',)\n"
                                           "called VBox.__init__\n"
                                           "called Dialog.setLayout with arg MockVBoxLayout\n")

    def test_start_line(self, monkeypatch, capsys):
        """unittest for QuietOptionsGui.start_line
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert isinstance(testobj.start_line(), testee.qtw.QHBoxLayout)
        assert capsys.readouterr().out == ("called HBox.__init__\n")

    def test_add_text_to_line(self, monkeypatch, capsys):
        """unittest for QuietOptionsGui.add_text_to_line
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        line = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called HBox.__init__\n"
        testobj.add_text_to_line(line, 'text')
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('text', {testobj})\n"
                "called HBox.addWidget with arg MockLabel\n")
        testobj.add_text_to_line(line, 'text', 5)
        assert capsys.readouterr().out == (
                "called HBox.addSpacing\n"
                f"called Label.__init__ with args ('text', {testobj})\n"
                "called HBox.addWidget with arg MockLabel\n")

    def test_add_radiobutton_to_line(self, monkeypatch, capsys):
        """unittest for QuietOptionsGui.add_radiobutton_to_line
        """
        monkeypatch.setattr(testee.qtw, 'QRadioButton', mockqtw.MockRadioButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        line = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called HBox.__init__\n"
        result = testobj.add_radiobutton_to_line(line, 'text', False)
        assert isinstance(result, testee.qtw.QRadioButton)
        assert capsys.readouterr().out == (
                f"called RadioButton.__init__ with args ('text', {testobj}) {{}}\n"
                "called HBox.addWidget with arg MockRadioButton\n")
        result = testobj.add_radiobutton_to_line(line, 'text', True)
        assert isinstance(result, testee.qtw.QRadioButton)
        assert capsys.readouterr().out == (
                f"called RadioButton.__init__ with args ('text', {testobj}) {{}}\n"
                "called HBox.addWidget with arg MockRadioButton\n"
                "called RadioButton.setChecked with arg `True`\n")

    def test_add_textentry_to_line(self, monkeypatch, capsys):
        """unittest for QuietOptionsGui.add_textentry_to_line
        """
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        testobj = self.setup_testobj(monkeypatch, capsys)
        line = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called HBox.__init__\n"
        result = testobj.add_textentry_to_line(line, 'initialtext')
        assert isinstance(result, testee.qtw.QLineEdit)
        assert capsys.readouterr().out == ("called LineEdit.__init__\n"
                                           "called LineEdit.setText with arg `initialtext`\n"
                                           "called HBox.addWidget with arg MockLineEdit\n")
        result = testobj.add_textentry_to_line(line, 'initialtext', width=10)
        assert isinstance(result, testee.qtw.QLineEdit)
        assert capsys.readouterr().out == ("called LineEdit.__init__\n"
                                           "called LineEdit.setMaximumWidth with arg `10`\n"
                                           "called LineEdit.setMinimumWidth with arg `10`\n"
                                           "called LineEdit.setText with arg `initialtext`\n"
                                           "called HBox.addWidget with arg MockLineEdit\n")

    def test_add_button_to_line(self, monkeypatch, capsys):
        """unittest for QuietOptionsGui.add_button_to_line
        """
        def callback():
            "dummy function for reference"
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        line = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called HBox.__init__\n"
        testobj.add_button_to_line(line, 'text', callback)
        assert capsys.readouterr().out == (
                f"called PushButton.__init__ with args ('text', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback},)\n"
                "called HBox.addWidget with arg MockPushButton\n")

    def test_end_line(self, monkeypatch, capsys):
        """unittest for QuietOptionsGui.end_line
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        line = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\ncalled HBox.__init__\n"
        testobj.end_line(line)
        assert capsys.readouterr().out == ("called HBox.addStretch\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_buttons(self, monkeypatch, capsys):
        """unittest for QuietOptionsGui.add_buttons
        """
        def callback1():
            "dummy function for reference"
        def callback2():
            "dummy function for reference"
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_buttons([('xx', callback1), ('yy', callback2)])
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                f"called PushButton.__init__ with args ('xx', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback1},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                f"called PushButton.__init__ with args ('yy', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback2},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def _test_browse(self, monkeypatch, capsys):
        """unittest for QuietOptionsGui.browse
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.browse() == "expected_result"
        assert capsys.readouterr().out == ("")
        # is nog TODO, dus nog geen testmethode

    def test_accept(self, monkeypatch, capsys):
        """unittest for QuietOptionsGui.accept
        """
        def mock_confirm():
            print('called FilterOptions.confirm')
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.accept()
        assert capsys.readouterr().out == ("called FilterOptions.confirm\n"
                                           "called Dialog.accept\n")

    def test_set_radiobutton_value(self, monkeypatch, capsys):
        """unittest for QuietOptionsGui.set_radiobutton_value
        """
        rb = mockqtw.MockRadioButton()
        assert capsys.readouterr().out == "called RadioButton.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_radiobutton_value(rb, 'value')
        assert capsys.readouterr().out == "called RadioButton.setChecked with arg `value`\n"

    def test_get_radiobutton_value(self, monkeypatch, capsys):
        """unittest for QuietOptionsGui.get_radiobutton_value
        """
        rb = mockqtw.MockRadioButton()
        assert capsys.readouterr().out == "called RadioButton.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert not testobj.get_radiobutton_value(rb)
        assert capsys.readouterr().out == "called RadioButton.isChecked\n"

    def test_set_textentry_value(self, monkeypatch, capsys):
        """unittest for QuietOptionsGui.set_textentry_value
        """
        textfield = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_textentry_value(textfield, 'value')
        assert capsys.readouterr().out == "called LineEdit.setText with arg `value`\n"

    def test_get_textentry_value(self, monkeypatch, capsys):
        """unittest for QuietOptionsGui.get_textentry_value
        """
        textfield = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textentry_value(textfield) == ""
        assert capsys.readouterr().out == "called LineEdit.text\n"


class TestSelectNamesGui:
    """unittests for qtgui.SelectNamesGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.SelectNamesGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SelectNamesGui.__init__ with args', args)
        monkeypatch.setattr(testee.SelectNamesGui, '__init__', mock_init)
        testobj = testee.SelectNamesGui()
        assert capsys.readouterr().out == 'called SelectNamesGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for SelectNamesGui.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        master = 'master'
        parent = types.SimpleNamespace(appicon='icon')
        testobj = testee.SelectNamesGui('master', parent, 'title')
        assert testobj.parent == parent
        assert isinstance(testobj.vbox, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == (f"called Dialog.__init__ with args {parent} () {{}}\n"
                                           "called Dialog.setWindowTitle with args ('title',)\n"
                                           "called Dialog.setWindowIcon with args ('icon',)\n"
                                           "called VBox.__init__\n"
                                           "called Dialog.setLayout with arg MockVBoxLayout\n")

    def test_start_line(self, monkeypatch, capsys):
        """unittest for SelectNamesGui.start_line
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        assert isinstance(testobj.start_line(), testee.qtw.QHBoxLayout)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_text_to_line(self, monkeypatch, capsys):
        """unittest for SelectNamesGui.add_text_line
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        line = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called HBox.__init__\n"
        testobj.add_text_to_line(line, 'text')
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('text', {testobj})\n"
                "called HBox.addWidget with arg MockLabel\n")

    def test_add_checkbox_to_line(self, monkeypatch, capsys):
        """unittest for SelectNamesGui.add_checkbox_to_line
        """
        def callback():
            "dummy function for reference"
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        line = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called HBox.__init__\n"
        result = testobj.add_checkbox_to_line(line, 'text', callback)
        assert isinstance(result, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ('text', {testobj})\n"
                f"called Signal.connect with args ({callback},)\n"
                "called HBox.addWidget with arg MockCheckBox\n")
        result = testobj.add_checkbox_to_line(line, 'text', callback, before=10)
        assert isinstance(result, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ('text', {testobj})\n"
                f"called Signal.connect with args ({callback},)\n"
                "called HBox.addSpacing\n"
                "called HBox.addWidget with arg MockCheckBox\n")

    def test_add_button_to_line(self, monkeypatch, capsys):
        """unittest for SelectNamesGui.add_button_to_line
        """
        def callback():
            "dummy function for reference"
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        line = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called HBox.__init__\n"
        testobj.add_button_to_line(line, 'text', callback)
        assert capsys.readouterr().out == (
                f"called PushButton.__init__ with args ('text', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback},)\n"
                "called HBox.addWidget with arg MockPushButton\n")
        testobj.add_button_to_line(line, 'text', callback, before=10)
        assert capsys.readouterr().out == (
                f"called PushButton.__init__ with args ('text', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback},)\n"
                "called HBox.addSpacing\n"
                "called HBox.addWidget with arg MockPushButton\n")

    def test_create_checkbox_list(self, monkeypatch, capsys):
        """unittest for SelectNamesGui.create_checkbox_list
        """
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QScrollArea', mockqtw.MockScrollArea)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.create_checkbox_list(['xx', 'yy'])
        for item in result:
            assert isinstance(item, testee.qtw.QCheckBox)
        assert isinstance(testobj.frm, testee.qtw.QFrame)
        assert capsys.readouterr().out == (
                "called Frame.__init__\n"
                "called VBox.__init__\n"
                f"called CheckBox.__init__ with args ('xx', {testobj.frm})\n"
                "called HBox.__init__\n"
                "called HBox.addWidget with arg MockCheckBox\n"
                "called VBox.addLayout with arg MockHBoxLayout\n"
                f"called CheckBox.__init__ with args ('yy', {testobj.frm})\n"
                "called HBox.__init__\n"
                "called HBox.addWidget with arg MockCheckBox\n"
                "called VBox.addLayout with arg MockHBoxLayout\n"
                "called Frame.setLayout with arg MockVBoxLayout\n"
                f"called ScrollArea.__init__ with args ({testobj},)\n"
                "called ScrollArea.setWidget with arg `MockFrame`\n"
                "called HBox.__init__\n"
                "called HBox.addWidget with arg MockScrollArea\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_create_button_bar(self, monkeypatch, capsys):
        """unittest for SelectNamesGui.create_button_bar
        """
        def callback1():
            "dummy function for reference"
        def callback2():
            "dummy function for reference"
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.create_button_bar([('xx', callback1), ('yy', callback2)])
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                f"called PushButton.__init__ with args ('xx', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback1},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                f"called PushButton.__init__ with args ('yy', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback2},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_get_checkbox_text(self, monkeypatch, capsys):
        """unittest for SelectNamesGui.get_checkbox_text
        """
        cb = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert not testobj.get_checkbox_text(cb)
        assert capsys.readouterr().out == "called CheckBox.text\n"

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for SelectNamesGui.get_checkbox_value
        """
        cb = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert not testobj.get_checkbox_value(cb)
        assert capsys.readouterr().out == "called CheckBox.isChecked\n"

    def test_set_checkbox_value(self, monkeypatch, capsys):
        """unittest for SelectNamesGui.set_checkbox_value
        """
        cb = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_checkbox_value(cb, 'value')
        assert capsys.readouterr().out == "called CheckBox.setChecked with arg value\n"

    def test_accept(self, monkeypatch, capsys):
        """unittest for SelectNamesGui.accept
        """
        def mock_confirm():
            print('called FilterOptions.confirm')
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.accept()
        assert capsys.readouterr().out == ("called FilterOptions.confirm\n"
                                           "called Dialog.accept\n")


class TestResultsGui:
    """unittests for qtgui.ResultsGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.ResultsGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ResultsGui.__init__ with args', args)
        monkeypatch.setattr(testee.ResultsGui, '__init__', mock_init)
        testobj = testee.ResultsGui()
        assert capsys.readouterr().out == 'called ResultsGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for ResultsGui.__init__
        """
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mockqtw.MockDialog.setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw.QDialog, 'resize', mockqtw.MockDialog.resize)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        master = 'master'
        parent = types.SimpleNamespace(appicon='icon')
        testobj = testee.ResultsGui('master', parent, 'title', 26)
        assert isinstance(testobj.vbox, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == (f"called Dialog.__init__ with args {parent} () {{}}\n"
                                           "called Dialog.setWindowTitle with args ('title',)\n"
                                           "called Dialog.setWindowIcon with args ('icon',)\n"
                                           "called VBox.__init__\n"
                                           "called Dialog.setLayout with arg MockVBoxLayout\n"
                                           "called Dialog.resize with args (600, 480)\n")

    def test_add_top_text(self, monkeypatch, capsys):
        """unittest for ResultsGui.add_top_text
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_top_text('text')
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           f"called Label.__init__ with args ('text', {testobj})\n"
                                           "called HBox.addWidget with arg MockLabel\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_combobox_line(self, monkeypatch, capsys):
        """unittest for ResultsGui.add_combobox_line
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(populate_list=lambda: 'dummy')
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.add_combobox_line('text', ['it', 'ems'])
        assert isinstance(result[0], testee.qtw.QHBoxLayout)
        assert isinstance(result[1], testee.qtw.QComboBox)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called VBox.addLayout with arg MockHBoxLayout\n"
                f"called Label.__init__ with args ('text', {testobj})\n"
                "called HBox.addWidget with arg MockLabel\n"
                "called ComboBox.__init__\n"
                "called ComboBox.addItems with arg ['it', 'ems']\n"
                "called ComboBox.setEditable with arg `False`\n"
                f"called Signal.connect with args ({testobj.master.populate_list},)\n"
                "called HBox.addWidget with arg MockComboBox\n"
                "called HBox.addStretch\n")

    def test_add_button_to_line(self, monkeypatch, capsys):
        """unittest for ResultsGui.add_button_to_line
        """
        def callback():
            "dummy function"
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        hbox = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called HBox.__init__\n"
        testobj.add_button_to_line(hbox, 'text', callback)
        assert capsys.readouterr().out == (
                f"called PushButton.__init__ with args ('text', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback},)\n"
                "called HBox.addWidget with arg MockPushButton\n")

    def test_add_results_list(self, monkeypatch, capsys):
        """unittest for ResultsGui.add_results_list
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.gui, 'QFont', mockqtw.MockFont)
        monkeypatch.setattr(testee.qtw, 'QTextEdit', mockqtw.MockEditorWidget)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        assert isinstance(testobj.add_results_list(), testee.qtw.QTextEdit)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           f"called Editor.__init__ with args ({testobj},)\n"
                                           "called Font.__init__\n"
                                           "called Font.setFamily\n"
                                           "called Font.setFixedPitch with arg `True`\n"
                                           "called Font.setPointSize\n"
                                           "called Editor.setCurrentFont\n"
                                           "called Editor.setReadOnly with arg `True`\n"
                                           "called HBox.addWidget with arg MockEditorWidget\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_buttons(self, monkeypatch, capsys):
        """unittest for ResultsGui.add_buttons
        """
        def callback1():
            "dummy function"
        def callback2():
            "dummy function"
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_buttons([('xx', callback1), ('yy', callback2)])
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                f"called PushButton.__init__ with args ('xx', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback1},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                f"called PushButton.__init__ with args ('yy', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback2},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_get_combobox_value(self, monkeypatch, capsys):
        """unittest for ResultsGui.get_combobox_value
        """
        cmb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_combobox_value(cmb) == "current text"
        assert capsys.readouterr().out == "called ComboBox.currentText\n"

    def test_set_combobox_value(self, monkeypatch, capsys):
        """unittest for ResultsGui.set_combobox_value
        """
        cmb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_combobox_value(cmb, 'value')
        assert capsys.readouterr().out == ("called ComboBox.setCurrentIndex with arg `value`\n")

    def test_set_textbox_value(self, monkeypatch, capsys):
        """unittest for ResultsGui.set_textbox_value
        """
        textbox = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == "called Editor.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_textbox_value(textbox, '')
        assert capsys.readouterr().out == "called Editor.clear\n"
        testobj.set_textbox_value(textbox, 'text')
        assert capsys.readouterr().out == ("called Editor.clear\n"
                                           "called Editor.setText with arg `text`\n")

    def test_klaar(self, monkeypatch, capsys):
        """unittest for ResultsGui.klaar
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'done', mockqtw.MockDialog.done)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.klaar()
        assert capsys.readouterr().out == "called Dialog.done with arg `0`\n"

    def test_copy_to_clipboard(self, monkeypatch, capsys):
        """unittest for ResultsGui.copy_to_clipboard
        """
        monkeypatch.setattr(testee.qtw, 'QApplication', mockqtw.MockApplication)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.copy_to_clipboard('data')
        assert capsys.readouterr().out == ("called Application.clipboard\n"
                                           "called ClipBoard.__init__\n"
                                           "called Clipboard.setText with arg 'data'\n")
