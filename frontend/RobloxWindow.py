from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton, QSizePolicy)
from backend import initializers, windows_util, template_matching, ORB
import pyautogui
import win32con
import win32gui
#temporary consts
TITLE = "Sect v0.0.1"

'''
    Initializes and sets Qtapplication as the parent application where Roblox is the child and is attached to the Qtapplication 
'''
class RobloxWindow(QMainWindow):
    def __init__(self, game_config: dict):
        super().__init__()
        self.game_config = game_config
        self.setupQt()
        self.testButton()
        self.setupRobloxIntegration()
        self.setupMainWindow()
        self.setupRobloxWindow()
        self.setupTemplateMatching()
        
    def setupQt(self):
        self.layout = QVBoxLayout()
        self.container = QWidget(self)
        self.main_widget = QWidget()
        self.hbox = QHBoxLayout()
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(1)
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        self.layout.addLayout(self.hbox)

    def setupTemplateMatching(self):
        self.template_match = template_matching.ImageProcessor()

    def setupRobloxIntegration(self):
        title = self.game_config["window_title"]
        print(title)
        self.game_res = self.game_config["resolution"]
        self.hwnd = windows_util.initWindow(title)
        self.roblox_rect = win32gui.GetWindowRect(self.hwnd) # (left, top, right, bottom)

    def setupMainWindow(self):
        window_width, window_height = self.game_res[0] + 500, self.game_res[1] + 200
        window_x, window_y = windows_util.resolutionMid(window_width, window_height)
        self.setGeometry(window_x, window_y, window_width, window_height)
        self.setWindowTitle(f"{TITLE} | {self.game_config['display_name']}")
        self.setStyleSheet("background-color: #1b1b1f;")
        
    def setupRobloxWindow(self):
        self.container.setFixedSize(self.game_res[0] + 20, self.game_res[1] + 40) # after removing title bar and border, windows of roblox still returns as 816 x 638 so we add +20 and +40 for any future discrepancies for qt
        self.final_container = windows_util.setupattachWindow(self.hwnd, self.container, self.game_res[0], self.game_res[1])
        self.final_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.hbox.addWidget(self.final_container)
        
        self._debugWindowInfo()
        
    def _debugWindowInfo(self):
        ### --- DEBUG INFO --- ###
        print("=== Qt container ===")
        print("size:", self.final_container.size().width(), "x", self.final_container.size().height())
        print("geometry:", self.final_container.geometry())         # QRect: x,y,w,h
        print("contentsRect:", self.final_container.contentsRect()) # excludes margins

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
        self.hbox.addWidget(button)
        self.button = button
        button.clicked.connect(self.buttonFunc)
        
    def buttonFunc(self):
        current_roblox_rect = win32gui.GetWindowRect(self.hwnd)
        location = self.template_match.both_methods("main_menu.png", current_roblox_rect)
        if location is None:
            print("No location has been given, skipping the process...")
            return   
        
    def closeEvent(self, event):
        windows_util.removeParent(self.hwnd, self.game_res[0], self.game_res[1])
        super().closeEvent(event)