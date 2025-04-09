import sys
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from form_validation import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect buttons
        self.ui.btn_save.clicked.connect(self.save_data)
        self.ui.btn_clear.clicked.connect(self.clear_fields)

        # Shortcut to quit
        quit_shortcut = QShortcut(QKeySequence("Q"), self)
        quit_shortcut.activated.connect(self.close)

    def save_data(self):
        name = self.ui.input_name.text().strip()
        email = self.ui.input_email.text().strip()
        age = self.ui.input_age.text().strip()
        phone = self.ui.input_phone.text().strip()
        address = self.ui.input_address.toPlainText().strip()
        gender = self.ui.combo_gender.currentText()
        education = self.ui.combo_education.currentText()

        raw_phone = self.ui.input_phone.text()
        phone = raw_phone.replace(" ", "")

        # Cek field kosong
        empty_fields = [f for f in [name, email, age, phone, address] if not f]
        empty_dropdowns = []

        if gender == "":
            empty_dropdowns.append("gender")
        if education == "":
            empty_dropdowns.append("education")

        total_empty = len(empty_fields) + len(empty_dropdowns)

        if total_empty >= 2:
            self.show_warning("All fields are required.")
            return

        # Validasi per field
        # Validasi name
        if not name:
            self.show_warning("Name is required.")
            return

        # Validasi email
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.show_warning("Please enter a valid email.")
            return

        if email.endswith("@example.com"):
            self.show_warning("Email cannot use '@example.com' domain.")
            return

        # Validasi age
        if not age:
            self.show_warning("Age is required.")
            return

        if not age.isdigit():
            self.show_warning("Age must be a number.")
            return

        # Validasi phone number
        if not phone or phone == "+62 ":
            self.show_warning("Phone number is required.")
            return

        # Total panjang harus 14 karakter termasuk +62 → +62 + 11 digit = 14
        if len(phone) != 14:
            self.show_warning("Phone number must be exactly 13 digits.")
            return

        # Cek jika angka pertama setelah +62 bukan 0
        if phone.startswith("+620"):
            self.show_warning("Phone number must not start with 0 after '+62'.")
            return

        # Validasi address
        if not address:
            self.show_warning("Address is required.")
            return

        # Validasi gender
        if gender == "":
            self.show_warning("Please select a gender.")
            return

        # Validasi education
        if education == "":
            self.show_warning("Please select your education level.")
            return

        # Jika semua valid
        QMessageBox.information(self, "Success", "Data saved successfully!")
        self.clear_fields()

    def show_warning(self, message):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Warning!")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def clear_fields(self):
        self.ui.input_name.clear()
        self.ui.input_email.clear()
        self.ui.input_age.clear()
        self.ui.input_phone.clear()
        self.ui.input_address.clear()
        self.ui.combo_gender.setCurrentIndex(0)
        self.ui.combo_education.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
