from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton)
from PyQt5.QtGui import QPixmap
import pyautogui
from backend import initializers
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initMain()
        self.layout = QVBoxLayout()
        self.layout.setSpacing(1)
        self.main_widget = QWidget()
        self.initLabels()
        self.initImages()
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
        label = QLabel("Sect")
        label.setStyleSheet("font-size: 50px;" \
                            "font-family: Times New Roman;"
                            "font-weight: bold;")
        self.layout.addWidget(label, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
    def initButtons(self):
        button = QPushButton("Anime Vanguards", self)
        button.setStyleSheet("font-size: 30px;" \
                             "font-family: Times New Roman;" 
                             "font-weight: bold;")
        self.layout.setContentsMargins(0, 0, 0, 300)
        self.layout.addWidget(button, alignment=Qt.AlignTop)
        self.button = button
        button.clicked.connect(self.buttonFunc)
    
    def initImages(self):
        image_label = QLabel(self)
        self.setStyleSheet("background-color: grey;")
        bg_pic = QPixmap("D:/python_scripts/Sect/Images/misc_images/download.png")
        if bg_pic.isNull():
            print("Did not load.")
            print(os.getcwd())
            return
        image_label.setPixmap(bg_pic)
        image_label.setGeometry(0, 0, bg_pic.width(), bg_pic.height())
        image_label.setScaledContents(True)
        self.layout.addWidget(image_label, alignment=Qt.AlignHCenter)

    def buttonFunc(self):
        QTimer.singleShot(100, lambda: self.button.setText("Loading..."))
    
    def resolution_mid(self):
        screen_resolution = self.screen_res
        x = (screen_resolution.width - 1000) // 2
        y = (screen_resolution.height- 700) // 2
        middle_screen = (x, y)
        return middle_screen