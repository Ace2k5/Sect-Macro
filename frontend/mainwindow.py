from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QPushButton)
from PyQt5.QtGui import QPixmap
import pyautogui
from backend import initializers, windows_util
from . import guardiansWindow

'''
    The initial application window where user can select a multitude of games(?)
'''

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.game_res = windows_util.getWindowRes("Roblox")
        self.setupMain()
        self.setupQt()
        self.initLabels()
        #   self.initImages()
        self.initButtons()
    
    '''We needed first the game resolution which I've set in initializers as 800x600. So we now have window height and window width for the game, but we use this as a foundation for me to extend the application for the roblox window handle.
Then, we needed the x and y coordinates of the qt application for it to be centered, and so we called upon resolutionMid which took in the parameters of window_width and window_height and returned the position of a centered window via floor division.'''
    def setupMain(self):
        window_width, window_height = self.game_res[0] + 200, self.game_res[1] + 200
        window_x, window_y = windows_util.resolutionMid(window_width, window_height)
        self.setGeometry(window_x, window_y, window_width, window_height)
        self.setWindowTitle("Sect v0.0.1")
        self.setStyleSheet("background-color: #1b1b1f;")
        
    def setupQt(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(1)
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        
    def initLabels(self):
        label = QLabel("Sect")
        label.setStyleSheet("font-size: 50px;" \
                            "font-family: Times New Roman;"
                            "font-weight: bold;"
                            "color: white")
        self.layout.addWidget(label, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
    def initButtons(self):
        button = QPushButton("Anime Guardians", self)
        button.setStyleSheet("font-size: 30px;" \
                             "font-family: Times New Roman;" 
                             "font-weight: bold;"
                             "color: white")
        self.layout.setContentsMargins(0, 0, 0, 300)
        self.layout.addWidget(button, alignment=Qt.AlignTop)
        self.button = button
        button.clicked.connect(self.buttonFunc)
        
    
    '''def initImages(self):
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
        self.layout.addWidget(image_label, alignment=Qt.AlignHCenter)'''

    def buttonFunc(self):
        QTimer.singleShot(100, lambda: self.button.setText("Loading..."))
        self.new_window = guardiansWindow.Guardians()
        self.new_window.show()
        self.close()
