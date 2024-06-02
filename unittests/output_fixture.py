import pytest

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
o_results_start = """\
called Dialog.__init__ with args {testobj.parent} () {{}}
called Dialog.setWindowTitle with args ('Title',)
called Dialog.setWindowIcon with args ('app icon',)
called VBox.__init__
called HBox.__init__
called Label.__init__ with args ('rpttitel (3 items)"""
o_results_end = """', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called Label.__init__ with args ('Files checked:', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called ComboBox.__init__
called ComboBox.addItems with arg ['xxx', 'yyy']
called ComboBox.setEditable with arg `False`
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockComboBox'>
called HBox.addStretch
called PushButton.__init__ with args ('&Go To File', {testobj}) {{}}
called Signal.connect with args ({testobj.goto_result},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called Editor.__init__ with args ({testobj},)
called Font.__init__
called Font.setFamily
called Font.setFixedPitch
called Font.setPointSize
called Editor.setCurrentFont
called Editor.setReadOnly with arg `True`
called ComboBox.currentText
called Editor.setText with arg `abcd`
called Signal.connect with args ({testobj.populate_list},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockEditorWidget'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Klaar', {testobj}) {{}}
called Signal.connect with args ({testobj.klaar},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Repeat Action', {testobj}) {{}}
called Signal.connect with args ({testobj.refresh},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('Copy to &File(s)', {testobj}) {{}}
called Signal.connect with args ({testobj.kopie},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('Copy to &Clipboard', {testobj}) {{}}
called Signal.connect with args ({testobj.to_clipboard},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Dialog.setLayout
called Widget.resize with args (724, 480)
called Dialog.exec_
"""
o_main_start = """\
called Grid.__init__
called HBox.__init__
called Label.__init__ with args ('Type of check:', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called ButtonGroup.__init__ with args ()
called RadioButton.__init__ with args ('&Xxx', {testobj}) {{}}
called ButtonGroup.addButton with arg of type <class 'mockgui.mockqtwidgets.MockRadioButton'>
called RadioButton.__init__ with args ('&Yyy', {testobj}) {{}}
called ButtonGroup.addButton with arg of type <class 'mockgui.mockqtwidgets.MockRadioButton'>
"""
o_main_bg1 = """\
called ButtonGroup.buttons
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockRadioButton'>
called RadioButton.setChecked with arg `True`
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockRadioButton'>
called ButtonGroup.id with arg of type <class 'mockgui.mockqtwidgets.MockRadioButton'>
called ButtonGroup.checkedButton
called RadioButton.isChecked
"""
o_main_bg2 = """\
called ButtonGroup.buttons
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockRadioButton'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockRadioButton'>
called ButtonGroup.id with arg of type <class 'mockgui.mockqtwidgets.MockRadioButton'>
called ButtonGroup.checkedButton
called RadioButton.isChecked
called RadioButton.isChecked
called ButtonGroup.button with arg '2'
called RadioButton.setChecked with arg `True`
"""
o_main_1a = """\
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (0, 0, 1, 2)
called VBox.__init__
called VBox.addSpacing
called Label.__init__ with args ('Check using:', {testobj})
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called VBox.addStretch
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'> at (1, 0, 2, 1)
called ButtonGroup.__init__ with args ({testobj},)
called HBox.__init__
called RadioButton.__init__ with args ('&Flake8', {testobj}) {{}}
called ButtonGroup.addButton with arg of type <class 'mockgui.mockqtwidgets.MockRadioButton'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockRadioButton'>
called PushButton.__init__ with args ('Configure', {testobj}) {{}}
called Signal.connect with args ({testobj.master.configure_linter},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (1, 1)
called HBox.__init__
called RadioButton.__init__ with args ('Py&Lint', {testobj}) {{}}
called ButtonGroup.addButton with arg of type <class 'mockgui.mockqtwidgets.MockRadioButton'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockRadioButton'>
called PushButton.__init__ with args ('Configure', {testobj}) {{}}
called Signal.connect with args ({testobj.master.configure_linter},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (2, 1)
called HBox.__init__
called RadioButton.__init__ with args ('&Ruff', {testobj}) {{}}
called ButtonGroup.addButton with arg of type <class 'mockgui.mockqtwidgets.MockRadioButton'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockRadioButton'>
"""
o_main_cb = """\
called RadioButton.setChecked with arg `True`
"""
o_main_1b = """\
called PushButton.__init__ with args ('Configure', {testobj}) {{}}
called Signal.connect with args ({testobj.master.configure_linter},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (3, 1)
"""
o_main_2 = """\
called Label.__init__ with args ('In file/directory:', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (4, 0)
called HBox.__init__
called Label.__init__ with args ('{fname}', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called HBox.addStretch
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (4, 1)
"""
o_main_3 = """\
called PushButton.__init__ with args ('&Zoek',) {{}}
called Signal.connect with args ({testobj.zoekdir},)
called Base.add_combobox_line with args ('In directory:', ['aaa']) {{'initial': '{fname}', 'button': {testobj.zoek}}}
called ComboBox.__init__
called ComboBox.setCompleter with arg None
called Signal.connect with args ({testobj.master.check_loc},)
"""
o_main_4 = """\
called Label.__init__ with args ('In de volgende files/directories:', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (4, 0, 1, 3)
called List.__init__
called List.insertItems with args (0, ['xxx', 'yyy'])
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockListBox'> at (5, 0, 1, 3)
"""
o_main_5 = """\
called PushButton.__init__ with args ('Configure', {testobj}) {{}}
called Signal.connect with args ({testobj.master.configure_filter},)
called Base.add_checkbox_line with args ('Use global whitelist/blacklist',) {{'toggle': True, 'button': {testobj.conf_filter}}}
"""
o_main_6 = """\
called CheckBox.__init__
called Base.add_checkbox_line with args ('Check repository files only (also does subdirectories)', False) {{}}
called CheckBox.__init__
"""
o_main_6a = """\
called CheckBox.__init__
"""
o_main_7 = """\
called Base.add_checkbox_line with args ('{extra}ook subdirectories doorzoeken', False) {{}}
called CheckBox.__init__
called SpinBox.__init__
called SpinBox.setMinimum with arg '-1'
called SpinBox.setValue with arg '5'
called Base.add_checkbox_line with args ('symlinks volgen - max. diepte (-1 is alles):',) {{'spinner': {testobj.vraag_diepte}}}
called CheckBox.__init__
called Base.add_checkbox_line with args ('selecteer (sub)directories om over te slaan',) {{}}
called CheckBox.__init__
called Base.add_checkbox_line with args ('selecteer bestanden om over te slaan',) {{}}
called CheckBox.__init__
"""
o_main_end = """\
called PushButton.__init__ with args ('Configure', {testobj}) {{}}
called Signal.connect with args ({testobj.master.configure_quiet},)
called Base.add_checkbox_line with args ('Output to file(s) directly',) {{'toggle': False, 'button': {testobj.conf_quiet}}}
called CheckBox.__init__
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('&Uitvoeren', {testobj}) {{}}
called Signal.connect with args ({testobj.master.doe},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('&Einde', {testobj}) {{}}
called Signal.connect with args ({testobj.close},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at ({row}, 0, 1, 2)
called VBox.__init__
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockGridLayout'>
called MainGui.setLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>
called ButtonGroup.buttons
called RadioButton.setFocus
called MainGui.show
"""
o_main_final = o_main_end + "called Base.doe\ncalled MainGui.close\n"
o_main_end += "called Application.exec_\n"
o_combo = """\
called Label.__init__ with args ('label text',)
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at ({row}, 0)
called ComboBox.__init__
called ComboBox.setMaximumWidth with arg `200`
called ComboBox.setMinimumWidth with arg `200`
called ComboBox.insertItems with args (0, ['item', 'list'])
called ComboBox.setEditable with arg `True`
called ComboBox.clearEditText
"""
o_combo_end1 = """\
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockComboBox'> at ({row}, 1)
"""
o_combo_end2 = """\
called ComboBox.setEditText with arg `start`
called HBox.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockComboBox'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at ({row}, 1)
"""
o_check = """\
called CheckBox.__init__
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'> at ({row}, 1)
"""
o_check2 = """\
called HBox.__init__
called CheckBox.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockSpinBox'>
called HBox.addStretch
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at ({row}, 1)
"""
o_check3 = """\
called HBox.__init__
called CheckBox.__init__
called CheckBox.toggle
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called Grid.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at ({row}, 1)
"""


