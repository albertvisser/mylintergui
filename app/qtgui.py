"""AFRIFT PyQt5 versie omgebouwd naar gebruik pylint / flake8
"""
import os
import sys
import subprocess
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
import PyQt6.QtWidgets as qtw

# from .linter_base import iconame, LBase, log, Mode
from .config import Mode, cmddict, checktypes, default_option
common_path_txt = 'De bestanden staan allemaal in of onder de directory "{}"'
TXTW = 200
SEP = ', '


def waiting_cursor(func):
    "change the cursor before and after an operation"
    def wrap_operation(self):
        "the wrapped operation is a method without arguments"
        self.app.setOverrideCursor(gui.QCursor(core.Qt.CursorShape.WaitCursor))
        func(self)
        self.app.restoreOverrideCursor()
    return wrap_operation


def show_dialog(cls, *args, **kwargs):
    "execute the given dialog and return whether it's confirmed or not"
    dlg = cls(*args, **kwargs).exec()
    return dlg == qtw.QDialog.DialogCode.Accepted


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

    def setup_screen(self):
        "build gui"
        self.grid = qtw.QGridLayout()
        self.row = -1

        self.row += 1
        box = qtw.QHBoxLayout()
        box.addWidget(qtw.QLabel('Type of check:', self))
        self.check_options = qtw.QButtonGroup()
        options = ['&' + checktype.title() for checktype in checktypes]
        for text in options:
            self.check_options.addButton(qtw.QRadioButton(text, self))
        dflt_id = ''
        for btn in self.check_options.buttons():
            box.addWidget(btn)
            if btn.text() == '&' + str(self.master.checking_type).title():
                btn.setChecked(True)
            if btn.text() == options[default_option]:
                dflt_id = self.check_options.id(btn)
        if not self.check_options.checkedButton() and dflt_id:
            self.check_options.button(dflt_id).setChecked(True)
        self.grid.addLayout(box, self.row, 0, 1, 2)

        self.row += 1
        box = qtw.QVBoxLayout()
        box.addSpacing(5)
        box.addWidget(qtw.QLabel('Check using:', self))
        box.addStretch()
        self.grid.addLayout(box, self.row, 0, 2, 1)
        self.linters = qtw.QButtonGroup(self)

        for linter in cmddict:
            box = qtw.QHBoxLayout()
            linter_text = 'py&lint' if linter == 'pylint' else '&' + linter
            btn = qtw.QRadioButton(linter_text.title(), self)
            self.linters.addButton(btn)
            box.addWidget(btn)
            if self.master.linter_from_input == linter:
                btn.setChecked(True)
            btn = qtw.QPushButton('Configure', self)
            btn.clicked.connect(self.master.configure_linter)
            box.addWidget(btn)
            box.addStretch()
            self.grid.addLayout(box, self.row, 1)
            self.row += 1

        if self.master.mode == Mode.single.value:
            self.grid.addWidget(qtw.QLabel('In file/directory:', self), self.row, 0)
            box = qtw.QHBoxLayout()
            box.addWidget(qtw.QLabel(self.master.p['filelist'][0], self))
            box.addStretch()
            self.grid.addLayout(box, self.row, 1)
        elif self.master.mode == Mode.standard.value:
            initial = ''
            if self.master.p['filelist']:
                initial = self.master.p['filelist'][0]
            self.zoek = qtw.QPushButton("&Zoek")
            self.zoek.clicked.connect(self.zoekdir)
            self.vraag_dir = self.add_combobox_row("In directory:", self.master._mru_items["dirs"],
                                                   initial=initial, button=self.zoek)
            self.vraag_dir.setCompleter(None)
            self.vraag_dir.editTextChanged[str].connect(self.master.check_loc)
        else:  # if self.master.mode == Mode.multi.value:  # currently only other possibility
            self.grid.addWidget(qtw.QLabel('In de volgende files/directories:', self), self.row,
                                0, 1, 3)
            self.row += 1
            self.lbox = qtw.QListWidget(self)
            self.lbox.insertItems(0, self.master.p['filelist'])
            self.grid.addWidget(self.lbox, self.row, 0, 1, 3)

        if self.master.mode != Mode.single.value:
            self.row += 1
            self.conf_filter = qtw.QPushButton('Configure', self)
            self.conf_filter.clicked.connect(self.master.configure_filter)
            self.vraag_filter = self.add_checkbox_row('Use global whitelist/blacklist',
                                                      toggle=True, button=self.conf_filter)
        if self.master.mode == Mode.standard.value:
            self.row += 1
            self.master.p['fromrepo'] = self.master.repo_only
            self.vraag_repo = self.add_checkbox_row(
                'Check repository files only (also does subdirectories)',
                self.master.p['fromrepo'])
        if self.master.mode != Mode.single.value or os.path.isdir(self.master.p['filelist'][0]):
            txt = ''
            if self.master.mode == Mode.multi.value:
                txt = "van geselecteerde directories "
            self.vraag_subs = self.add_checkbox_row(
                txt + "ook subdirectories doorzoeken", self.master.p["subdirs"])
            self.vraag_diepte = qtw.QSpinBox(self)
            self.vraag_diepte.setMinimum(-1)
            self.vraag_diepte.setValue(5)
            self.vraag_links = self.add_checkbox_row("symlinks volgen - max. diepte (-1 is alles):",
                                                     spinner=self.vraag_diepte)
            self.ask_skipdirs = self.add_checkbox_row("selecteer (sub)directories om over te slaan")
            self.ask_skipfiles = self.add_checkbox_row("selecteer bestanden om over te slaan")
        self.row += 1
        self.conf_quiet = qtw.QPushButton('Configure', self)
        self.conf_quiet.clicked.connect(self.master.configure_quiet)
        self.vraag_quiet = self.add_checkbox_row('Output to file(s) directly',
                                                 toggle=self.master.dest_from_input,
                                                 button=self.conf_quiet)
        self.row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addStretch(1)
        self.b_doit = qtw.QPushButton('&Uitvoeren', self)
        self.b_doit.clicked.connect(self.master.doe)
        hbox.addWidget(self.b_doit)
        self.b_cancel = qtw.QPushButton('&Einde', self)
        self.b_cancel.clicked.connect(self.close)
        hbox.addWidget(self.b_cancel)
        hbox.addStretch(1)
        self.grid.addLayout(hbox, self.row, 0, 1, 2)

        vbox = qtw.QVBoxLayout()
        vbox.addLayout(self.grid)

        self.setLayout(vbox)
        self.linters.buttons()[0].setFocus()

        self.show()
        if self.master.skip_screen:
            self.master.doe()
            self.close()
        else:
            sys.exit(self.app.exec())

    def add_combobox_row(self, labeltext, itemlist, initial='', button=None):
        """add a line to the GUI containing a combobox
        """
        self.row += 1
        self.grid.addWidget(qtw.QLabel(labeltext), self.row, 0)
        cmb = qtw.QComboBox(self)
        cmb.setMaximumWidth(TXTW)
        cmb.setMinimumWidth(TXTW)
        cmb.insertItems(0, itemlist)
        cmb.setEditable(True)
        cmb.clearEditText()
        if initial:
            cmb.setEditText(initial)
        if button:
            box = qtw.QHBoxLayout()
            box.addWidget(cmb)
            box.addWidget(button)
            box.addStretch()
            self.grid.addLayout(box, self.row, 1)
        else:
            self.grid.addWidget(cmb, self.row, 1)
        return cmb

    def add_checkbox_row(self, text, toggle=False, spinner=None, button=None):
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
            box.addWidget(spinner)
        if button:
            box.addWidget(button)
        if spinner or button:
            box.addStretch()
            self.grid.addLayout(box, self.row, 1)
        else:
            self.grid.addWidget(chk, self.row, 1)
        return chk

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
                                                   self.vraag_dir.currentText())
        if dlg:
            self.vraag_dir.setEditText(dlg)


