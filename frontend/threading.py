from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QSizePolicy)
import time
from backend import initializers

class attachedWindow(QMainWindow):
    def __init__(self, step):
        super().__init__()
        self.step = step
        self.setupQtWorker()

    def setupWorker(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
    
    def updateStatus(self, step):
        self.status_label.setText(f"Currently at {step}")

    def setupQtWorker(self):
        self.layout = QVBoxLayout()
        self.container = QWidget(self)
        self.main_widget = QWidget()
        self.hbox = QHBoxLayout()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        self.layout.addLayout(self.hbox)
        self.container_size = initializers.qt.get("worker_container_res")
    
    def setupWindow(self):
        container_width, container_height = self.container_size
        

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def run(self, step, sleep=1): # sleep should depend on a txt file in the future...
        while step > 0:
            self.progress.emit(step)
            time.sleep(sleep)
            step -= 1
        self.progress.emit("Finished.")
        self.finished.emit()