import sys
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTextEdit, QComboBox, 
                             QCheckBox, QLabel)
from backend import initializers, windows_util

class LoggerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.log_info = initializers.qt.get("logging")
        self.log_res = self.log_info.get("logging_res")
        self.center_screen = windows_util.resolutionMid(self.log_res[0], self.log_res[1])
        self.setWindowTitle("Logger")
        self.setGeometry(self.center_screen[0], self.center_screen[1], self.log_res[0], self.log_res[1])

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)
        central_widget.setStyleSheet("background-color: #1b1b1f;")
        self.setupLogsPanel()
        self.setupDebugPanel()


    def setupLogsPanel(self):
        logs_panel = QWidget()
        layout_v = QVBoxLayout(logs_panel)

        logs_label = QLabel("Logs")
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)

        layout_v.addWidget(logs_label)
        layout_v.addWidget(self.logs_text)

        logs_label.setStyleSheet("font-size: 25px;" \
                            "font-family: Times New Roman;"
                            "font-weight: bold;"
                            "color: white;"
                            )

        logs_panel.setStyleSheet("background-color: #3c3c42;"
                                 "border: none")

        self.main_layout.addWidget(logs_panel)

    def setupDebugPanel(self):
        debug_panel = QWidget()
        layout_v = QVBoxLayout(debug_panel)

        debug_label = QLabel("Debug")
        self.debug_text = QTextEdit()
        self.debug_text.setReadOnly(True)

        layout_v.addWidget(debug_label)
        layout_v.addWidget(self.debug_text)

        debug_panel.setStyleSheet("background-color: #3c3c42;"
                                  "border: none")
        debug_label.setStyleSheet("font-size: 25px;" \
                            "font-family: Times New Roman;"
                            "font-weight: bold;"
                            "color: white;"
                            )


        self.main_layout.addWidget(debug_panel)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoggerWindow()
    window.show()
    sys.exit(app.exec_())