class FilterOptions(qtw.QDialog):
    """configure what files (not) to lint
    """
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.setWindowTitle(self.parent.master.title + " - configure")
        self.setWindowIcon(self.parent.appicon)
        vbox = qtw.QVBoxLayout()

        gbox = qtw.QGridLayout()
        row = 1
        gbox.addWidget(qtw.QLabel("Blacklist (do no lint):", self), row, 0, 1, 2)
        row += 1
        gbox.addWidget(qtw.QLabel("Directory names:", self), row, 0)
        self.skipdirs = qtw.QLineEdit(self)
        self.skipdirs.setMinimumWidth(200)
        self.skipdirs.setText(SEP.join(self.parent.master.blacklist['exclude_dirs']))
        gbox.addWidget(self.skipdirs, row, 1)
        row += 1
        gbox.addWidget(qtw.QLabel("File extensions:", self), row, 0)
        self.skipexts = qtw.QLineEdit(self)
        self.skipexts.setText(SEP.join(self.parent.master.blacklist['exclude_exts']))
        gbox.addWidget(self.skipexts, row, 1)
        row += 1
        gbox.addWidget(qtw.QLabel("File names:", self), row, 0)
        self.skipfiles = qtw.QLineEdit(self)
        self.skipfiles.setText(SEP.join(self.parent.master.blacklist['exclude_files']))
        gbox.addWidget(self.skipfiles, row, 1)
        row += 1
        gbox.addWidget(qtw.QLabel("", self), row, 0)
        row += 1
        gbox.addWidget(qtw.QLabel("Whitelist (only lint):", self), row, 0, 1, 2)
        row += 1
        gbox.addWidget(qtw.QLabel("File extensions:", self), row, 0)
        self.do_exts = qtw.QLineEdit(self)
        self.do_exts.setText(SEP.join(self.parent.master.blacklist['include_exts']))
        gbox.addWidget(self.do_exts, row, 1)
        row += 1
        gbox.addWidget(qtw.QLabel("Shebang lines:", self), row, 0)
        self.do_bangs = qtw.QLineEdit(self)
        self.do_bangs.setText(SEP.join(self.parent.master.blacklist['include_shebang']))
        gbox.addWidget(self.do_bangs, row, 1)
        row += 1
        gbox.addWidget(qtw.QLabel("", self), row, 0)
        vbox.addLayout(gbox)

        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        b_can = qtw.QPushButton("&Terug", self)
        b_can.clicked.connect(self.reject)
        hbox.addWidget(b_can)
        b_ok = qtw.QPushButton("&Klaar", self)
        b_ok.clicked.connect(self.accept)
        hbox.addWidget(b_ok)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def accept(self):
        """transfer chosen options to parent"""
        self.parent.master.blacklist = {
            'exclude_dirs': list(self.skipdirs.text().split(SEP)),
            'exclude_exts': list(self.skipexts.text().split(SEP)),
            'include_exts': list(self.do_exts.text().split(SEP)),
            'exclude_files': list(self.skipfiles.text().split(SEP)),
            'include_shebang': list(self.do_bangs.text().split(SEP)), }
        super().accept()


