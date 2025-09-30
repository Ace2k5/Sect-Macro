from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QSizePolicy, QTextEdit)
from PyQt5.QtCore import QTimer, QObject
from . import threading
import win32gui
from pathlib import Path
import win32api

class frontUtils(QObject):
    def __init__(self, hbox, main_widget, game_manager):
        super().__init__()
        self.main_widget = main_widget
        self.timer = QTimer()
        self.hbox = hbox
        self.game_manager = game_manager
        self.timer.timeout.connect(self.game_manager.printMouse)
    
    def testButton(self):
        button = QPushButton("Test menu", self.main_widget)
        button.setStyleSheet("font-size: 30px;" \
                             "font-family: Times New Roman;" 
                             "font-weight: bold;"
                             "color: white")
        self.hbox.addWidget(button)
        button.clicked.connect(self.game_manager.buttonFunc)

    def mouseButton(self):
        '''
        this function creates the clickable and toggleable button
        '''
        button = QPushButton("Mouse Debug", self.main_widget)
        button.setCheckable(True)
        button.setStyleSheet("font-size: 30px;" \
                             "font-family: Times New Roman;" 
                             "font-weight: bold;"
                             "color: white")
        self.hbox.addWidget(button)
        button.toggled.connect(self.mouseLoc)
            
    def mouseLoc(self, state):
        '''
        functions as the time.sleep equivalent of Qt.
        '''
        sender_button = self.sender()
        if state:
            self.timer.start(200)
            if sender_button:
                sender_button.setText("Getting coordinates.")
        else:
            self.timer.stop()
            if sender_button:
                sender_button.setText("Mouse Debug")