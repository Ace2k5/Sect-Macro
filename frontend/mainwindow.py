from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QMainWindow, QLabel, QWidget, QVBoxLayout,
                             QPushButton)
from backend import initializers, windows_util
from . import RobloxWindow
from functools import partial
'''
    The initial application window where user can select a multitude of games(?)
'''

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupMain()
        self.setupQt()
        self.initLabels()
        #   self.initImages()
        self.initButtons()
    
    '''We need params x, y, width and height for geometry so we only need the width and height to pass onto resMid for x and y'''
    def setupMain(self):
        window_width, window_height = initializers.qt.get("qt_default_resolution")
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
        for game_config in initializers.game_configs.values():
            button = QPushButton(game_config.get("display_name"), self)
            button.setStyleSheet("font-size: 30px;" \
                                "font-family: Times New Roman;" 
                                "font-weight: bold;"
                                "color: white")
            self.layout.setContentsMargins(0, 0, 0, 300)
            button.clicked.connect(partial(self.buttonFunc, game_config)) # partial prefills some of the args, each individual loop has their own values passed unto RobloxWindow class
                                                                          # root of all game_configs
            self.layout.addWidget(button, alignment=Qt.AlignTop)
        
    
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

    def buttonFunc(self, game_config: dict):
        print(f"Loading game: {game_config}")
        original_message = game_config.get("display_name")
        clicked_button = self.sender()
        if clicked_button:
            try:
                QTimer.singleShot(100, lambda: clicked_button.setText("Loading..."))
                self.new_window = RobloxWindow.RobloxWindow(game_config)
                self.new_window.show()
                self.close()
            except RuntimeError:
                QTimer.singleShot(100, lambda: clicked_button.setText("Roblox is not open, please open Roblox..."))
                clicked_button.setText(original_message)
                return
            except Exception as e:
                QTimer.singleShot(300, lambda: clicked_button.setText(f"An unknown error has occured as {e}."))
                clicked_button.setText(original_message)
