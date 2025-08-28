import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QFont
import pyautogui
#Still testing pyqt
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.screen_res = pyautogui.size()
        self.res = self.resolution_mid()
        self.setGeometry(self.res[0], self.res[1], 800, 600)
        self.setWindowTitle("Sect v0.0.1")
        
        label = QLabel("Hello", self)
        label.setFont(QFont("Arial"))
        label.setGeometry(0, 0, 1000, 600)

        
    def resolution_mid(self):
        screen_resolution = self.screen_res
        x = (screen_resolution.width - 800) // 2
        y = (screen_resolution.height- 600) // 2
        middle_screen = (x, y)
        return middle_screen


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()