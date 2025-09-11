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


'''We needed first the game resolution which I've set in initializers as 800x600. So we now have window height and window width for the game, but we use this as a foundation for me to extend the application for the roblox window handle.
Then, we needed the x and y coordinates of the qt application for it to be centered, and so we called upon resolutionMid which took in the parameters of window_width and window_height and returned the position of a centered window via floor division.'''
    def mainWindow(self):
        self.game_res = initializers.resolutions.get("Roblox")
        if self.game_res is None:
            print("Game resolution not found. Problem within initializers.py ")
            return
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
        win32gui.MoveWindow(self.hwnd, 0, 0, game_width, game_height, True) #Makes sure 800x600 is constant. Grabs x and y from rect, 0 0 because now roblox handle is a child
        self.coordinates = (self.res[0], self.res[1], self.game_res[0], self.game_res[1])
        return self.coordinates