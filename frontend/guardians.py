from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton)
from backend import initializers, windows_util
import pyautogui
import win32con
import win32gui
#temporary consts
TITLE = "Sect v0.0.1"


class Guardians(QMainWindow):
    def __init__(self):
        super().__init__()
        self.game_res = initializers.resolutions.get("Roblox")
        self.mainWindow()
        self.layout = QVBoxLayout()
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        self.initLabels()
        self.initWindow()

    def mainWindow(self):
        self.res = windows_util.resolutionMid()
        self.setGeometry(self.res[0], self.res[1], (self.game_res[0] + 200), (self.game_res[1] + 200))
        self.setWindowTitle(TITLE)
        self.setStyleSheet("background-color: #1b1b1f;")

    def initLabels(self):
        title = QLabel("Anime Guardians")
        title.setStyleSheet("font-size: 25px;" \
                            "font-family: Times New Roman;"
                            "font-weight: bold;"
                            "color: white")
        self.layout.addWidget(title, alignment=Qt.AlignLeft | Qt.AlignTop)
    
    def initWindow(self):
        self.hwnd = windows_util.initWindow("Roblox")
        self.container = QWidget(self)
        win32gui.SetParent(self.hwnd, int(self.container.winId())) # set qt window as parent application and roblox as child, so if user decides to move qt application roblox also moves
        self.layout.addWidget(self.container)
        self.initAttachWindow()

    def initAttachWindow(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE) #Grabs HWND and uses SW_RESTORE to prevent minimization
        game_width = self.game_res[0]
        game_height = self.game_res[1]
        self.container.setFixedSize(game_width, game_height)
        x_coord, y_coord = windows_util.resolutionMid(game_width, game_height)
        win32gui.MoveWindow(self.hwnd, x_coord, y_coord, game_width, game_height, True) #Makes sure 800x600 is constant. Grabs x and y from rect
        self.coordinates = (self.res[0], self.res[1], self.game_res[0], self.game_res[1])
        return self.coordinates