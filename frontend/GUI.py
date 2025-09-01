import sys
from PyQt5.QtWidgets import QApplication
from . import mainwindow
#Still testing pyqt
def main():
    app = QApplication(sys.argv)
    window = mainwindow.MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()