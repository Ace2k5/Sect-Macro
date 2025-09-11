from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton)
from backend import initializers
import pyautogui
import win32con
import win32gui

class Guardians(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainWindow()
        self.layout = QVBoxLayout()
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        self.initLabels()
        self.initWindow()

    def mainWindow(self):
        self.screen_res = pyautogui.size()
        self.game_res = initializers.resolutions.get("Roblox")
        self.res = self.resolution_mid()
        self.setGeometry(self.res[0], self.res[1], (self.game_res[0] + 200), (self.game_res[1] + 200))
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
        self.hwnd = win32gui.FindWindow(None, "Roblox")
        self.container = QWidget(self)
        win32gui.SetParent(self.hwnd, int(self.container.winId()))
        self.layout.addWidget(self.container)
        self.initAttachWindow()

    def initAttachWindow(self):
        win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE) #Grabs HWND and uses SW_RESTORE to prevent minimization
        game_width = self.game_res[0]
        game_height = self.game_res[1]
        self.container.setFixedSize(game_width, game_height)
        win32gui.MoveWindow(self.hwnd, 0, 0, game_width, game_height, True) #Makes sure 800x600 is constant. Grabs x and y from rect
        self.coordinates = (self.res[0], self.res[1], self.game_res[0], self.game_res[1])
        return self.coordinates


    def resolutionMid(self):
        screen_resolution = self.screen_res # gets screen size from pyautogui
        x = (screen_resolution.width - 1000) // 2 # 1000x700 since roblox is at 800x600
        y = (screen_resolution.height- 700) // 2
        middle_screen = (x, y)
        return middle_screen