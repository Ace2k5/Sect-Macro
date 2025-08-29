import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QFont
import pyautogui
from backend import initializers
#Still testing pyqt
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.screen_res = pyautogui.size()
        self.game_res = initializers.resolutions.get("Roblox")
        self.res = self.resolution_mid()
        self.setGeometry(self.res[0], self.res[1], (self.game_res[0] + 200), (self.game_res[1] + 100))
        self.setWindowTitle("Sect v0.0.1")

        
    def resolution_mid(self):
        screen_resolution = self.screen_res
        x = (screen_resolution.width - 1000) // 2
        y = (screen_resolution.height- 700) // 2
        middle_screen = (x, y)
        return middle_screen


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()