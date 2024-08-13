from PySide6.QtCore import (Qt,
                            QPoint,
                            QSize,
                            QRect,
                            QPropertyAnimation,
                            QParallelAnimationGroup)
from PySide6.QtGui import (QIcon,
                           QPixmap,
                           QCursor, QGuiApplication)
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
                                 "background-color:rgba(240,240,240,0.5);"
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

    def __glass_setGeo(self, geo: QRect):
        if self.__is_glass_closed():
            self.am0 = QPropertyAnimation(self.glass, b'geometry')
            self.am0.setDuration(50)
            self.am0.setStartValue(QRect(QCursor.pos().x(), QCursor.pos().y(), 0, 0))
            self.am0.setEndValue(geo)
            self.am0.start()
        def event():
            self.ag1.stop()
            self.ag1.clear()
        self.ag1 = QParallelAnimationGroup(self)
        self.am0 = QPropertyAnimation(self.glass, b'geometry')
        self.am0.setDuration(50)
        self.am0.setStartValue(self.glass.geometry())
        self.am0.setEndValue(geo)
        self.ag1.addAnimation(self.am0)
        self.ag1.finished.connect(event)
        self.ag1.start()

    def will_full_right(self):
        self.__glass_setGeo(QRect(QGuiApplication.primaryScreen().size().width() // 2, 0,
                                  QGuiApplication.primaryScreen().size().width() // 2,
                                  (QGuiApplication.primaryScreen().size().height() - self.body.taskbar_height)))

    def will_full_left(self):
        self.__glass_setGeo(QRect(0, 0,
                                  QGuiApplication.primaryScreen().size().width() // 2,
                                  (QGuiApplication.primaryScreen().size().height() - self.body.taskbar_height)))

    def will_up_left(self):
        self.__glass_setGeo(QRect(0, 0,
                                  QGuiApplication.primaryScreen().size().width() // 2,
                                  (QGuiApplication.primaryScreen().size().height() - self.body.taskbar_height) // 2))

    def will_down_left(self):
        self.__glass_setGeo(QRect(0, (QGuiApplication.primaryScreen().size().height() - self.body.taskbar_height) // 2,
                                  QGuiApplication.primaryScreen().size().width() // 2,
                                  (QGuiApplication.primaryScreen().size().height() - self.body.taskbar_height) // 2))

    def will_up_right(self):
        self.__glass_setGeo(QRect(QGuiApplication.primaryScreen().size().width() // 2, 0,
                                  QGuiApplication.primaryScreen().size().width() // 2,
                                  (QGuiApplication.primaryScreen().size().height() - self.body.taskbar_height) // 2))

    def will_down_right(self):
        self.__glass_setGeo(QRect(QGuiApplication.primaryScreen().size().width() // 2,
                                  (QGuiApplication.primaryScreen().size().height() - self.body.taskbar_height) // 2,
                                  QGuiApplication.primaryScreen().size().width() // 2,
                                  (QGuiApplication.primaryScreen().size().height() - self.body.taskbar_height) // 2))

    def will_lined(self):
        self.__glass_setGeo(QRect(self.body.pos().x(), 0, self.body.size().width(),
                                  (QGuiApplication.primaryScreen().size().height() - self.body.taskbar_height)))

    def will_max(self):
        self.__glass_setGeo(QRect(0, 0, QGuiApplication.primaryScreen().size().width(),
                                  (QGuiApplication.primaryScreen().size().height() - self.body.taskbar_height)))

    def will_close(self):
        def __clo():
            self.glass.setGeometry(-10, -10, 0, 0)
            self.glass.setWindowOpacity(0.5)
        __clo()