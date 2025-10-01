from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QSizePolicy, QTextEdit)
from PyQt5.QtCore import QTimer
from backend import windows_util, template_matching, initializers
from . import threading, debug_utils, game_manager
import win32gui
from pathlib import Path
import win32api

#temporary consts
TITLE = "Sect v0.0.1"

'''
    Initializes and sets Qtapplication as the parent application where Roblox is the child and is attached to the Qtapplication 
'''
class RobloxWindow(QMainWindow):
    def __init__(self, game_config: dict):
        super().__init__()
        self.game_config = game_config
        # Qt #
        self.setupQt()
        self.setupMainWindow()
        qt_window_handle = self.winId()
        # GAME MANAGER #
        self.manager = game_manager.gameManager(self.hbox, self.roblox_container, self.container, qt_window_handle, self.layout, self.game_config)
        self.manager.setupRobloxIntegration()
        self.manager.setupTemplateMatching()
        self.manager.setupRobloxWindow()
        # DEV TOOLS #
        self.setupDebugControls()
        
    def setupQt(self):
        '''
        sets up qt buttons and miscellaneous
        '''
        self.layout = QVBoxLayout()
        self.container = QWidget(self)
        self.main_widget = QWidget()
        self.hbox = QHBoxLayout()
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

    def setupMainWindow(self):
        '''
        sets the qt application width and height
        '''
        window_width, window_height = self.qt_res
        window_x, window_y = windows_util.resolutionMid(window_width, window_height)
        self.setGeometry(window_x, window_y, window_width, window_height)
        self.setWindowTitle(f"{TITLE} | {self.game_config.get('display_name')}")
        self.setStyleSheet("background-color: #1b1b1f;")
        
        
    def setupDebugControls(self):
        '''
        for debugging window, checking template_matching and all other stuff.
        '''
        self.debug = debug_utils.frontUtils(self.hbox, self.main_widget, self.manager, self.layout)
        self.debug.testButton()
        self.debug.mouseButton()
        
    def setupThreading(self):
        self.thread = threading.attachedWindow(None, self.layout)
        
    def closeEvent(self, event):
        '''
        safely de-attaches roblox from qt
        '''
        self.manager.deattachWindow()
        super().closeEvent(event)