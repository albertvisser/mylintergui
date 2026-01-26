"""AFRIFT PyQt5 versie omgebouwd naar gebruik pylint / flake8
"""
# import os
import sys
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
import PyQt6.QtWidgets as qtw


def waiting_cursor(func):
    "change the cursor before and after an operation"
    def wrap_operation(self):
        "the wrapped operation is a method without arguments"
        self.app.setOverrideCursor(gui.QCursor(core.Qt.CursorShape.WaitCursor))
        func(self)
        self.app.restoreOverrideCursor()
    return wrap_operation


def show_dialog(dlg):  # (cls, *args, **kwargs):
    "execute the given dialog and return whether it's confirmed or not"
    # dlg = cls(*args, **kwargs).exec()
    # return dlg == qtw.QDialog.DialogCode.Accepted
    return dlg.exec() == qtw.QDialog.DialogCode.Accepted


def show_message(parent, title, message):
    "show a nessage in a message box"
    qtw.QMessageBox.information(parent, title, message)


class LinterGui(qtw.QWidget):
    """Hoofdscherm van de applicatie

    QMainWindow is een beetje overkill, daarom maar een QWidget
    """
    def __init__(self, master):
        self.app = qtw.QApplication(sys.argv)
        super().__init__()
        self.master = master

        self.setWindowTitle(self.master.title)
        self.appicon = gui.QIcon(self.master.iconame)
        self.setWindowIcon(self.appicon)

    def start_display(self):
        "build gui"
        self.grid = qtw.QGridLayout()
        self.row = -1

    def build_radiobutton_row(self, title, optiondefs):
        "build horizontal selector for linter severity"
        self.row += 1
        self.grid.addWidget(qtw.QLabel(title, self), self.row, 0)
        options = qtw.QButtonGroup()
        box = qtw.QHBoxLayout()
        # dflt_id = ''
        for text, checked in optiondefs:
            btn = qtw.QRadioButton(text, self)
            options.addButton(btn)
            box.addWidget(btn)
            # if btn.text() == '&' + str(self.master.checking_type).title():
            if checked:
                btn.setChecked(True)
            # if btn.text() == optiondefs[default_option]:
            #     dflt_id = options.id(btn)
        # if not options.checkedButton() and dflt_id:
        #     options.button(dflt_id).setChecked(True)
        self.grid.addLayout(box, self.row, 1, 1, 2)
        return options

    def build_radiobutton_block(self, title, optiondefs):
        "build vertical selector for which linter to use"
        self.row += 1
        self.grid.addWidget(qtw.QLabel(title, self), self.row, 0)
        options = qtw.QButtonGroup()
        for text, checked in optiondefs:
            box = qtw.QHBoxLayout()
            btn = qtw.QRadioButton(text.title(), self)
            options.addButton(btn)
            box.addWidget(btn)
            # if self.master.linter_from_input == text.replace('&', ''):
            if checked:
                btn.setChecked(True)
            # self.grid.addWidget(btn, self.row, 1)
            btn = qtw.QPushButton('Configure', self)
            btn.clicked.connect(self.master.configure_linter)
            box.addWidget(btn)
            box.addStretch()
            self.grid.addLayout(box, self.row, 1)
            # self.grid.addWidget(btn, self.row, 2)
            self.row += 1
        return options

    def add_combobox_row(self, labeltext, itemlist, initial='', width=0, callback=None, button=None):
        """add a line to the GUI containing a combobox
        """
        self.row += 1
        self.grid.addWidget(qtw.QLabel(labeltext), self.row, 0)
        cmb = qtw.QComboBox(self)
        if width:
            cmb.setMaximumWidth(width)
            cmb.setMinimumWidth(width)
        cmb.insertItems(0, itemlist)
        cmb.setEditable(True)
        cmb.clearEditText()
        if initial:
            cmb.setEditText(initial)
        cmb.setCompleter(None)
        if callback:
            cmb.editTextChanged[str].connect(callback)
            # cmb.editTextChanged.connect(callback)
        if button:
            box = qtw.QHBoxLayout()
            btn = qtw.QPushButton(button[0])
            btn.clicked.connect(button[1])
            box.addWidget(cmb)
            box.addWidget(btn)
            box.addStretch()
            self.grid.addLayout(box, self.row, 1)
        else:
            self.grid.addWidget(cmb, self.row, 1)
        return cmb

    def show_single_mode_info(self, locationtext, value):
        "show which file will be linted"
        self.row += 1
        self.grid.addWidget(qtw.QLabel(locationtext, self), self.row, 0)
        box = qtw.QHBoxLayout()
        box.addWidget(qtw.QLabel(value, self))
        # box.addStretch()
        self.grid.addLayout(box, self.row, 1, 1, 2)

    def show_multi_mode_info(self, locationtext, values):
        "show the files / directories to apply linting to"
        self.row += 1
        self.grid.addWidget(qtw.QLabel(locationtext, self), self.row, 0, 1, 3)
        lbox = qtw.QListWidget(self)
        lbox.insertItems(0, values)
        self.grid.addWidget(lbox, self.row, 0, 1, 3)

    def add_checkbox_line(self, text, toggle=False, spinner=None, button=None):
        """add a line to the GUI containing a checkbox
        """
        self.row += 1
        if spinner or button:
            box = qtw.QHBoxLayout()
        chk = qtw.QCheckBox(text, self)
        if toggle:
            chk.toggle()
        if spinner or button:
            box.addWidget(chk)
        if spinner:
            spin = qtw.QSpinBox(self)
            spin.setMinimum(spinner[0])
            spin.setValue(spinner[1])
            box.addWidget(spin)
        else:
            spin = None
        if button:
            btn = qtw.QPushButton(button[0], self)
            btn.clicked.connect(button[1])
            box.addWidget(btn)
        if spinner or button:
            box.addStretch()
            self.grid.addLayout(box, self.row, 1)
        else:
            self.grid.addWidget(chk, self.row, 1)
        return chk, spin

    def add_buttons(self, buttondefs):
        "add action buttons to the bottom of the display"
        self.row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addStretch(1)
        for text, callback in buttondefs:
            btn = qtw.QPushButton(text, self)
            btn.clicked.connect(callback)
            hbox.addWidget(btn)
        hbox.addStretch(1)
        self.grid.addLayout(hbox, self.row, 0, 1, 2)

    def finalize_display(self, buttongroup):
        "last actions needed before showing"
        vbox = qtw.QVBoxLayout()
        vbox.addLayout(self.grid)
        self.setLayout(vbox)
        buttongroup.buttons()[0].setFocus()

    def go(self):
        "start event loop"
        sys.exit(self.app.exec())

    def keyPressEvent(self, event):
        """event handler voor toetsaanslagen"""
        if event.key() == core.Qt.Key.Key_Escape:
            self.close()

    def get_radiogroup_checked(self, group):
        """return the text of the checked radiobutton
        """
        test = group.checkedButton() or None
        if test:
            test = test.text().replace('&', '').lower()
        return test

    def meld_fout(self, mld):
        "show message as error"
        qtw.QMessageBox.critical(self, self.master.fouttitel, mld, qtw.QMessageBox.StandardButton.Ok)

    def meld_info(self, msg):
        "show message as informational"
        qtw.QMessageBox.information(self, self.master.resulttitel, msg,
                                    qtw.QMessageBox.StandardButton.Ok)

    def get_combobox_textvalue(self, widget):
        "get text shown in combobox"
        return widget.currentText()

    def set_checkbox_value(self, widget, value):
        "set checkbox to given value"
        widget.setChecked(value)

    def get_checkbox_value(self, widget):
        "get value for checkbox"
        return widget.isChecked()

    def get_spinbox_value(self, widget):
        "get value from spinbox"
        return widget.value()

    @waiting_cursor
    def execute_action(self):
        """change cursor, do the linting and change the cursor back
        """
        self.master.do_checks.do_action()

    def zoekdir(self):
        """event handler voor 'zoek in directory'"""
        dlg = qtw.QFileDialog.getExistingDirectory(self, "Choose a directory:",
                                                   self.master.vraag_dir.currentText())
        if dlg:
            self.master.vraag_dir.setEditText(dlg)


