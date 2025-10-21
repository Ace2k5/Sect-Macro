from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout,
                            QPushButton, QSizePolicy, QWidget, QMainWindow, QLabel, QApplication)
from backend import windows_util, initializers
from . import threading, debug_utils, game_manager
import sys

class UnitWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.unit_window = initializers.qt.get("unit_window")
        self.unit_window_res = self.unit_window.get("unit_window_res")
        self.center = windows_util.resolutionMid(self.unit_window_res[0], self.unit_window_res[1])
        self.setupWindow()
    

    def setupWindow(self):
        self.setWindowTitle("Unit Window")
        self.widget = QWidget()
        self.main_layout = QVBoxLayout(self.widget)
        self.setCentralWidget(self.widget)
        self.setGeometry(self.center[0], self.center[1], self.unit_window_res[0], self.unit_window_res[1])
        self.widget.setStyleSheet("background-color: #1b1b1f;")
        
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        for i in range(3):
            label = QLabel()
            label.setText(f"Unit {i + 1}")
            label.setStyleSheet("font-size: 10px;" \
                            "font-family: Times New Roman;"
                            "font-weight: bold;"
                            "color: white;"
                            )
            label.setAlignment(Qt.AlignCenter)
            self.hbox1.addWidget(label)
        self.main_layout.addLayout(self.hbox1)
        for i in range(3):
            label = QLabel()
            label.setText (f"Unit {(i + 3) + 1}")
            label.setStyleSheet("font-size: 10px;" \
                            "font-family: Times New Roman;"
                            "font-weight: bold;"
                            "color: white;"
                            )
            label.setAlignment(Qt.AlignCenter)
            self.hbox2.addWidget(label)
        self.main_layout.addLayout(self.hbox2)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UnitWindow()
    window.show()
    sys.exit(app.exec_())