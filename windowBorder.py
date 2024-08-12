
from PySide6.QtCore import (Qt,
                            QPoint,
                            QSize,
                            QRect,
                            QPropertyAnimation,
                            QParallelAnimationGroup)
from PySide6.QtGui import (QIcon,
                           QPixmap,
                           QCursor)
from PySide6.QtWidgets import (QMainWindow,
                               QWidget,
                               QPushButton,
                               QLabel)
from customizeWindow import CustomizeWindow


class WindowBorder(QMainWindow):
    def __init__(self, parent: QWidget = None, Min: tuple[int, int] = (800, 450)):
        super(WindowBorder, self).__init__(parent=parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.Min = Min
        self.setBody()

    def setBody(self):
        self.__setGlass()
        self.body = CustomizeWindow(self, title="FramelessWindow 示例", icon=QIcon("icon.png"),
                                    MinimumSize=QSize(self.Min[0], self.Min[1]))

    def showNormal(self):
        self.showMaximized()

    def showFullScreen(self):
        self.showMaximized()

    def __setGlass(self):
        self.glass = QPushButton(self)
        self.glass.setStyleSheet("QPushButton {"
                                 "background-color:rgba(240,240,240,0.7);"
                                 "border:rgb(125,125,125);"
                                 "}")
        self.glass.setGeometry(-10, -10, 0, 0)

    def __is_glass_closed(self) -> bool:
        if (self.glass.size().width() == 0 and
                self.glass.size().height() == 0 and
                self.glass.pos().x() == -10 and
                self.glass.pos().y() == -10):
            return True
        else:
            return False

    def __glass_setGeo(self, geo: QRect, event: object = None):
        if self.__is_glass_closed():
            self.glass.move(QCursor.pos())
        self.am0 = QPropertyAnimation(self.glass, b'geometry')
        self.am0.setDuration(100)
        self.am0.setStartValue(self.geometry())
        self.am0.setEndValue(geo)
        if event is not None:
            self.am0.finished.connect(event)

    # def
