from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QSizePolicy)
import time
from backend import initializers
from mss import mss

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(object)
    location_found = pyqtSignal(tuple)
    
    def __init__(self):
        super().__init__()
        self.img_proc = None
        self.template_filename = None
        self.rect = None
        
    def setup(self, proc, filename: str, rect: tuple):
        self.img_proc = proc
        self.template_filename = filename
        self.rect = rect

    def run(self):
        try:
            if self.img_proc and self.template_filename and self.rect:
                with mss() as sct:
                    location = self.img_proc.both_methods(self.template_filename, self.rect, sct)
                if location:
                    self.location_found.emit(location)
                self.progress.emit(location)
            else:
                print("Worker not init properly.")
        except Exception as e:
            self.progress.emit(None)
        finally:
            self.progress.emit("Finished.")
            self.finished.emit()