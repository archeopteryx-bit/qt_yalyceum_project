import sys
import sqlite3
import datetime as dt
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QLineEdit
from PyQt5.QtGui import QIcon


with open('colors.txt', mode='rt') as color_:
    color_ = color_.readlines()
    color_1 = color_[0][:color_[0].index(' ')]
    color_2 = color_[1][:color_[1].index(' ')]
    color_3 = color_[2][:color_[2].index(' ')]
    icons = color_[3][:color_[3].index(' ')]
    save = color_[4][:color_[4].index(' ')]
    sort_method = color_[5][:color_[5].index(' ')]
    sort_reverse = color_[6][:color_[6].index(' ')]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Notepad')
        uic.loadUi('Note.ui', self)
        self.search_frame.hide()
        self.menu_widget.hide()
        self.menu_button.clicked.connect(self.menu)
        self.plus_button.clicked.connect(self.add_note)
        self.open_search.clicked.connect(self.search_note)
        self.close_search.clicked.connect(self.search_note)
        self.settings.clicked.connect(self.open_setting)
        self.to_search.clicked.connect(self.searching)
        self.note_list.itemClicked.connect(self.open_note)
        self.list_()

    def list_(self):
        global sort_method, sort_reverse
        self.note_list.clear()
        con = sqlite3.connect('note_db.sqlite')
        cur = con.cursor()
        result = cur.execute(f"""
                        SELECT heading, {sort_method}
                        FROM notes""").fetchall()
        how_to_sort = sorted(result, key=lambda x: x[1], reverse=bool(sort_reverse))
        con.close()
        for elem in how_to_sort:
            self.note_list.addItem(elem[0])

    def open_note(self):
        edit_note.editnote()

    def menu(self):
        if self.menu_widget.isHidden():
            self.menu_widget.show()
        elif not self.menu_widget.isHidden():
            self.menu_widget.hide()

    def add_note(self):
        self.menu_widget.hide()
        ex.setVisible(False)
        new_note.show()

    def search_note(self):
        if self.sender() == self.open_search:
            self.search_frame.show()
            self.menu_widget.hide()
        elif self.sender() == self.close_search:
            self.search_frame.hide()

    def searching(self):
        ex.note_list.clear()
        con = sqlite3.connect('note_db.sqlite')
        cur = con.cursor()
        result = cur.execute(f"""
                        SELECT heading
                        FROM notes
                        WHERE note LIKE '%{self.search.text()}%' OR heading LIKE '%{self.search.text()}%'
                        """).fetchall()
        con.close()
        for elem in result:
            ex.note_list.addItem(elem[0])

    def open_setting(self):
        ex.setVisible(False)
        sett.show()


