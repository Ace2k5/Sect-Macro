from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton)
from backend import initializers, windows_util, template_matching
import pyautogui
import win32con
import win32gui
#temporary consts
TITLE = "Sect v0.0.1 | Anime Guardians"
CURRENT_GAME = "Anime_Guardians"


class Guardians(QMainWindow):
    def __init__(self):
        super().__init__()
        self.game_res = windows_util.getWindowRes("Roblox")
        self.hwnd = windows_util.initWindow("Roblox")
        self.roblox_rect = win32gui.GetWindowRect(self.hwnd) # (left, top, right, bottom)
        self.container = QWidget(self)
        self.mainWindow()
        self.layout = QVBoxLayout()
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        self.initWindow()
        self.testButton()

    def mainWindow(self):
        window_width, window_height = self.game_res[0] + 500, self.game_res[1] + 200
        window_x, window_y = windows_util.resolutionMid(window_width, window_height)
        self.setGeometry(window_x, window_y, window_width, window_height)
        self.setWindowTitle(f"{TITLE}")
        self.setStyleSheet("background-color: #1b1b1f;")
        
    def initWindow(self):
        self.container.setFixedSize(self.game_res[0] + 20, self.game_res[1] + 40) # after removing title bar and border, windows of roblox still returns as 816 x 638 so we add +20 and +40 for any future discrepancies for qt
        final_container = windows_util.initattachWindow(self.hwnd, self.container)
        self.layout.addWidget(final_container, alignment=Qt.AlignHCenter | Qt.AlignRight)
        ### --- DEBUG INFO --- ###
        print("=== Qt container ===")
        print("size:", final_container.size().width(), "x", final_container.size().height())
        print("geometry:", final_container.geometry())         # QRect: x,y,w,h
        print("contentsRect:", final_container.contentsRect()) # excludes margins

        rect = win32gui.GetWindowRect(self.hwnd)   # (left, top, right, bottom)
        client = win32gui.GetClientRect(self.hwnd) # (0,0,width,height) relative
        print("=== Roblox HWND ===")
        print("window rect:", rect, "=> w,h =", rect[2]-rect[0], "x", rect[3]-rect[1])
        print("client rect:", client, "=> w,h =", client[2]-client[0], "x", client[3]-client[1])
        ### --- DEBUG INFO END --- ###
        
    def testButton(self):
        button = QPushButton("Test menu", self)
        button.setStyleSheet("font-size: 30px;" \
                             "font-family: Times New Roman;" 
                             "font-weight: bold;"
                             "color: white")
        self.layout.addWidget(button, alignment=Qt.AlignTop)
        self.button = button
        button.clicked.connect(self.buttonFunc)
        
    def buttonFunc(self):
        template = template_matching.ImageProcessor()
        template.template_matching("main_menu.png", self.roblox_rect)
        
    def closeEvent(self, event):
        windows_util.removeParent(self.hwnd)
        super().closeEvent(event)