class FilterOptionsGui(qtw.QDialog):
    """configure what files (not) to lint
    """
    def __init__(self, master, parent, title):
        self.master = master
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(parent.appicon)
        self.vbox = qtw.QVBoxLayout()
        self.gbox = qtw.QGridLayout()
        self.vbox.addLayout(self.gbox)
        self.row = 0
        self.setLayout(self.vbox)

    def add_title_line(self, text):
        "add a line with text"
        self.row += 1
        self.gbox.addWidget(qtw.QLabel(text, self), self.row, 0, 1, 2)

    def add_textentry_line(self, caption, initialtext, width=0):
        "add a line with some fixed text and a textentry field"
        self.row += 1
        self.gbox.addWidget(qtw.QLabel(caption, self), self.row, 0)
        textfield = qtw.QLineEdit(self)
        if width:
            textfield.setMinimumWidth(width)
        textfield.setText(initialtext)
        self.gbox.addWidget(textfield, self.row, 1)
        return textfield

    def add_buttons(self, buttondefs):
        "add action buttons at the bottom of the display"
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        for text, callback in buttondefs:
            btn = qtw.QPushButton(text, self)
            btn.clicked.connect(callback)
            hbox.addWidget(btn)
        hbox.addStretch()
        self.vbox.addLayout(hbox)

    def accept(self):
        """transfer chosen options to parent"""
        self.master.confirm()
        super().accept()

    def get_textentry_value(self, textfield):
        "return the value of the entered text"
        return textfield.text()


