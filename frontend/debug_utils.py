from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QSizePolicy, QTextEdit, QLabel)
from PyQt5.QtCore import QTimer, QObject, Qt
from . import threading
import win32gui
from pathlib import Path
import win32api
class DebugController(QObject):
    def __init__(self, hbox: QHBoxLayout, main_widget: QWidget, game_manager: object,
                layout: QVBoxLayout, vbox2: QVBoxLayout, qt_window: tuple[int, int], hwnd: int,
                template_match: object, qt_hwnd: int, logger: object):
        super().__init__()
        # Qt
        self.main_widget = main_widget
        self.timer = QTimer()
        self.hbox = hbox
        self.game_manager = game_manager
        self.layout = layout
        self.timer.timeout.connect(self.printMouse)
        self.vbox2 = vbox2
        self.qt_window = qt_window
        self.qt_hwnd = qt_hwnd
        #

        # logs
        self.logger = logger
        self.log = self.logger.log_message
        self.debug = self.logger.debug_message
        # Game Manager
        self.hwnd = hwnd
        self.template_match = template_match
        self.start_worker = self.game_manager.start_worker
        #
        
        self.devTools()
    
    
    def devTools(self):
        local_container = QWidget()
        local_container.setStyleSheet("border-color: #555555;"
                                      "border-width: 1px;"
                                      "border-style: solid;")
        local_vbox = QVBoxLayout(local_container)
        test = self.testButton()
        coords = self.mouseButton()
        label = QLabel("Dev Tools")
        label.setStyleSheet("font-size: 10px;"
                            "font-family: Times New Roman;"
                            "font-weight: bold;"
                            "color: white;"
                            "border: none;"
                            )
        label.setFixedHeight(20)
        label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        local_vbox.addWidget(label, alignment=Qt.AlignHCenter)
        local_vbox.addWidget(test)
        local_vbox.addWidget(coords)
        self.vbox2.addWidget(local_container)
        
    
    def testButton(self):
        button = QPushButton("Test menu", self.main_widget)
        button.setStyleSheet("font-size: 30px;"
                             "font-family: Times New Roman;" 
                             "font-weight: bold;"
                             "color: white;")
        button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.vbox2.addWidget(button)
        button.clicked.connect(self.templateTest)
        return button

    def templateTest(self):
        '''
        testing connectivity between backend and frontend
        '''
        current_roblox_rect = win32gui.GetWindowRect(self.hwnd)
        self.start_worker(self.template_match, "sjw.png", current_roblox_rect)

    def mouseButton(self):
        '''
        this function creates the clickable and toggleable button
        '''
        button = QPushButton("Mouse Debug", self.main_widget)
        button.setCheckable(True)
        button.setStyleSheet("font-size: 30px;"
                             "font-family: Times New Roman;" 
                             "font-weight: bold;"
                             "color: white;")
        button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        button.toggled.connect(self.mouseLoc)
        return button


    def printMouse(self) -> None:
        '''
        this function gets the relative positioning of the roblox application. By subtracting the position of the cursor and the x and y of the application
        we are able to find where the roblox window is and check if it is outside the boundary
        steps:
        1. get cursor x and y via getcursorpos()
        2. find top and left from getwindowrect(self.hwnd)
        3. subtract x - top, y - left to get relative x and y to the screen of the Roblox window
        4. left, top, right, bottom to detect the relative position of roblox window
        5. check if qt application is minimized first to stop unnecessary logs when qt is minimized
        6. if x is greater than left and less than right, then it is inside the boundary, same goes for y but top and bottom otherwise it is outside
        '''
        x, y = win32api.GetCursorPos()
        rect = win32gui.GetWindowRect(self.hwnd)
        relative_x, relative_y = (x - rect[0]), (y - rect[1])
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        
        minimized = self.qt_hwnd
        if win32gui.IsIconic(minimized):
            self.debug("Window is minimized.")
        else:
            if left <= x <= right and top <= y <= bottom:
                relative_x, relative_y = x - left, y - top
                self.log((relative_x, relative_y))
            else:
                self.debug("Mouse is outside boundary.")

        
            
    def mouseLoc(self, state):
        '''
        functions as the time.sleep equivalent of Qt for self.timer. The primary receiver of the sender() in mouseButton
        '''
        sender_button = self.sender()
        if state:
            self.timer.start(200)
            if sender_button:
                sender_button.setText("Getting\ncoordinates.")
        else:
            self.timer.stop()
            if sender_button:
                sender_button.setText("Mouse Debug")
