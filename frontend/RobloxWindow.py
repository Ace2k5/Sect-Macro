from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QSizePolicy, QTextEdit)
from backend import windows_util, template_matching, initializers
from . import threading
import win32gui
#temporary consts
TITLE = "Sect v0.0.1"

'''
    Initializes and sets Qtapplication as the parent application where Roblox is the child and is attached to the Qtapplication 
'''
class RobloxWindow(QMainWindow):
    def __init__(self, game_config: dict):
        super().__init__()
        self.game_config = game_config # originates in mainwindow.py
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
        self.qt_res = initializers.qt.get("qt_default_resolution")
        self.roblox_container = initializers.qt.get("roblox_container_res")

    def setupLogs(self, game_config: str): # specialized game configs should have a set function in the future.
        self.threadUpdate = threading.attachedWindow(game_config)
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.hbox.addWidget(self.log_box)
        self.setGeometry()

    def setupTemplateMatching(self):
        game_images = self.game_config.get("game_images")
        self.template_match = template_matching.ImageProcessor(game_images)

    def setupRobloxIntegration(self):
        title = self.game_config["window_title"]
        print(title)
        self.game_res = self.game_config["resolution"]
        self.hwnd = windows_util.initWindow(title)

    def setupMainWindow(self):
        window_width, window_height = self.qt_res
        window_x, window_y = windows_util.resolutionMid(window_width, window_height)
        self.setGeometry(window_x, window_y, window_width, window_height)
        self.setWindowTitle(f"{TITLE} | {self.game_config['display_name']}")
        self.setStyleSheet("background-color: #1b1b1f;")
        
    def setupRobloxWindow(self):
        '''
        Attachment of the roblox container to Qt GUI:
        roblox_container comes setupQt
        hwnd comes from setupRobloxIntegration
        setupattachWindow requires 4 params: hwnd, size of container, width and height
        '''
        x, y = self.roblox_container
        self.container.setFixedSize(x, y)
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