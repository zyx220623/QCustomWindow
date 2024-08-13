from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from windowBorder import WindowBorder
from sys import argv
from sys import exit as sys_exit

app = QApplication(argv)
window = WindowBorder(Min=(400,225))
window.showreal()
sys_exit(app.exec())