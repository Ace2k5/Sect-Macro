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
        self.game_res = windows_util.getWindowRes("Roblox")
        if self.game_res is None:
            print("Game resolution not found. Problem within initializers.py ")
            return
        self.hwnd = windows_util.initWindow("Roblox")
        self.mainWindow()
        self.layout = QVBoxLayout()
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        self.initLabels()
        self.initWindow()

    def mainWindow(self):
        window_width, window_height = self.game_res[0] + 200, self.game_res[1] + 200
        window_x, window_y = windows_util.resolutionMid(window_width, window_height)
        self.setGeometry(window_x, window_y, window_width, window_height)
        self.setWindowTitle("Sect v0.0.1")
        self.setStyleSheet("background-color: #1b1b1f;")

    def initLabels(self):
        title = QLabel("Anime Guardians")
        title.setStyleSheet("font-size: 25px;" \
                            "font-family: Times New Roman;"
                            "font-weight: bold;"
                            "color: white")
        self.layout.addWidget(title, alignment=Qt.AlignLeft | Qt.AlignTop)
    
    def initWindow(self):
        self.container = QWidget(self)
        win32gui.SetParent(self.hwnd, int(self.container.winId())) # set qt window as parent application and roblox as child, so if user decides to move qt application roblox also moves
        self.layout.addWidget(self.container)
        self.initAttachWindow()

    def initAttachWindow(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE) #Grabs HWND and uses SW_RESTORE to prevent minimization
        game_width = self.game_res[0]
        game_height = self.game_res[1]
        self.container.setFixedSize(game_width, game_height)
        win32gui.MoveWindow(self.hwnd, 0, 0, game_width, game_height, True) #Makes sure 800x600 is constant. Grabs x and y from rect, 0 0 because now roblox handle is a child