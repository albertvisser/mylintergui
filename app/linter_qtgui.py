"""AFRIFT PyQt versie omgebouwd naar gebruik pylint / flake8
"""
import os
import sys
import subprocess
import PyQt5.QtCore as core
import PyQt5.QtGui as gui
import PyQt5.QtWidgets as qtw

from .linter_base import iconame, LBase, log, Mode
from .linter_exec import Linter
common_path_txt = 'De bestanden staan allemaal in of onder de directory "{}"'
TXTW = 200


class QuietOptions(qtw.QDialog):
    """configure where to send output to
    """
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.setWindowTitle(self.parent.title + " - configure")
        self.setWindowIcon(gui.QIcon(iconame))
        vbox = qtw.QVBoxLayout()
        vbox.addWidget(qtw.QLabel("Send output to:", self))

        box = qtw.QHBoxLayout()
        self.single = qtw.QRadioButton('Single file:', self)
        box.addWidget(self.single)
        self.fname = qtw.QLineEdit(self)
        self.fname.setMaximumWidth(TXTW)
        self.fname.setMinimumWidth(TXTW)
        if self.parent.quiet_options['dest'] == 'single':
            self.single.setChecked(True)
            self.fname.setText(self.parent.quiet_options['pattern'])
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
        if self.parent.quiet_options['dest'] == 'multi':
            self.multi.setChecked(True)
            patt = self.parent.quiet_options['pattern']
            if not patt:
                patt = '~/.linters/<linter>/<ignore>/<filename>'
            self.pattern.setText(patt)
        box.addWidget(self.pattern)
        box.addStretch()
        vbox.addLayout(box)

        text = """\
        <linter>: replace linter name in path
        <ignore>: part of source filename not to include in target, e.g. ~/projects/
        <filename>: (remainder of) source filename
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
        if self.parent.dest_from_input:
            self.single.setChecked(True)
            self.fname.setText(self.parent.dest_from_input)

    def browse(self):
        pass

    def accept(self):
        """transfer chosen options to parent"""
        super().accept()


class SelectNames(qtw.QDialog):
    """Tussenscherm om te verwerken files te kiezen
    """
    def __init__(self, parent, files=True):
        self.dofiles = files
        self.parent = parent
        super().__init__(parent)
        self.setWindowTitle(self.parent.title + " - file list")
        self.setWindowIcon(gui.QIcon(iconame))
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

        frm = qtw.QFrame(self)
        fvbox = qtw.QVBoxLayout()
        self.checklist = []
        for item in self.parent.names:
            chk = qtw.QCheckBox(item, frm)
            fhbox = qtw.QHBoxLayout()
            fhbox.addWidget(chk)
            self.checklist.append(chk)
            fvbox.addLayout(fhbox)
        frm.setLayout(fvbox)
        scrl = qtw.QScrollArea(self)
        scrl.setWidget(frm)
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
        state = self.sel_all.isChecked()
        for chk in self.checklist:
            chk.setChecked(state)

    def invert_selection(self):
        for chk in self.checklist:
            chk.setChecked(not chk.isChecked())

    def accept(self):
        "dialoog afsluiten"
        dirs = []
        for chk in self.checklist:
            if chk.isChecked():
                if self.dofiles:
                    self.parent.names.remove(chk.text())
                else:
                    dirs.append(chk.text())
        if not self.dofiles:
            self.parent.names = dirs
        super().accept()


class Results(qtw.QDialog):
    """Show results on screen
    """
    def __init__(self, parent, common_path=''):
        self.parent = parent
        self.common = common_path
        self.show_context = self.parent.p["context"]
        self.results = []
        titel = 'Regel' if self.parent.apptype == "single" else 'File/Regel'
        breedte = 50 if self.parent.apptype == "single" else 150
        super().__init__(parent)
        self.setWindowTitle(self.parent.resulttitel)
        self.setWindowIcon(gui.QIcon(iconame))
        vbox = qtw.QVBoxLayout()

        hbox = qtw.QHBoxLayout()
        label_txt = "{0} ({1} items)".format(self.parent.zoekvervang.rpt[0],
                                             len(self.parent.zoekvervang.rpt) - 1)
        if self.parent.apptype == "multi":
            label_txt += '\n' + common_path_txt.format(self.common)
        self.txt = qtw.QLabel(label_txt, self)
        hbox.addWidget(self.txt)
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        self.lijst = qtw.QTableWidget(self)
        self.lijst.verticalHeader().setVisible(False)
        self.lijst.setGridStyle(core.Qt.NoPen)  # hierbij niet
        if self.show_context:
            self.lijst.setColumnCount(3)
            self.lijst.setColumnWidth(1, 200)
            self.lijst.setColumnWidth(2, 340)
            self.lijst.setHorizontalHeaderLabels((titel, 'Context', 'Tekst'))
        else:
            self.lijst.setColumnCount(2)
            self.lijst.setColumnWidth(1, 520)
            self.lijst.setHorizontalHeaderLabels((titel, 'Tekst'))
        self.lijst.setColumnWidth(0, breedte)
        self.lijst.horizontalHeader().setStretchLastSection(True)
        self.populate_list()
        ## self.lijst.cellDoubleClicked[int, int].connect(self.goto_result)
        self.lijst.cellDoubleClicked.connect(self.goto_result)
        act = qtw.QAction('Help', self)
        act.setShortcut('F1')
        act.triggered.connect(self.help)
        self.addAction(act)
        act = qtw.QAction('Goto Result', self)
        act.setShortcut('Ctrl+G')
        act.triggered.connect(self.to_result)
        self.addAction(act)
        hbox.addWidget(self.lijst)
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addStretch(1)
        btn = qtw.QPushButton("&Klaar", self)
        btn.clicked.connect(self.klaar)
        hbox.addWidget(btn)
        btn = qtw.QPushButton("&Repeat Search", self)
        btn.clicked.connect(self.refresh)
        if self.parent.p['vervang']:
            btn.setEnabled(False)
        hbox.addWidget(btn)
        btn = qtw.QPushButton("Copy to &File", self)
        btn.clicked.connect(self.kopie)
        hbox.addWidget(btn)
        btn = qtw.QPushButton("Copy to &Clipboard", self)
        btn.clicked.connect(self.to_clipboard)
        hbox.addWidget(btn)
        self.chk = qtw.QCheckBox("toon directorypad in uitvoer", self)
        if self.parent.apptype == "single":
            self.chk.setEnabled(False)
        hbox.addWidget(self.chk)
        self.chk = qtw.QCheckBox("comma-delimited", self)
        hbox.addWidget(self.chk)
        hbox.addStretch()
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.resize(574 + breedte, 480)
        self.exec_()

    def populate_list(self):
        """copy results to listbox
        """
        ## headers = []
        for ix, line in enumerate(self.parent.zoekvervang.rpt):
            if ix == 0:
                kop = line
            elif line != "":
                where, what = line.split(": ", 1)
                if self.parent.apptype == "single":
                    if "r. " in where:
                        lineno = where.split("r. ", 1)[1]
                        ## if ix == 1:
                        ##     kop += " in {0}".format(fname)
                        where = lineno
                    else:
                        where = ""
                if self.common:
                    where = where.replace(self.common, "")
                if self.show_context:
                    where, rest = where.rsplit(' (', 1)
                    context = rest.split(')')[0]
                self.lijst.insertRow(ix - 1)
                self.lijst.setRowHeight(ix - 1, 18)
                ## headers.append('')
                col = 0
                rowitem = []
                item = qtw.QTableWidgetItem(where)
                item.setFlags(core.Qt.ItemIsSelectable | core.Qt.ItemIsEnabled)
                self.lijst.setItem(ix - 1, col, item)
                rowitem.append(where)
                if self.show_context:
                    col += 1
                    item = qtw.QTableWidgetItem(context)
                    item.setFlags(core.Qt.ItemIsSelectable | core.Qt.ItemIsEnabled)
                    self.lijst.setItem(ix - 1, col, item)
                    rowitem.append(context)
                col += 1
                item = qtw.QTableWidgetItem(what)
                item.setFlags(core.Qt.ItemIsSelectable | core.Qt.ItemIsEnabled)
                self.lijst.setItem(ix - 1, col, item)
                rowitem.append(what)
                self.results.append(tuple(rowitem))
        ## self.lijst.setVerticalHeaderLabels(headers)
        self.results.insert(0, kop)

    def klaar(self):
        """finish dialog
        """
        qtw.QDialog.done(self, 0)

    def get_results(self):
        """apply switch to show complete path to results
        """
        toonpad = True if self.cb.isChecked() else False
        comma = True if self.cb2.isChecked() else False
        text = ["{}".format(self.results[0])]
        if self.parent.apptype == "multi" and not toonpad:
            text.append(common_path_txt.format(self.common) + '\n')
        if comma:
            import io
            import csv
            textbuf = io.StringIO()
            writer = csv.writer(textbuf, dialect='unix')
        for item in self.results[1:]:
            result = list(item)
            if toonpad and self.parent.apptype == 'multi':
                result[0] = self.common + result[0]
            ## elif not toonpad and self.parent.apptype != 'multi':
                ## result[0] = result[0].split(os.sep)[-1]
            if comma:
                writer.writerow(result)
            else:
                text.append(" ".join(result))
        if comma:
            text = textbuf.getvalue().split("\n")
            textbuf.close()
        return text

    def refresh(self):
        self.results = []
        self.lijst.clearContents()
        self.parent.zoekvervang.rpt = ["".join(self.parent.zoekvervang.specs)]
        self.parent.zoekvervang.do_action(search_python=self.parent.p["context"])
        if len(self.parent.zoekvervang.rpt) == 1:
            qtw.QMessageBox.information(self, self.parent.resulttitel,
                                        "Niks gevonden", qtw.QMessageBox.Ok)
            super().done(0)
        label_txt = "{0} ({1} items)".format(self.parent.zoekvervang.rpt[0],
                                             len(self.parent.zoekvervang.rpt) - 1)
        if self.parent.apptype == "multi":
            label_txt += '\n' + common_path_txt.format(self.common)
        self.txt.setText(label_txt)
        self.populate_list()

    def kopie(self):
        """callback for button 'Copy to file'
        """
        fn_out = self.parent.p["zoek"]
        for char in '/\\?%*:|"><.':
            if char in fn_out:
                fn_out = fn_out.replace(char, "~")
        fn_out = fn_out.join(("files containing ", ".txt"))
        dlg = qtw.QFileDialog.getSaveFileName(self,
                                              "Resultaat naar bestand kopieren",
                                              str(self.parent.hier / fn_out),
                                              "Text files (*.txt);;All files (*.*)")
        if not dlg[0]:
            return
        with open(dlg[0], "w") as f_out:
            for line in self.get_results():
                f_out.write(line + "\n")

    def help(self):
        qtw.QMessageBox.information(self, self.parent.title,
                                    "Select a line and doubleclick or press Ctrl-G"
                                    " to open the indicated file\n"
                                    "at the indicated line (not in single file mode)")

    def to_clipboard(self):
        """callback for button 'Copy to clipboard'
        """
        _ = qtw.QApplication.clipboard()

    def to_result(self):
        print('shortcut pressed')
        self.goto_result(self.lijst.currentRow(), self.lijst.currentColumn())

    def goto_result(self, row, col):
        """open the file containing the selected item
        """
        if self.parent.apptype == 'single':
            qtw.QMessageBox.information(self, 'ahem', 'Not in single file mode')
            return
        selected = self.results[row + 1]
        target, line = selected[0].split(' r. ')
        target = self.common + target
        prog, fileopt, lineopt = self.parent.editor_option
        subprocess.run([prog, fileopt.format(target), lineopt.format(line)])


class MainFrame(qtw.QWidget, LBase):
    """Hoofdscherm van de applicatie

    QMainWindow is een beetje overkill, daarom maar een QWidget
    """
    def __init__(self, parent=None, args=None):
        app = qtw.QApplication(sys.argv)
        super().__init__(parent)
        self.set_mode(args)

        self.setWindowTitle(self.title)
        self.setWindowIcon(gui.QIcon(iconame))

        self.grid = qtw.QGridLayout()
        self.row = -1

        self.row += 1
        box = qtw.QVBoxLayout()
        box.addSpacing(5)
        box.addWidget(qtw.QLabel('Check using:', self))
        box.addStretch()
        self.grid.addLayout(box, self.row, 0, 2, 1)
        self.linters = qtw.QButtonGroup(self)

        box = qtw.QHBoxLayout()
        self.use_pylint = qtw.QRadioButton('Pylint', self)
        self.linters.addButton(self.use_pylint)
        box.addWidget(self.use_pylint)
        if self.linter_from_input == 'pylint':
            self.use_pylint.setChecked(True)
        self.conf_pylint = qtw.QPushButton('Configure', self)
        self.conf_pylint.clicked.connect(self.configure_pylint)
        box.addWidget(self.conf_pylint)
        box.addStretch()
        self.grid.addLayout(box, self.row, 1)

        self.row += 1
        box = qtw.QHBoxLayout()
        self.use_flake8 = qtw.QRadioButton('Flake8', self)
        self.linters.addButton(self.use_flake8)
        box.addWidget(self.use_flake8)
        if self.linter_from_input == 'flake8':
            self.use_flake8.setChecked(True)
        self.conf_flake8 = qtw.QPushButton('Configure', self)
        self.conf_flake8.clicked.connect(self.configure_flake8)
        box.addWidget(self.conf_flake8)
        box.addStretch()
        self.grid.addLayout(box, self.row, 1)

        self.row += 1
        if self.mode == Mode.single.value:
            self.grid.addWidget(qtw.QLabel('In file/directory:', self), self.row, 0)
            box = qtw.QHBoxLayout()
            box.addWidget(qtw.QLabel(self.fnames[0], self))
            box.addStretch()
            self.grid.addLayout(box, self.row, 1)
        elif self.mode == Mode.standard.value:
            ## self.grid.addWidget(qtw.QLabel('In directory:', self), self.row, 0)
            initial = ''
            if self.fnames:
                initial = self.fnames[0]
            self.zoek = qtw.QPushButton("&Zoek")
            self.zoek.clicked.connect(self.zoekdir)
            self.vraag_dir = self.add_combobox_row("In directory:",
                                                   self._mru_items["dirs"],
                                                   initial=initial, button=self.zoek)
        elif self.mode == Mode.multi.value:
            self.grid.addWidget(qtw.QLabel('In de volgende files/directories:', self),
                                self.row, 0, 1, 3)
            self.row += 1
            self.lbox = qtw.QListWidget(self)
            self.lbox.insertItems(0, self.fnames)
            self.grid.addWidget(self.lbox, self.row, 0, 1, 3)

        if self.mode != Mode.single.value or os.path.isdir(self.fnames[0]):
            txt = ''
            if self.mode == Mode.multi.value:
                txt = "van geselecteerde directories "
            self.vraag_subs = self.add_checkbox_row(txt + "ook subdirectories "
                                                    "doorzoeken", self.p["subdirs"])
            self.vraag_diepte = qtw.QSpinBox(self)
            self.vraag_diepte.setMinimum(-1)
            self.vraag_diepte.setValue(5)
            self.vraag_links = self.add_checkbox_row("symlinks volgen - max. diepte "
                                                     "(-1 is alles):",
                                                     spinner=self.vraag_diepte)
            self.ask_skipdirs = self.add_checkbox_row("selecteer (sub)directories "
                                                      "om over te slaan")
            self.ask_skipfiles = self.add_checkbox_row("selecteer bestanden "
                                                       "om over te slaan")

        self.row += 1
        box = qtw.QHBoxLayout()
        self.quiet = qtw.QCheckBox('Output to file(s) directly', self)
        box.addWidget(self.quiet)
        if self.dest_from_input:
            self.quiet.setChecked(True)
        self.conf_quiet = qtw.QPushButton('Configure', self)
        self.conf_quiet.clicked.connect(self.configure_quiet)
        box.addWidget(self.conf_quiet)
        box.addStretch()
        self.grid.addLayout(box, self.row, 1)

        self.row += 1
        hbox = qtw.QHBoxLayout()
        hbox.addStretch(1)
        self.b_doit = qtw.QPushButton('&Uitvoeren', self)
        self.b_doit.clicked.connect(self.doe)
        hbox.addWidget(self.b_doit)
        self.b_cancel = qtw.QPushButton('&Einde', self)
        self.b_cancel.clicked.connect(self.close)
        hbox.addWidget(self.b_cancel)
        hbox.addStretch(1)
        self.grid.addLayout(hbox, self.row, 0, 1, 2)

        vbox = qtw.QVBoxLayout()
        vbox.addLayout(self.grid)

        self.setLayout(vbox)
        ## self.resize(250, 150)
        self.use_pylint.setFocus()

        self.show()
        sys.exit(app.exec_())

    def add_combobox_row(self, labeltext, itemlist, initial='', button=None):
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

    def add_checkbox_row(self, text, toggler=None, spinner=None):
        self.row += 1
        chk = qtw.QCheckBox(text, self)
        if toggler:
            chk.toggle()
        if spinner:
            box = qtw.QHBoxLayout()
            box.addWidget(chk)
            box.addWidget(spinner)
            box.addStretch()
            self.grid.addLayout(box, self.row, 1)
        else:
            self.grid.addWidget(chk, self.row, 1)
        return chk

    def check_case(self, inp):
        """autocompletion voor zoektekst in overeenstemming brengen met case
        indicator"""
        if inp == core.Qt.Checked:
            new_value = core.Qt.CaseSensitive
        else:
            new_value = core.Qt.CaseInsensitive
        self.vraag_zoek.setAutoCompletionCaseSensitivity(new_value)

    def keyPressEvent(self, event):
        """event handler voor toetsaanslagen"""
        if event.key() == core.Qt.Key_Escape:
            self.close()

    def determine_common(self):
        if self.mode == Mode.single.value:
            test = self.input
        elif self.mode == Mode.multi.value:
            test = os.path.commonprefix(self.input)
            if test in self.input:
                pass
            else:
                while test and not os.path.exists(test):
                    test = test[:-1]
        else:
            test = self.p["pad"] + os.sep
        return test

    def doe(self):
        """Zoekactie uitvoeren en resultaatscherm tonen"""
        test = self.linters.checkedButton() or ''
        if test: test = test.text()
        mld = self.check_linter(test)
        if not mld and self.mode == Mode.standard.value:
            mld = self.checkpath(str(self.vraag_dir.currentText()))
        if not mld:
            if self.mode != Mode.single.value or os.path.isdir(self.input):
                self.checksubs(self.vraag_subs.isChecked(),
                               self.vraag_links.isChecked(), self.vraag_diepte.value())
            elif self.mode == Mode.single.value and os.path.islink(self.input):
                self.p["follow_symlinks"] = True
        if not mld and self.quiet.isChecked():
            mld = self.check_quiet_options()
        if mld:
            qtw.QMessageBox.critical(self, self.fouttitel, mld, qtw.QMessageBox.Ok)
            return

        self.p["fallback_encoding"] = self._fallback_encoding
        self.schrijfini()
        self.zoekvervang = Linter(**self.p)
        if not self.zoekvervang.ok:
            msg = '\n'.join(self.zoekvervang.rpt)
            qtw.QMessageBox.information(self, self.resulttitel, msg,
                                        qtw.QMessageBox.Ok)
            return

        if not self.zoekvervang.filenames:
            qtw.QMessageBox.information(self, self.resulttitel, "Geen bestanden gevonden",
                                        qtw.QMessageBox.Ok)
            return

        common_part = self.determine_common()
        if self.apptype == "single" or (
                len(self.fnames) == 1 and os.path.isfile(self.fnames[0])):
            pass
        else:
            ## print(self.skipdirs_overslaan, self.skipfiles_overslaan)
            go_on = self.ask_skipdirs.isChecked() or self.ask_skipfiles.isChecked()
            canceled = False
            while go_on:
                if self.ask_skipdirs.isChecked():
                    # eerste ronde: toon directories
                    if self.zoekvervang.dirnames:
                        self.names = sorted(self.zoekvervang.dirnames)
                        dlg = SelectNames(self, files=False).exec_()
                        if dlg == qtw.QDialog.Rejected:
                            canceled = True
                            break
                        # tweede ronde: toon de files die overblijven
                        fnames = self.zoekvervang.filenames[:]
                        for fname in fnames:
                            for name in self.names:
                                if fname.startswith(name + '/'):
                                    self.zoekvervang.filenames.remove(fname)
                                    break
                        if not self.ask_skipfiles.isChecked():
                            go_on = False
                    log(self.zoekvervang.filenames)
                if self.ask_skipfiles.isChecked():
                    self.names = sorted(self.zoekvervang.filenames)
                    dlg = SelectNames(self).exec_()
                    if dlg == qtw.QDialog.Rejected and not self.ask_skipdirs.isChecked():
                        canceled = True
                        break
                    if dlg == qtw.QDialog.Accepted:
                        self.zoekvervang.filenames = self.names
                        go_on = False
            if canceled:
                return

        self.zoekvervang.do_action(search_python=self.p["context"])
        if len(self.zoekvervang.rpt) == 1:
            qtw.QMessageBox.information(self, self.resulttitel, "Niks gevonden",
                                        qtw.QMessageBox.Ok)
        else:
            dlg = Results(self, common_part)
        if self.vraag_exit.isChecked() and self.p["vervang"] is not None:
            self.close()

    def zoekdir(self):
        """event handler voor 'zoek in directory'"""
        dlg = qtw.QFileDialog.getExistingDirectory(self, "Choose a directory:",
                                                   self.vraag_dir.currentText())
        if dlg:
            self.vraag_dir.setEditText(dlg)

    def configure_pylint(self):
        """open pylint configuration in editor
        """
        self.edit_conf(os.path.join(os.path.expanduser('~'), '.pylintrc'))

    def configure_flake8(self):
        self.edit_conf(os.path.join(os.path.expanduser('~'), '.config', 'flake8'))

    def edit_conf(self, conf):
        subprocess.run(['xdg-open', conf])

    def configure_quiet(self):
        dlg = QuietOptions(self).exec_()
        if dlg == qtw.QDialog.Accepted:
            "update config"  # TODO
