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
    def __init__(self, parent: QWidget | None = None,
                 taskbar_height: int = 45,
                 MinimumSize: QSize = QSize(400, 225),
                 ReSize: QSize = QSize(400, 225),
                 Position: QPoint | None = None,
                 title_height: int = 35,
                 title_font_size: int = 15,
                 icon: QIcon = None,
                 title: str = "",
                 background_color_rgba: tuple[int, int, int, int] | list[int] | set[int] = (230, 230, 230, 1),
                 title_background_color_rgba: tuple[int, int, int, int] | list[int] | set[int] = (0, 0, 0, 0.8),
                 title_text_color_rgba: tuple[int, int, int, int] | list[int] | set[int] = (255, 255, 255, 1),
                 button_hoverColor: tuple[int, int, int, int] | list[int] | set[int] = (100, 100, 100, 1),
                 closeButton_hoverColor: tuple[int, int, int, int] | list[int] | set[int] = (255, 0, 0, 1),
                 glass_color_rgba: tuple[int, int, int, int] | list[int] | set[int] = (240, 240, 240, 0.5),
                 glass_border_color_rgb: tuple[int, int, int] | list[int] | set[int] = (125, 125, 125)):
        super(WindowBorder, self).__init__(parent=parent)
        self.setWindowFlags(Qt.WindowType.Window |
                            Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.WindowSystemMenuHint |
                            Qt.WindowType.WindowMinimizeButtonHint |
                            Qt.WindowType.WindowMaximizeButtonHint |
                            Qt.WindowType.WindowCloseButtonHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.glass_color_rgba = glass_color_rgba
        self.glass_border_color_rgb = glass_border_color_rgb
        self.Min = MinimumSize
        self.__setGlass()
        self.body = CustomizeWindow(parent=self,
                                    taskbar_height=taskbar_height,
                                    MinimumSize=MinimumSize,
                                    ReSize=ReSize,
                                    Position=Position,
                                    title_height=title_height,
                                    title_font_size=title_font_size,
                                    icon=icon,
                                    title=title,
                                    background_color_rgba=background_color_rgba,
                                    title_background_color_rgba=title_background_color_rgba,
                                    title_text_color_rgba=title_text_color_rgba,
                                    button_hoverColor=button_hoverColor,
                                    closeButton_hoverColor=closeButton_hoverColor)
        super(WindowBorder, self).show()

    def showNormal(self):
        self.showMaximized()

    def showFullScreen(self):
        self.showMaximized()

    def showMinimized(self):
        if self.isMinimized():
            self.showMaximized()
            self.body.show()
        else:
            self.body.showMinimized()

    def showMin(self):
        super().showMinimized()

    def show(self):
        if self.isMinimized():
            self.showMaximized()
            self.body.show()
        else:
            self.body.showMinimized()

    def __setGlass(self):
        self.glass = QPushButton(self)
        self.glass.setStyleSheet("QPushButton {"
                                 f"background-color:rgba({self.glass_color_rgba[0]}, {self.glass_color_rgba[1]}, {self.glass_color_rgba[2]}, {self.glass_color_rgba[3]});"
                                 f"border:rgb({self.glass_border_color_rgb[0]}, {self.glass_border_color_rgb[1]}, {self.glass_border_color_rgb[2]});"
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

    def will_normal(self):
        self.__glass_setGeo(self.body.normal_geometry)

    def will_center(self):
        self.__glass_setGeo(QRect(((self.body.__screen__ - self.body.size()).width()) // 2,
                                  (
                                              self.body.__screen__.height() - self.body.size().height() - self.body.taskbar_height) // 2,
                                  self.body.size().width(), self.body.size().height()))