class Note(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('Plus_Note.ui', self)
        self.back.clicked.connect(self.close_note)
        self.save_button.clicked.connect(self.savenote)
        self.delete_2.clicked.connect(self.delete)
        self.warning.hide()

    def already_have(self):
        con = sqlite3.connect('note_db.sqlite')
        cur = con.cursor()
        note = cur.execute(f"""
                        SELECT heading
                        FROM notes
                        WHERE heading = (?)""", (self.heading.text(),)).fetchall()
        con.close()
        if len(note) == 0:
            return True
        return False

    def close_note(self):
        global save
        new_note.close()
        ex.setVisible(True)
        if save == 'True' and self.heading.text() != '':
            self.savenote()
        self.heading.setText('')
        self.noteEdit.setPlainText('')
        self.warning.hide()
        ex.list_()

    def savenote(self):
        if self.already_have():
            if self.heading.text() != '':
                if self.noteEdit.toPlainText() == '':
                    self.noteEdit.setPlainText(' ')
                con = sqlite3.connect('note_db.sqlite')
                cur = con.cursor()
                cur.execute(f"""INSERT INTO notes
                            VALUES (?,?,?,?)""",
                            (self.heading.text(), self.noteEdit.toPlainText(),
                             dt.datetime.today(), dt.datetime.today()))
                con.commit()
                con.close()
        else:
            self.warning.show()

    def delete(self):
        new_note.close()
        ex.setVisible(True)
        self.heading.setText('')
        self.noteEdit.setPlainText('')
        self.warning.hide()
        ex.list_()


class EditNote(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('Plus_Note.ui', self)
        self.back.clicked.connect(self.close_note)
        self.save_button.clicked.connect(self.savenote)
        self.delete_2.clicked.connect(self.delete)
        self.warning.hide()

    def already_have(self):
        con = sqlite3.connect('note_db.sqlite')
        cur = con.cursor()
        note = cur.execute(f"""
                        SELECT heading
                        FROM notes
                        WHERE heading = (?)""", (self.heading.text(),)).fetchall()
        con.close()
        if len(note) == 0 or self.heading.text() == ex.note_list.currentItem().text():
            return True
        return False

    def close_note(self):
        global save
        edit_note.close()
        ex.setVisible(True)
        if save == 'True' and self.heading.text() != '':
            self.savenote()
        self.heading.setText('')
        self.noteEdit.setPlainText('')
        self.warning.hide()
        ex.list_()

    def savenote(self):
        try:
            if self.already_have():
                self.warning.hide()
                con = sqlite3.connect('note_db.sqlite')
                cur = con.cursor()
                note = cur.execute(f"""SELECT create_time
                                        FROM notes
                                        WHERE heading = (?)""", (self.heading.text(),)).fetchall()
                cur.execute(f"""DELETE FROM notes
                            WHERE heading = (?)""", (ex.note_list.currentItem().text(),))
                cur.execute(f"""INSERT INTO notes
                            VALUES (?,?,?,?)""",
                            (self.heading.text(), self.noteEdit.toPlainText(),
                             note[0][0], dt.datetime.today()))
                con.commit()
                con.close()
            else:
                self.warning.show()
        except Exception as e:
            print('Непредвиденная ошибка %s' % e)

    def editnote(self):
        ex.setVisible(False)
        edit_note.show()
        con = sqlite3.connect('note_db.sqlite')
        cur = con.cursor()
        note = cur.execute(f"""
                        SELECT heading, note
                        FROM notes
                        WHERE heading = (?)""",
                           (ex.note_list.currentItem().text(),)).fetchall()
        self.heading.setText(note[0][0])
        self.noteEdit.setPlainText(note[0][1])

    def delete(self):
        con = sqlite3.connect('note_db.sqlite')
        cur = con.cursor()
        cur.execute(f"""DELETE FROM notes
                    WHERE heading = (?)""", (ex.note_list.currentItem().text(),))
        con.commit()
        con.close()
        self.heading.setText('')
        self.noteEdit.setPlainText('')
        self.close()
        self.warning.hide()
        ex.setVisible(True)
        ex.list_()


class Settings(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('Settings.ui', self)
        self.dark_theme.clicked.connect(self.change_theme)
        self.light_theme.clicked.connect(self.change_theme)
        self.back.clicked.connect(self.close_setting)
        self.password_button.clicked.connect(self.password)
        self.delpassword_button.clicked.connect(self.password)
        self.autosave_btn.clicked.connect(self.on_off_save)
        self.increases.clicked.connect(self.order)
        self.decrease.clicked.connect(self.order)
        self.create_time.clicked.connect(self.sigh_sort)
        self.edit_time.clicked.connect(self.sigh_sort)
        self.heading.clicked.connect(self.sigh_sort)
        self.passworded()

    def passworded(self):
        with open('psw.txt', mode='rt') as psw_r:
            psw_r = psw_r.readline()
        if len(psw_r) == 1:
            self.delpassword_button.hide()
            self.password_button.show()
        elif len(psw_r) > 1:
            self.password_button.hide()
            self.delpassword_button.show()

    def change_theme(self):
        global color_1, color_2, color_3, icons
        if self.sender() == self.light_theme:
            color_1 = '#FFB841'
            color_2 = '#FFDB9E'
            color_3 = '#000000'
            icons = '(light)'
        elif self.sender() == self.dark_theme:
            color_1 = '#0A0A0A'
            color_2 = '#141414'
            color_3 = '#FFFFFF'
            icons = ''
        save_changes()
        theme()

    def on_off_save(self):
        global save
        if self.autosave_btn.isChecked():
            save = 'True'
        else:
            save = 'False'
        save_changes()

    def password(self):
        if self.sender() == self.password_button:
            psw_.show()
        else:
            psw_2.show()

    def order(self):
        global sort_reverse
        if self.sender() == self.increases:
            sort_reverse = ''
        elif self.sender() == self.decrease:
            sort_reverse = 'reverse '
        save_changes()
        ex.list_()

    def sigh_sort(self):
        global sort_method
        if self.sender() == self.create_time:
            sort_method = 'create_time'
        elif self.sender() == self.edit_time:
            sort_method = 'edit_time'
        elif self.sender() == self.heading:
            sort_method = 'heading'
        save_changes()
        ex.list_()

    def close_setting(self):
        sett.close()
        ex.setVisible(True)


class Dlg(QDialog):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('SetPassword.ui', self)
        self.password_error_label.hide()
        self.ok.clicked.connect(self.set_password)
        self.cancel.clicked.connect(self.close_)
        self.see_psw.clicked.connect(self.ech_mode)
        self.not_see_psw.clicked.connect(self.ech_mode)
        self.not_see_psw.show()

    def ech_mode(self):
        if self.sender() == self.not_see_psw:
            self.first_line.setEchoMode(QLineEdit.Normal)
            self.not_see_psw.hide()
        else:
            self.first_line.setEchoMode(QLineEdit.Password)
            self.not_see_psw.show()

    def set_password(self):
        if self.first_line.text() == self.second_line.text():
            with open('psw.txt', mode='wt') as psw_w:
                psw_w.write('.' + self.first_line.text())
            sett.passworded()
            self.close()
        else:
            self.password_error_label.setText('Введённые пароли не совпадают.')
            self.password_error_label.show()

    def close_(self):
        self.close()

    def closeEvent(self, event):
        self.first_line.setText('')
        self.second_line.setText('')
        self.password_error_label.hide()
        event.accept()


class Dlg2(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('Password.ui', self)
        self.password_error_label.hide()
        self.cancel.setText('Выход')
        self.ok.clicked.connect(self.delete_password)
        self.cancel.clicked.connect(self.close_)
        self.see_psw.clicked.connect(self.ech_mode)
        self.not_see_psw.clicked.connect(self.ech_mode)
        self.not_see_psw.show()

    def ech_mode(self):
        if self.sender() == self.not_see_psw:
            self.first_line.setEchoMode(QLineEdit.Normal)
            self.not_see_psw.hide()
        else:
            self.first_line.setEchoMode(QLineEdit.Password)
            self.not_see_psw.show()

    def delete_password(self):
        with open('psw.txt', mode='rt') as psw_r:
            psw_r = psw_r.readline()[1:]
        if self.first_line.text() == psw_r.rstrip():
            with open('psw.txt', mode='wt') as psw_w:
                psw_w.write('.')
            sett.passworded()
            self.close()
        else:
            self.password_error_label.setText('Введён неправильный пароль.')
            self.password_error_label.show()

    def close_(self):
        self.close()

    def closeEvent(self, event):
        self.first_line.setText('')
        self.password_error_label.hide()
        event.accept()


class CheckPassword(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('Password.ui', self)
        self.password_error_label.hide()
        self.ok.clicked.connect(check_password)
        self.cancel.clicked.connect(self.close_)
        self.see_psw.clicked.connect(self.ech_mode)
        self.not_see_psw.clicked.connect(self.ech_mode)
        self.not_see_psw.show()

    def ech_mode(self):
        if self.sender() == self.not_see_psw:
            self.first_line.setEchoMode(QLineEdit.Normal)
            self.not_see_psw.hide()
        else:
            self.first_line.setEchoMode(QLineEdit.Password)
            self.not_see_psw.show()

    def close_(self):
        self.close()


def save_changes():
    with open('colors.txt', mode='wt') as color_:
        color_.write(f'{color_1} - color for frame.\n'
                     f'{color_2} - color for other.\n'
                     f'{color_3} - color for font.\n'
                     f'{icons} - icons.\n'
                     f'{save} - autosave.\n'
                     f'{sort_method} - sort.\n'
                     f'{sort_reverse} - revers sort.')


def theme():
    r, l = '{', '}'

    ex.menu_button.setIcon(QIcon('Sprites' + icons + '/menu1.png'))
    ex.settings.setIcon(QIcon('Sprites' + icons + '/sett.png'))
    ex.plus_button.setIcon(QIcon('Sprites' + icons + '/plus.png'))
    ex.close_search.setIcon(QIcon('Sprites' + icons + '/close_search.png'))
    ex.open_search.setIcon(QIcon('Sprites' + icons + '/search.png'))
    ex.to_search.setIcon(QIcon('Sprites' + icons + '/search.png'))
    new_note.back.setIcon(QIcon('Sprites' + icons + '/back.png'))
    new_note.delete_2.setIcon(QIcon('Sprites' + icons + '/basket.png'))
    new_note.save_button.setIcon(QIcon('Sprites' + icons + '/save.png'))
    edit_note.back.setIcon(QIcon('Sprites' + icons + '/back.png'))
    edit_note.delete_2.setIcon(QIcon('Sprites' + icons + '/basket.png'))
    edit_note.save_button.setIcon(QIcon('Sprites' + icons + '/save.png'))
    sett.delpassword_button.setIcon(QIcon('Sprites' + icons + '/open_lock.png'))
    sett.password_button.setIcon(QIcon('Sprites' + icons + '/lock.png'))
    sett.back.setIcon(QIcon('Sprites' + icons + '/back.png'))
    psw_.not_see_psw.setIcon(QIcon('Sprites' + icons + '/close_eye.png'))
    psw_.see_psw.setIcon(QIcon('Sprites' + icons + '/eye.png'))
    psw_2.not_see_psw.setIcon(QIcon('Sprites' + icons + '/close_eye.png'))
    psw_2.see_psw.setIcon(QIcon('Sprites' + icons + '/eye.png'))
    chk.see_psw.setIcon(QIcon('Sprites' + icons + '/eye.png'))
    chk.not_see_psw.setIcon(QIcon('Sprites' + icons + '/close_eye.png'))

    ex.setStyleSheet(f"""
            QMainWindow{r}
                background-color: {color_2};
            {l}
    """)
    ex.note_list.setStyleSheet(f"""
                    QWidget{r}
                        background-color: {color_2};
                        color: {color_3};
                    {l}
    """)
    ex.centralwidget.setStyleSheet(f"""
                    QWidget{r}
                        background-color: {color_2};
                    {l}
    """)
    ex.frame.setStyleSheet(f"""
                    QFrame{r}
                        background-color: {color_1};
                    {l}
    """)
    ex.menu_button.setStyleSheet(f"""
                    QPushButton{r}
                        background-color: {color_1};
                    {l}
    """)
    ex.open_search.setStyleSheet(f"""
                    QPushButton{r}
                        background-color: {color_1};
                        color: {color_3};
                    {l}
    """)
    ex.plus_button.setStyleSheet(f"""
                    QPushButton{r}
                        background-color: {color_1};
                    {l}
    """)
    ex.search_frame.setStyleSheet(f"""
                    QFrame{r}
                        background-color: {color_1};
                    {l}
    """)
    ex.close_search.setStyleSheet(f"""
                    QPushButton{r}
                        background-color: {color_1};
                    {l}
    """)
    ex.search.setStyleSheet(f"""
                    QLineEdit{r}
                        background-color: {color_1};
                        color: {color_3};
                    {l}
    """)
    ex.menu_widget.setStyleSheet(f"""
                    QWidget{r}
                        background-color: {color_1};
                    {l}
    """)
    ex.settings.setStyleSheet(f"""
                    QPushButton{r}
                        color: {color_3}
                    {l}
    """)
    ex.label_3.setStyleSheet(f"""
                    QLabel{r}
                        color: {color_3}
                    {l}
    """)

    new_note.setStyleSheet(f"""
                    QWidget{r}
                        background-color: {color_2};
                    {l}
    """)
    new_note.frame.setStyleSheet(f"""
                    QFrame{r}
                        background-color: {color_1};
                    {l}
    """)
    new_note.back.setStyleSheet(f"""
                    QPushButton{r}
                        background-color: {color_1};
                    {l}
    """)
    new_note.noteEdit.setStyleSheet(f"""
                    QTextEdit{r}
                        background-color: {color_2};
                        color: {color_3};
                    {l}
    """)
    new_note.heading.setStyleSheet(f"""
                    QLineEdit{r}
                        background-color: {color_1};
                        color: {color_3};
                    {l}
    """)
    new_note.save_button.setStyleSheet(f"""
                    QPushButton{r}
                        background-color: {color_1};
                        color: {color_3};
                    {l}
    """)

    edit_note.setStyleSheet(f"""
                    QWidget{r}
                        background-color: {color_2};
                    {l}
    """)
    edit_note.frame.setStyleSheet(f"""
                    QFrame{r}
                        background-color: {color_1};
                    {l}
    """)
    edit_note.back.setStyleSheet(f"""
                    QPushButton{r}
                        background-color: {color_1};
                    {l}
    """)
    edit_note.noteEdit.setStyleSheet(f"""
                    QTextEdit{r}
                        background-color: {color_2};
                        color: {color_3};
                    {l}
    """)
    edit_note.heading.setStyleSheet(f"""
                    QLineEdit{r}
                        background-color: {color_1};
                        color: {color_3};
                    {l}
    """)
    edit_note.save_button.setStyleSheet(f"""
                    QPushButton{r}
                        background-color: {color_1};
                        color: {color_3};
                    {l}
    """)

    sett.setStyleSheet(f"""
                    QWidget{r}
                        background-color: {color_2};
                    {l}
                    Settings{r}
                        color: {color_1};
                    {l}
    """)
    sett.password_button.setStyleSheet(f"""
                QPushButton{r}
                    color: {color_3};
                {l}
    """)
    sett.delpassword_button.setStyleSheet(f"""
                QPushButton{r}
                    color: {color_3};
                {l}
    """)
    sett.frame.setStyleSheet(f"""
                    QFrame{r}
                        background-color: {color_1};
                        color: {color_3};
                    {l}
    """)
    sett.back.setStyleSheet(f"""
                    QPushButton{r}
                        background-color: {color_1};
                        color: {color_3};
                    {l}
    """)
    sett.theme_label.setStyleSheet(f"""
                    QLabel{r}
                        color: {color_3};
                    {l}
    """)
    sett.light_theme.setStyleSheet(f"""
                    QRadioButton{r}
                        color: {color_3};
                    {l}
    """)
    sett.dark_theme.setStyleSheet(f"""
                    QRadioButton{r}
                        color: {color_3};
                    {l}
    """)
    sett.autosave_btn.setStyleSheet(f"""
                    QCheckBox{r} 
                        color: {color_3};
                    {l}
    """)
    sett.sort_label.setStyleSheet(f"""
                    QLabel{r}
                        color: {color_3};
                    {l}
    """)
    sett.order_label.setStyleSheet(f"""
                    QLabel{r}
                        color: {color_3};
                    {l}
    """)
    sett.increases.setStyleSheet(f"""
                    QRadioButton{r}
                        color: {color_3};
                    {l}
    """)
    sett.decrease.setStyleSheet(f"""
                    QRadioButton{r}
                        color: {color_3};
                    {l}
    """)
    sett.sigh_label.setStyleSheet(f"""
                    QLabel{r}
                        color: {color_3};
                    {l}
    """)
    sett.create_time.setStyleSheet(f"""
                    QRadioButton{r}
                        color: {color_3};
                    {l}
    """)
    sett.edit_time.setStyleSheet(f"""
                    QRadioButton{r}
                        color: {color_3};
                    {l}
    """)
    sett.heading.setStyleSheet(f"""
                    QRadioButton{r}
                        color: {color_3};
                    {l}
    """)

    psw_.setStyleSheet(f"""
                    QDialog{r}
                        background-color: {color_2};
                    {l}
    """)
    psw_.first_line.setStyleSheet(f"""
                    QLineEdit{r}
                        background-color: {color_2};
                        color {color_3};
                    {l}
    """)
    psw_.second_line.setStyleSheet(f"""
                    QLineEdit{r}
                        background-color: {color_2};
                        color {color_3};
                    {l}
    """)
    psw_.ok.setStyleSheet(f"""
                    QPushButton{r}
                        background-color: {color_2};
                        color: {color_3};
                    {l}
    """)
    psw_.cancel.setStyleSheet(f"""
                    QPushButton{r}
                        background-color: {color_2};
                        color: {color_3};
                    {l}
    """)
    psw_.not_see_psw.setStyleSheet(f"""
                    QPushButton{r}
                        background-color: {color_2};
                    {l}
    """)
    psw_.see_psw.setStyleSheet(f"""
                    QPushButton{r}
                        background-color: {color_2};
                    {l}
    """)

    psw_2.setStyleSheet(f"""
                    QDialog{r}
                        background-color: {color_2};
                    {l}
    """)
    psw_2.first_line.setStyleSheet(f"""
                    QLineEdit{r}
                        background-color: {color_2};
                        color {color_3};
                    {l}
    """)
    psw_2.ok.setStyleSheet(f"""
                    QPushButton{r}
                        background-color: {color_2};
                        color: {color_3};
                    {l}
    """)
    psw_2.cancel.setStyleSheet(f"""
                    QPushButton{r}
                        background-color: {color_2};
                        color: {color_3};
                    {l}
    """)
    psw_2.not_see_psw.setStyleSheet(f"""
                    QPushButton{r}
                        background-color: {color_2};
                    {l}
    """)
    psw_2.see_psw.setStyleSheet(f"""
                    QPushButton{r}
                        background-color: {color_2};
                    {l}
    """)

    chk.setStyleSheet(f"""
                    QDialog{r}
                        background-color: {color_2};
                    {l}
    """)
    chk.first_line.setStyleSheet(f"""
                    QLineEdit{r}
                        background-color: {color_2};
                        color {color_3};
                    {l}
    """)
    chk.ok.setStyleSheet(f"""
                    QPushButton{r}
                        background-color: {color_2};
                        color: {color_3};
                    {l}
    """)
    chk.cancel.setStyleSheet(f"""
                    QPushButton{r}
                        background-color: {color_2};
                        color: {color_3};
                    {l}
    """)


def check():

    if color_1 == '#FFB841':
        sett.dark_theme.setChecked(False)
        sett.light_theme.setChecked(True)
    else:
        sett.light_theme.setChecked(False)
        sett.dark_theme.setChecked(True)

    if sort_reverse == 'reverse ':
        sett.increases.setChecked(True)
        sett.decrease.setChecked(False)
    else:
        sett.decrease.setChecked(True)
        sett.increases.setChecked(False)

    if sort_method == 'edit_time':
        sett.edit_time.setChecked(True)
        sett.create_time.setChecked(False)
        sett.heading.setChecked(False)
    elif sort_method == 'create_time':
        sett.create_time.setChecked(True)
        sett.edit_time.setChecked(False)
        sett.heading.setChecked(False)
    elif sort_method == 'heading':
        sett.heading.setChecked(True)
        sett.edit_time.setChecked(False)
        sett.create_time.setChecked(False)

    theme()


def check_password():
    with open('psw.txt', mode='rt') as psw_r:
        psw_r = psw_r.readline()[1:]
    if chk.first_line.text() == psw_r.rstrip():
        chk.close()
        ex.show()
    else:
        chk.password_error_label.setText('Введён неправильный пароль.')
        chk.password_error_label.show()
    if chk.sender() == chk.cancel:
        ex.close()


def if_passworded():
    with open('psw.txt', mode='rt') as psw_r:
        psw_r = psw_r.readline()
    if len(psw_r) != 1:
        chk.show()
    else:
        ex.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    new_note = Note()
    edit_note = EditNote()
    sett = Settings()
    psw_ = Dlg()
    psw_2 = Dlg2()
    chk = CheckPassword()
    check()
    if_passworded()
    sys.exit(app.exec())
