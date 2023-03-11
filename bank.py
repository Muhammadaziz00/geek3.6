from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QListWidget
from PyQt5.uic import loadUi
import sys
import sqlite3
import time

class StartDB:
    def __init__(self):
        self.connect = sqlite3.connect('bank.db')
        self.connect.execute("""
            CREATE TABLE IF NOT EXISTS users(
            login VARCHAR(255),
            password VARCHAR(255),
            email VARCHAR(255),
            created VARCHAR(100)
            );
        """)
        self.connect.commit()

class SignUp(QWidget):
    def __init__(self, user_list):
        super(SignUp, self).__init__()
        loadUi('untitled2.ui', self)
        self.hide_error()
        self.db = StartDB()
        self.user_list = user_list
        self.signup.clicked.connect(self.register)

    def hide_error(self):
        self.error.hide()

    def show_error(self):
        self.error.show()

    def register(self):
        login = self.login.text()
        password = self.password.text()
        email = self.email.text()
        cursor = self.db.connect.cursor()
        # Проверяем, что логин еще не зарегистрирован
        cursor.execute(f"SELECT COUNT(*) FROM users WHERE login='{login}'")
        count = cursor.fetchone()[0]
        if count > 0:
            self.show_error()
            self.error.setText("Пользователь уже зарегистрирован")
        else:
            self.show_error()
            cursor.execute(f"INSERT INTO users VALUES ('{login}', '{password}', '{email}', '{time.ctime()}');")
            self.db.connect.commit()
            self.user_list.addItem(login) # добавляем логин в список
            self.error.setText("Успешно")
        print(login, password, email)

class Bank(QMainWindow):
    def __init__(self):
        super(Bank, self).__init__()
        loadUi('untitled.ui', self)
        self.hide_error()
        self.signin.clicked.connect(self.check_login)
        self.user_list = QListWidget(self) # создаем список пользователей
        self.gridLayout.addWidget(self.user_list, 2, 1) # добавляем список на главное окно
        self.class_signup = SignUp(self.user_list) # передаем список в класс регистрации
        self.signup.clicked.connect(self.show_signup)

    def show_signup(self):
        self.class_signup.show()

    def hide_error(self):
        self.error.hide()

    def show_error(self):
        self.error.show()

    def check_login(self):
        login = self.login.text()
        password = self.password.text()
        if login == 'geeks' and password == 'geeks2023':
            self.show_error()
            self.error.setText("Ok")
        else:
            self.show_error()
            self.error.setText("Неправильные данные")

app = QApplication(sys.argv)
bank = Bank()
bank.show()
app.exec_()