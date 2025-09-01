from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton)
import pyautogui
from backend import initializers

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initMain()
        self.layout = QVBoxLayout()
        self.main_widget = QWidget()
        self.initLabels()
        self.initButtons()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
    
    def initMain(self):
        self.screen_res = pyautogui.size()
        self.game_res = initializers.resolutions.get("Roblox")
        self.res = self.resolution_mid()
        self.setGeometry(self.res[0], self.res[1], (self.game_res[0] + 200), (self.game_res[1] + 100))
        self.setWindowTitle("Sect v0.0.1")
        self.setStyleSheet("background-color: grey;")
        
    def initLabels(self):
        label = QLabel("Hello!")
        label.setStyleSheet("font-size: 20px;")
        self.layout.addWidget(label, alignment=Qt.AlignTop)
        
    def initButtons(self):
        button = QPushButton("S", self)
        button.setStyleSheet("font-size: 30px;")
        self.layout.addWidget(button, alignment=Qt.AlignBottom)
        self.button = button
        button.clicked.connect(self.test)
            
    def test(self):
        self.button.setText("Clicked")
        QTimer.singleShot(500, lambda: self.button.setText("S"))
    
    def resolution_mid(self):
        screen_resolution = self.screen_res
        x = (screen_resolution.width - 1000) // 2
        y = (screen_resolution.height- 700) // 2
        middle_screen = (x, y)
        return middle_screen