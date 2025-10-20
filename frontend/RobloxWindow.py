from PyQt5.QtWidgets import ( QVBoxLayout, QHBoxLayout,
                            QPushButton, QSizePolicy, QWidget, QMainWindow)
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
        # IMPORTANT #
        self.game_config = game_config
        self.mode = mode
        # 

        # LOGGER #
        self.logger = log_window
        #

        # Qt 
        self.setupQt()
        self.setupMainWindow()
        qt_window_handle = self.winId()
        #

        # SETUP
        self.logger_button = self.setupToggleLogger()
        self.manager = game_manager.GameManager(self.hbox, self.roblox_container, self.container,
                                                qt_window_handle, self.layout, self.game_config, self.mode,
                                                self.logger_button, self.logger)
        self.game_res = self.manager.game_res
        self.hwnd = self.manager.hwnd
        self.setupRobloxWindow()
        self.setupModeButtons()
        #

        # DEV TOOLS
        self.setupDebugControls()
        self.remove_logger_borders()
        #
        
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

        # second boxes

        self.vbox2 = QVBoxLayout()
        self.hbox.addLayout(self.vbox2)
    
    def setupToggleLogger(self):
        '''
        Button to showcase logs
        '''
        button = QPushButton("Show Logger")
        button.setStyleSheet("font-size: 30px;" \
                            "font-family: Times New Roman;" 
                            "font-weight: bold;"
                            "color: white;"
                            )
        button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.vbox2.addWidget(button)
        return button

    def setupModeButtons(self):
        '''
        Button for current available mode
        '''

        game_modes = self.game_config.get("gamemode")
        if self.mode in game_modes:
            button = QPushButton(self.mode)
            button.setStyleSheet("font-size: 30px;" \
                            "font-family: Times New Roman;" 
                            "font-weight: bold;"
                            "color: white;"
                            )
            button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.vbox2.addWidget(button)

    def setupRobloxWindow(self):
        '''
        Attachment of the roblox container to Qt GUI:
        roblox_container comes from setupQt
        hwnd comes from setupRobloxIntegration
        setupattachWindow requires 4 params: hwnd, size of container, width and height
        '''

        x, y = self.roblox_container
        if x is None or y is None:
            raise ValueError("roblox_container must be a tuple of (width, height)")
        self.container.setFixedSize(x, y)
        self.final_container = windows_util.setupattachWindow(self.hwnd, self.container, self.game_res[0], self.game_res[1])   
        self.hbox.addWidget(self.final_container)
        self.manager._debugWindowInfo()
    
    def deattachWindow(self):
        windows_util.removeParent(self.hwnd, self.game_res[0], self.game_res[1])

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
                    win32con.WS_MAXIMIZEBOX |
                    win32con.WS_SYSMENU
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
        self.debug = debug_utils.frontUtils(self.hbox, self.main_widget, self.manager, self.layout, self.vbox2)
        self.debug.testButton()
        self.debug.mouseButton()
        
    def closeEvent(self, event):
        '''
        safely de-attaches roblox from qt
        '''
        self.deattachWindow()
        if self.logger:
            self.logger.close()
        super().closeEvent(event)