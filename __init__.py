from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from windowBorder import WindowBorder
from sys import argv
from sys import exit as sys_exit

app = QApplication(argv)
window = WindowBorder(MinimumSize=QSize(100, 70), title="123", icon=QIcon("icon.png"))
sys_exit(app.exec())