class QuietOptionsGui(qtw.QDialog):
    """configure where to send output to
    """
    def __init__(self, master, parent, title):
        self.master = master
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(parent.appicon)
        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)

    def start_line(self):
        "add an empty line to the display"
        box = qtw.QHBoxLayout()
        return box

    def add_text_to_line(self, box, text, before=0):
        "add some fixed text to the screen line"
        if before:
            box.addSpacing(before)
        box.addWidget(qtw.QLabel(text, self))

    def add_radiobutton_to_line(self, box, text, state):
        "add a checkbox to the screen line"
        rb = qtw.QRadioButton(text, self)
        box.addWidget(rb)
        if state:
            rb.setChecked(True)
        return rb

    def add_textentry_to_line(self, box, initialtext, width=0):
        "add a text entry field to the screen line"
        textfield = qtw.QLineEdit(self)
        if width:
            textfield.setMaximumWidth(width)
            textfield.setMinimumWidth(width)
        textfield.setText(initialtext)
        box.addWidget(textfield)
        return textfield

    def add_button_to_line(self, box, text, callback):
        "add a button to the screen line"
        btn = qtw.QPushButton(text, self)
        btn.clicked.connect(callback)
        box.addWidget(btn)

    def end_line(self, box):
        "add an ending to the screen line"
        box.addStretch()
        self.vbox.addLayout(box)

    def add_buttons(self, buttondefs):
        "add action buttons at the bottom of the display"
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        for text, callback in buttondefs:
            btn = qtw.QPushButton(text, self)
            btn.clicked.connect(callback)
            hbox.addWidget(btn)
        hbox.addStretch()
        self.vbox.addLayout(hbox)

    def browse(self):
        """callback for selector
        """
        # TODO

    def accept(self):
        """transfer chosen options to parent"""
        self.master.confirm()
        super().accept()

    def set_radiobutton_value(self, rb, value):
        "set the state of a radiobutton"
        rb.setChecked(value)

    def get_radiobutton_value(self, rb):
        "return the state of a radiobutton"
        return rb.isChecked()

    def set_textentry_value(self, textfield, text):
        "set the text in a textfield"
        textfield.setText(text)

    def get_textentry_value(self, textfield):
        "return the entered value in a text field"
        return textfield.text()