class QuietOptions(qtw.QDialog):
    """configure where to send output to
    """
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.setWindowTitle(self.parent.master.title + " - configure")
        self.setWindowIcon(self.parent.appicon)
        vbox = qtw.QVBoxLayout()
        vbox.addWidget(qtw.QLabel("Send output to:", self))

        box = qtw.QHBoxLayout()
        self.single = qtw.QRadioButton('Single file:', self)
        box.addWidget(self.single)
        self.fname = qtw.QLineEdit(self)
        self.fname.setMaximumWidth(TXTW)
        self.fname.setMinimumWidth(TXTW)
        self.fname.setText(self.parent.master.quiet_options['fname'])
        if self.parent.master.quiet_options['dest'] == Mode.single.name:
            self.single.setChecked(True)
        box.addWidget(self.fname)
        btn = qtw.QPushButton('Select', self)
        btn.clicked.connect(self.browse)
        box.addWidget(btn)
        box.addStretch()
        vbox.addLayout(box)

        box = qtw.QHBoxLayout()
        self.multi = qtw.QRadioButton('Multiple files like:', self)
        box.addWidget(self.multi)
        self.pattern = qtw.QLineEdit(self)
        self.pattern.setMaximumWidth(TXTW + 100)
        self.pattern.setMinimumWidth(TXTW + 100)
        if self.parent.master.quiet_options['dest'] == Mode.multi.name:
            self.multi.setChecked(True)
        self.pattern.setText(self.parent.master.quiet_options['pattern'])
        box.addWidget(self.pattern)
        box.addStretch()
        vbox.addLayout(box)

        box = qtw.QHBoxLayout()
        box.addSpacing(26)
        box.addWidget(qtw.QLabel('<ignore> part of filename:', self))
        self.ignore = qtw.QLineEdit(self)
        self.ignore.setMaximumWidth(TXTW)
        self.ignore.setMinimumWidth(TXTW)
        self.ignore.setText(self.parent.master.quiet_options['ignore'])
        box.addWidget(self.ignore)
        box.addStretch()
        vbox.addLayout(box)

        text = """\
        <linter>: replace linter name in path
        <ignore>: part of source filename not to include in target name
        <filename>: (remainder of) source filename
        <date>: datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        """
        vbox.addWidget(qtw.QLabel(text, self))

        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        b_can = qtw.QPushButton("&Terug", self)
        b_can.clicked.connect(self.reject)
        hbox.addWidget(b_can)
        b_ok = qtw.QPushButton("&Klaar", self)
        b_ok.clicked.connect(self.accept)
        hbox.addWidget(b_ok)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        if self.parent.master.dest_from_input:
            self.single.setChecked(True)
            self.fname.setText(self.parent.master.dest_from_input)

    def browse(self):
        """callback for selector
        """

    def accept(self):
        """transfer chosen options to parent"""
        self.parent.newquietoptions = {
            'single_file': self.single.isChecked(),
            'fname': self.fname.text(),
            'pattern': self.pattern.text(),
            'ignore': self.ignore.text()}
        super().accept()