@pytest.fixture
def expected_output():
    """provide test output generated for methods that setup screens
    """
    return {'filteroptions': o_filter,
            'quietoptions': o_quiet + o_quiet_pt2 + o_quiet_pt3,
            'quietoptions2': o_quiet + o_quiet_single + o_quiet_pt2 + o_quiet_pt3 + o_quiet_end,
            'quietoptions3': o_quiet + o_quiet_pt2 + o_quiet_multi + o_quiet_pt3 + o_quiet_end,
            'selectnames': o_names, 'selectnames_2': o_names.replace('bestanden', 'directories'),
            'results': o_results_start + o_results_end,
            'results2': o_results_start + "\\nxxx yyy" + o_results_end,
            'maingui_standard': (o_main_start + o_main_bg1 + o_main_1a + o_main_cb + o_main_1b
                                 + o_main_3 + o_main_5 + o_main_6 + o_main_7 + o_main_end),
            'maingui_standard2': (o_main_start + o_main_bg1 + o_main_1a + o_main_cb + o_main_1b
                                 + o_main_3 + o_main_5 + o_main_6 + o_main_7 + o_main_end),
            'maingui_single1': (o_main_start + o_main_bg2 + o_main_1a + o_main_1b + o_main_2
                                + o_main_end),
            'maingui_single2': (o_main_start + o_main_bg2 + o_main_1a + o_main_1b + o_main_2
                                + o_main_7 + o_main_end),
            'maingui_multi': (o_main_start + o_main_bg2 + o_main_1a + o_main_1b + o_main_4
                              + o_main_5 + o_main_6a + o_main_7 + o_main_end),
            'maingui_nogui': (o_main_start + o_main_bg2 + o_main_1a + o_main_1b + o_main_4
                              + o_main_5 + o_main_6a + o_main_7 + o_main_final),
            'combobox_row1': o_combo + o_combo_end1, 'combobox_row2': o_combo + o_combo_end2,
            'checkbox_row': o_check, 'checkbox_row2': o_check2, 'checkbox_row3': o_check3}