class SelectNamesGui(qtw.QDialog):
    """Tussenscherm om te verwerken files te kiezen
    """
    def __init__(self, master, parent, title):
        self.master = master
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(parent.appicon)
        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)

    def start_line(self):
        "start a new line on the display"
        hbox = qtw.QHBoxLayout()
        self.vbox.addLayout(hbox)
        return hbox

    def add_text_to_line(self, line, text):
        "put some fixed text on the screen line"
        txt = qtw.QLabel(text, self)
        line.addWidget(txt)

    def add_checkbox_to_line(self, line, text, callback, before=0):
        "add a checkbox to the screen line"
        chk = qtw.QCheckBox(text, self)
        chk.clicked.connect(callback)
        if before:
            line.addSpacing(before)
        line.addWidget(chk)
        return chk

    def add_button_to_line(self, line, text, callback, before=0):
        "add an action button to the screen line"
        btn = qtw.QPushButton(text, self)
        btn.clicked.connect(callback)
        if before:
            line.addSpacing(before)
        line.addWidget(btn)
        # line.addStretch()
        return btn

    def create_checkbox_list(self, names):
        "add a list of names with checkboxes to the display"
        self.frm = qtw.QFrame(self)   # attribuut van gemaakt tbv unittest
        fvbox = qtw.QVBoxLayout()
        checklist = []
        for item in names:
            chk = qtw.QCheckBox(item, self.frm)
            fhbox = qtw.QHBoxLayout()
            fhbox.addWidget(chk)
            checklist.append(chk)
            fvbox.addLayout(fhbox)
        self.frm.setLayout(fvbox)
        scrl = qtw.QScrollArea(self)
        scrl.setWidget(self.frm)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(scrl)
        self.vbox.addLayout(hbox)
        return checklist

    def create_button_bar(self, buttondefs):
        "add a sript with action buttons at the bottom of the display"
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        for name, callback in buttondefs:
            btn = qtw.QPushButton(name, self)
            btn.clicked.connect(callback)
            hbox.addWidget(btn)
        hbox.addStretch()
        self.vbox.addLayout(hbox)

    def get_checkbox_text(self, cb):
        "return the label text of a checkbox"
        return cb.text()

    def get_checkbox_value(self, cb):
        "return the state of a checkbox"
        return cb.isChecked()

    def set_checkbox_value(self, cb, state):
        "set the state of a checkbox"
        cb.setChecked(state)

    def accept(self):
        "dialoog afsluiten"
        self.master.confirm()
        super().accept()


class ResultsGui(qtw.QDialog):
    """Show results on screen
    """
    helpinfo = ("Select a line and doubleclick or press Ctrl-G to open the indicated file\n"
                "at the indicated line (not in single file mode)")

    def __init__(self, master, parent, title, breedte):
        self.master = master
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(parent.appicon)
        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)
        self.resize(574 + breedte, 480)

    def add_top_text(self, label_txt):
        "add some fixed text at the top of the display"
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel(label_txt, self))
        self.vbox.addLayout(hbox)

    def add_combobox_line(self, text, items):
        "add a combobox/selector voor files"
        hbox = qtw.QHBoxLayout()
        self.vbox.addLayout(hbox)
        hbox.addWidget(qtw.QLabel(text, self))
        cmb = qtw.QComboBox(self)
        cmb.addItems(items)
        cmb.setEditable(False)
        cmb.currentIndexChanged.connect(self.master.populate_list)
        hbox.addWidget(cmb)
        hbox.addStretch()
        return hbox, cmb

    def add_button_to_line(self, hbox, text, callback):
        "add an action button to the line"
        btn = qtw.QPushButton(text, self)
        btn.clicked.connect(callback)
        hbox.addWidget(btn)

    def add_results_list(self):
        "add a text field to present the linting results"
        hbox = qtw.QHBoxLayout()
        lijst = qtw.QTextEdit(self)
        font = gui.QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        lijst.setCurrentFont(font)
        lijst.setReadOnly(True)
        hbox.addWidget(lijst)
        self.vbox.addLayout(hbox)
        return lijst

    def add_buttons(self, buttondefs):
        "add action buttons at the bottom of the display"
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        for text, callback in buttondefs:
            btn = qtw.QPushButton(text, self)
            btn.clicked.connect(callback)
            hbox.addWidget(btn)
        hbox.addStretch()
        self.vbox.addLayout(hbox)

    def get_combobox_value(self, cmb):
        "get the selected value from a combobox"
        return cmb.currentText()

    def set_combobox_value(self, cmb, value):
        "select a value in a combobox"
        return cmb.setCurrentIndex(value)

    def set_textbox_value(self, textbox, text):
        "add contents to the results list if given, otherwise just clear out"
        textbox.clear()
        if text:
            textbox.setText(text)

    def klaar(self):
        """finish dialog
        """
        qtw.QDialog.done(self, 0)

    def copy_to_clipboard(self, data):
        """callback for button 'Copy to clipboard'
        """
        clp = qtw.QApplication.clipboard()
        clp.setText(data)