class SelectNames(qtw.QDialog):
    """Tussenscherm om te verwerken files te kiezen
    """
    def __init__(self, parent, files=True):
        self.dofiles = files
        self.parent = parent
        super().__init__(parent)
        self.setWindowTitle(self.parent.master.title + " - file list")
        # self.setWindowIcon(gui.QIcon(self.parent.master.iconame))
        self.setWindowIcon(self.parent.appicon)
        vbox = qtw.QVBoxLayout()

        if files:
            text = "Selecteer de bestanden die je *niet* wilt verwerken"
        else:
            text = "Selecteer de directories die je *niet* wilt verwerken"
        txt = qtw.QLabel(text, self)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(txt)
        vbox.addLayout(hbox)
        self.sel_all = qtw.QCheckBox('Select/Unselect All', self)
        self.sel_all.clicked.connect(self.select_all)
        hbox = qtw.QHBoxLayout()
        hbox.addSpacing(10)
        hbox.addWidget(self.sel_all)
        self.flip_sel = qtw.QPushButton('Invert selection', self)
        self.flip_sel.clicked.connect(self.invert_selection)
        hbox.addStretch()
        hbox.addWidget(self.flip_sel)
        hbox.addSpacing(20)
        vbox.addLayout(hbox)

        self.frm = qtw.QFrame(self)   # attribuut van gemaakt tbv unittest
        fvbox = qtw.QVBoxLayout()
        self.checklist = []
        for item in self.parent.master.names:
            chk = qtw.QCheckBox(item, self.frm)
            fhbox = qtw.QHBoxLayout()
            fhbox.addWidget(chk)
            self.checklist.append(chk)
            fvbox.addLayout(fhbox)
        self.frm.setLayout(fvbox)
        scrl = qtw.QScrollArea(self)
        scrl.setWidget(self.frm)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(scrl)
        vbox.addLayout(hbox)

        b_can = qtw.QPushButton("&Terug", self)
        b_can.clicked.connect(self.reject)
        b_ok = qtw.QPushButton("&Klaar", self)
        b_ok.clicked.connect(self.accept)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(b_can)
        hbox.addWidget(b_ok)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def select_all(self):
        """check/uncheck all boxes
        """
        state = self.sel_all.isChecked()
        for chk in self.checklist:
            chk.setChecked(state)

    def invert_selection(self):
        """check unchecked and uncheck checked
        """
        for chk in self.checklist:
            chk.setChecked(not chk.isChecked())

    def accept(self):
        "dialoog afsluiten"
        dirs = []
        for chk in self.checklist:
            if chk.isChecked():
                if self.dofiles:
                    self.parent.master.names.remove(chk.text())
                else:
                    dirs.append(chk.text())
        if not self.dofiles:
            self.parent.master.names = dirs
        super().accept()


