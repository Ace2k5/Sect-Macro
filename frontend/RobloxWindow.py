from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QTextEdit)
from backend import windows_util, initializers
from . import threading, debug_utils, game_manager

#temporary consts
TITLE = "Sect v0.0.1"

'''
    Initializes and sets Qtapplication as the parent application where Roblox is the child and is attached to the Qtapplication 
'''
class RobloxWindow(QMainWindow):
    def __init__(self, game_config: dict, mode: str, log_window: object):
        super().__init__()
        self.game_config = game_config
        self.mode = mode
        # LOGGER #
        self.logger = log_window
        # Qt #
        self.setupQt()
        self.setupMainWindow()
        qt_window_handle = self.winId()
        # GAME MANAGER #
        self.manager = game_manager.GameManager(self.hbox, self.roblox_container, self.container,
                                                qt_window_handle, self.layout, self.game_config, self.mode,
                                                self.logger)
        self.manager.setupRobloxIntegration()
        self.manager.setupTemplateMatching()
        self.manager.setupRobloxWindow()
        # DEV TOOLS #
        self.setupDebugControls()
        self.remove_logger_borders()
        
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

    def remove_logger_borders(self):
        """
        Remove title bar and borders from logger window
        """
        if hasattr(self.logger, 'winId'):
            logger_hwnd = self.logger.winId()
            if logger_hwnd:
                import win32gui
                import win32con
                
                current_style = win32gui.GetWindowLong(logger_hwnd, win32con.GWL_STYLE)
                new_style = current_style & ~(
                    win32con.WS_MINIMIZEBOX | 
                    win32con.WS_MAXIMIZEBOX
                )
                win32gui.SetWindowLong(logger_hwnd, win32con.GWL_STYLE, new_style)
                win32gui.SetWindowPos(logger_hwnd, None, 0, 0, 0, 0,
                                    win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | 
                                    win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED)

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
        if self.logger:
            self.logger.close()
        super().closeEvent(event)