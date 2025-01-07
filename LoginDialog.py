import hashlib
from LoggingHandler import Logger
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox,
)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


USER_LOGIN = "admin"
USER_PASSWORD_HASH = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Logowanie")
        self.setModal(True)
        self.logger = Logger()

        layout = QVBoxLayout()

        self.password_label = QLabel("Hasło:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Wprowadź hasło")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Zaloguj")
        self.login_button.clicked.connect(self.handle_login)

        self.password_input.returnPressed.connect(self.handle_login)

        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def handle_login(self):
        password = self.password_input.text().strip()

        if hash_password(password) == USER_PASSWORD_HASH:
            QMessageBox.information(self, "Sukces", "Logowanie powiodło się!")
            self.logger.log_info("Użytkownik zalogował się poprawnie.")
            self.accept()
        else:
            QMessageBox.warning(self, "Błąd", "Niepoprawne dane logowania.")
            self.logger.log_info("Nieudana próba logowania.")
            self.password_input.clear()
