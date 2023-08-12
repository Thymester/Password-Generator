import sys
import secrets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QCheckBox, QDesktopWidget

class PasswordGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Password Generator")

        # Calculate the window size based on 40% of screen resolution
        screen_geometry = QDesktopWidget().screenGeometry()
        self.width = int(screen_geometry.width() * 0.4)
        self.height = int(screen_geometry.height() * 0.4)

        # Calculate the window position to center the window
        self.move(screen_geometry.center() - self.rect().center())

        self.setGeometry(100, 100, self.width, self.height)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Applying dark mode style
        self.central_widget.setStyleSheet(
            """
            background-color: #333;
            color: #FFF;
            font-size: 14px;
            QLabel {
                color: #FFF;
            }
            QLineEdit {
                background-color: #444;
                color: #FFF;
                padding: 5px;
            }
            QPushButton {
                background-color: #007BFF;
                color: #FFF;
                border: none;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QCheckBox {
                color: #FFF;
            }
            """
        )

        self.password_label = QLabel("Generated Password:")
        self.password_line_edit = QLineEdit(self)
        self.password_line_edit.setReadOnly(True)

        self.length_label = QLabel("Password Length:")
        self.length_input = QLineEdit(self)
        self.length_input.setText("16")  # Default password length

        self.special_chars_checkbox = QCheckBox("Include Special Characters")
        self.numbers_checkbox = QCheckBox("Include Numbers")
        
        # New checkbox to exclude certain special characters
        self.exclude_special_chars_checkbox = QCheckBox("Exclude Commonly Disallowed Special Characters")
        self.special_chars_checkbox.stateChanged.connect(self.special_chars_changed)

        self.generate_button = QPushButton("Generate Password")
        self.generate_button.clicked.connect(self.generate_password)

        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.copy_button.setEnabled(False)

        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_line_edit)
        self.layout.addWidget(self.length_label)
        self.layout.addWidget(self.length_input)
        self.layout.addWidget(self.special_chars_checkbox)
        self.layout.addWidget(self.numbers_checkbox)
        self.layout.addWidget(self.exclude_special_chars_checkbox)  # Add the new checkbox
        self.layout.addWidget(self.generate_button)
        self.layout.addWidget(self.copy_button)

        self.central_widget.setLayout(self.layout)

    def special_chars_changed(self):
        if self.special_chars_checkbox.isChecked():
            self.exclude_special_chars_checkbox.setChecked(False)

    def generate_password(self):
        password_length = int(self.length_input.text())
        password_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if self.special_chars_checkbox.isChecked():
            password_characters += "!@#$%^&*()-_=+[]{}|;:,.<>?/~"
        
        if self.numbers_checkbox.isChecked():
            password_characters += "0123456789"

        if self.exclude_special_chars_checkbox.isChecked():
            # Exclude commonly disallowed special characters
            password_characters = password_characters.replace("!@#$%^&*(){}[]|;:,.<>?/~", "")

        secure_random = secrets.SystemRandom()
        generated_password = ''.join(secure_random.choice(password_characters) for _ in range(password_length))
        self.password_line_edit.setText(generated_password)
        self.copy_button.setEnabled(True)
        self.password_label.setText("Generated Password:")

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.password_line_edit.text())
        self.password_label.setText("Password Copied to Clipboard!")

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Set Fusion style for a consistent look
    window = PasswordGeneratorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