class Results(qtw.QDialog):
    """Show results on screen
    """
    helpinfo = ("Select a line and doubleclick or press Ctrl-G to open the indicated file\n"
                "at the indicated line (not in single file mode)")

    def __init__(self, parent, common_path=''):
        self.parent = parent
        self.common = common_path
        self.results = []
        breedte = 50 if self.parent.master.mode == Mode.single.value else 150
        super().__init__(parent)
        self.setWindowTitle(self.parent.master.resulttitel)
        # self.setWindowIcon(gui.QIcon(self.parent.master.iconame))
        self.setWindowIcon(self.parent.appicon)
        vbox = qtw.QVBoxLayout()

        hbox = qtw.QHBoxLayout()
        label_txt = (f"{self.parent.master.do_checks.rpt[0]}"
                     f" ({len(self.parent.master.do_checks.results)} items)")
        if self.parent.master.mode == Mode.multi.value:
            label_txt += '\n' + common_path_txt.format(self.common.rstrip(os.sep))
        self.txt = qtw.QLabel(label_txt, self)
        hbox.addWidget(self.txt)
        vbox.addLayout(hbox)

        # combobox/selector voor files
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel('Files checked:', self))
        self.filelist = qtw.QComboBox(self)
        self.filelist.addItems(self.parent.master.do_checks.filenames)
        self.filelist.setEditable(False)
        hbox.addWidget(self.filelist)
        hbox.addStretch()
        btn = qtw.QPushButton("&Go To File", self)
        btn.clicked.connect(self.goto_result)
        hbox.addWidget(btn)
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        # mag gewoon een listbox of een tekstvak worden - niet-proportioneel font graag
        self.lijst = qtw.QTextEdit(self)
        font = gui.QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.lijst.setCurrentFont(font)
        self.lijst.setReadOnly(True)

        self.populate_list()
        self.filelist.currentIndexChanged.connect(self.populate_list)

        hbox.addWidget(self.lijst)
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        btn = qtw.QPushButton("&Klaar", self)
        btn.clicked.connect(self.klaar)
        hbox.addWidget(btn)
        btn = qtw.QPushButton("&Repeat Action", self)
        btn.clicked.connect(self.refresh)
        hbox.addWidget(btn)
        btn = qtw.QPushButton("Copy to &File(s)", self)
        btn.clicked.connect(self.kopie)
        hbox.addWidget(btn)
        btn = qtw.QPushButton("Copy to &Clipboard", self)
        btn.clicked.connect(self.to_clipboard)
        hbox.addWidget(btn)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.resize(574 + breedte, 480)
        self.exec()

    def populate_list(self):
        """copy results to listbox
        """
        fname = self.filelist.currentText()
        text = self.parent.master.do_checks.results[fname]
        self.lijst.setText(text)

    def klaar(self):
        """finish dialog
        """
        qtw.QDialog.done(self, 0)

    def refresh(self):
        """callback for repeat action
        """
        self.results = []
        self.lijst.clear()
        self.parent.master.do_checks.rpt = ["".join(self.parent.master.do_checks.specs)]
        self.parent.execute_action()
        self.populate_list()
        self.filelist.setCurrentIndex(0)

    def kopie(self):
        """callback for button 'Copy to file'
        """
        dlg = QuietOptions(self.parent).exec()
        if not dlg:
            return
        if self.parent.newquietoptions['single_file']:
            fname = self.parent.master.get_output_filename(self.parent.newquietoptions['fname'])
            with open(fname, "w") as f_out:
                first_file = True
                for name, data in self.parent.master.do_checks.results.items():
                    if not first_file:
                        print('', file=f_out)
                        print('', file=f_out)
                    first_file = False
                    print(f'results for {name}', file=f_out)
                    print('', file=f_out)
                    print(data, file=f_out)
            msgstart = 'O'
        else:
            for name, data in self.parent.master.do_checks.results.items():
                fname = self.parent.master.get_output_filename(
                    self.parent.newquietoptions['pattern'], name)
                with open(fname, 'w') as f_out:
                    print(f'results for {name}', file=f_out)
                    print('', file=f_out)
                    print(data, file=f_out)
            msgstart = 'Last o'
        qtw.QMessageBox.information(self, self.parent.master.title,
                                    f'{msgstart}utput saved as {fname}')

    def help(self):
        """suggest workflow
        """
        qtw.QMessageBox.information(self, self.parent.master.title, self.helpinfo)

    def to_clipboard(self):
        """callback for button 'Copy to clipboard'
        """
        clp = qtw.QApplication.clipboard()
        text = []
        first_file = True
        for name, data in self.parent.master.do_checks.results.items():
            if not first_file:
                text.extend(['', ''])
            first_file = False
            text.extend([f'results for {name}', '', data])
        clp.setText('\n'.join(text))
        qtw.QMessageBox.information(self, self.parent.master.title, 'Output copied to clipboard')

    def goto_result(self):
        """open the file containing the checked lines
        """
        fname = self.filelist.currentText()
        prog, fileopt = self.parent.master.editor_option[:2]
        subprocess.run(prog + [fileopt.format(fname)], check=False)  # , lineopt.format(line)])
