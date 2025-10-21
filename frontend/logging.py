import sys
from PyQt5.QtCore import QObject, pyqtSignal, QDateTime, Qt
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
        button = QPushButton("Clear Debug", logs_panel)
        button.setStyleSheet("color: white;"
                            "font-family: Times New Roman;"
                            "font-size: 10px")
        self.logs_text.setStyleSheet("color: white;"
                                     "font-family: Times New Roman")


        layout_v.addWidget(logs_label, alignment=Qt.AlignHCenter)
        layout_v.addWidget(button, alignment=Qt.AlignHCenter)
        layout_v.addWidget(self.logs_text)

        logs_label.setStyleSheet("font-size: 25px;" \
                            "font-family: Times New Roman;"
                            "font-weight: bold;"
                            "color: white;"
                            )

        logs_panel.setStyleSheet("background-color: #3c3c42;"
                                 "border: none")

        button.clicked.connect(self.clear_logs)
        self.main_layout.addWidget(logs_panel)

    def setupDebugPanel(self):
        debug_panel = QWidget()
        layout_v = QVBoxLayout(debug_panel)

        debug_label = QLabel("Debug")
        self.debug_text = QTextEdit()
        self.debug_text.setReadOnly(True)
        button = QPushButton("Clear Debug", debug_panel)
        button.setStyleSheet("color: white;"
                            "font-family: Times New Roman;"
                            "font-size: 10px")

        self.debug_text.setStyleSheet("color: white;"
                                    "font-family: Times New Roman;")

        layout_v.addWidget(debug_label, alignment=Qt.AlignHCenter)
        layout_v.addWidget(button, alignment=Qt.AlignHCenter)
        layout_v.addWidget(self.debug_text)

        debug_panel.setStyleSheet("background-color: #3c3c42;"
                                  "border: none")
        debug_label.setStyleSheet("font-size: 25px;" \
                            "font-family: Times New Roman;"
                            "font-weight: bold;"
                            "color: white;"
                            )
        button.clicked.connect(self.clear_debug)


        self.main_layout.addWidget(debug_panel)

    def log_message(self, message: str, level: str = "INFO"):
        """Add a message to the logs panel"""
        timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
        formatted_message = f"[{timestamp}] [{level}] {message}"
        self.logs_text.append(formatted_message)
        
        cursor = self.logs_text.textCursor()
        cursor.movePosition(cursor.End)
        self.logs_text.setTextCursor(cursor)
        self.logs_text.ensureCursorVisible()
    
    def debug_message(self, message: str):
        """Add a message to the debug panel"""
        timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
        formatted_message = f"[{timestamp}] {message}"
        self.debug_text.append(formatted_message)
        
        cursor = self.debug_text.textCursor()
        cursor.movePosition(cursor.End)
        self.debug_text.setTextCursor(cursor)
        self.debug_text.ensureCursorVisible()
    
    def clear_logs(self):
        self.logs_text.clear()
    def clear_debug(self):
        self.debug_text.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoggerWindow()
    window.show()
    sys.exit(app.exec_())