import sys  # import sqlite3
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QLineEdit
from PyQt5.QtGui import QIcon, QFont
# from DataBase import *


with open('colors.txt', mode='rt') as color_:
    color_ = color_.readlines()
    color_1 = color_[0][:color_[0].index(' ')]
    color_2 = color_[1][:color_[1].index(' ')]
    color_3 = color_[2][:color_[2].index(' ')]
    icons = color_[3][:color_[3].index(' ')]
    save = color_[4][:color_[4].index(' ')]
no = ['<', '>', ':', '/', '\'', '|', '?', '*', '"']


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Notepad')
        uic.loadUi('Note.ui', self)
        self.search_frame.hide()
        self.menu_widget.hide()
        self.note_list.hide()
        self.menu_button.clicked.connect(self.menu)
        self.plus_button.clicked.connect(self.add_note)
        self.open_search.clicked.connect(self.search_note)
        self.close_search.clicked.connect(self.search_note)
        self.settings.clicked.connect(self.open_setting)
        self.note_list.itemClicked.connect(self.open_note)

    def open_note(self):
        print(self.a.currentItem().text())

    def menu(self):
        if self.menu_widget.isHidden():
            self.menu_widget.show()
        elif not self.menu_widget.isHidden():
            self.menu_widget.hide()

    def add_note(self):
        self.menu_widget.hide()
        ex.setVisible(False)
        new_note.show()

    def search_note(self):  # SQL3
        if self.sender() == self.open_search:
            self.search_frame.show()
            self.menu_widget.hide()
        elif self.sender() == self.close_search:
            self.search_frame.hide()
        text = self.search.text()

    def open_setting(self):
        ex.setVisible(False)
        sett.show()

    def open_basket(self):
        pass


class Note(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('Plus_Note.ui', self)
        self.back.clicked.connect(self.close_note)
        self.save_button.clicked.connect(self.savenote)

    def close_note(self):
        global save
        new_note.close()
        ex.setVisible(True)
        if save == 'True':
            self.savenote()
        self.heading.setText('')
        self.noteEdit.setPlainText('')

    def savenote(self):
        global no
        try:
            if self.heading.text() != '' or self.noteEdit.toPlainText() != '':
                name = self.heading.text()
                filename = f'{name}.txt'
                if filename in os.listdir("note"):
                    print('blin')
                    return
                with open(f'note/{filename}', mode='wt') as newfile:
                    newfile.write(self.heading.text() + '\n' + self.noteEdit.toPlainText())
                    self.note_list.addItem(self.heading.text())
        except Exception as e:
            print('Непредвиденная ошибка %s' % e)


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

    def close_setting(self):
        sett.close()
        ex.setVisible(True)


class Basket(QWidget):
    def __init__(self, *args):
        super().__init__()

    def restore(self):  # SQL3
        pass


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
                     f'{save} - autosave.')


def theme():
    r, l = '{', '}'

    ex.menu_button.setIcon(QIcon('Sprites' + icons + '/menu1.png'))
    ex.settings.setIcon(QIcon('Sprites' + icons + '/sett.png'))
    ex.plus_button.setIcon(QIcon('Sprites' + icons + '/plus.png'))
    ex.close_search.setIcon(QIcon('Sprites' + icons + '/close_search.png'))
    ex.basket_button.setIcon(QIcon('Sprites' + icons + '/basket.png'))
    new_note.back.setIcon(QIcon('Sprites' + icons + '/back.png'))
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
    ex.label_2.setStyleSheet(f"""
                    QLabel{r}
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
    new_note.extr.setStyleSheet(f"""
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
    sett = Settings()
    psw_ = Dlg()
    psw_2 = Dlg2()
    chk = CheckPassword()
    check()
    if_passworded()
    sys.exit(app.exec())
