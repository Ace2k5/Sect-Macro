from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QSizePolicy, QTextEdit)
from PyQt5.QtCore import QTimer, QObject, QThread
from backend import windows_util, template_matching, initializers, clicks
from . import threading, debug_utils
import win32gui
from pathlib import Path
import win32api
from abc import ABC, abstractmethod
TITLE = "Sect v0.0.1"
class GameManager(QObject):
    def __init__(self, hbox: QHBoxLayout, roblox_container: tuple[int, int], container: QObject, qt_window_handle: int, layout: QVBoxLayout, game_config: dict, mode: str):
        super().__init__()
        self.hbox = hbox
        self.game_config = game_config
        self.roblox_container = roblox_container
        self.container = container
        self.qt_hwnd = qt_window_handle
        self.layout = layout
        self.template_worker = None
        self.template_thread = None
        self.location = None
        self.mode = mode
        self.state_manager = self.gameInstance()
        
        
# --------------------------SETUP-------------------------------------- #
        
    def gameInstance(self):
        if self.mode == "summer":
            from .guardians import summerEvent
            return summerEvent(self.game_config, self.click)
        if self.mode == "infinite":
            from .guardians import infinite
            return infinite(self.game_config, self.click)
    
    def setupTemplateMatching(self):
        '''
        sets up template_matching class
        '''
        self.game_images = self.game_config.get('game_images')
        if self.game_images is None:
            raise KeyError("The key type of game_config['game_images'] does not exist.")
        self.template_match = template_matching.ImageProcessor(self.game_images)
        
    def click(self, location: tuple, hardlocation: tuple[int,int]=None, rect=None):
        if location:
            clicks.left_click_location(location)
        if hardlocation and rect:
            clicks.left_hardcoded_clicks(hardlocation, rect)
        
    def setupRobloxIntegration(self):
        '''
        attaches roblox to qt and also gets the resolution from dict in initializers.py
        '''
        title = self.game_config.get("window_title")
        if title is None:
            raise KeyError("The key type of game_config['window_title'] does not exist.")
        print(title)
        self.game_res = self.game_config.get("resolution")
        if self.game_res is None or self.game_res == 0:
            raise KeyError("The key type of game_config['resolution'] does not exist.")
        self.hwnd = windows_util.initWindow(title)
        
    def setupRobloxWindow(self):
        '''
        Attachment of the roblox container to Qt GUI:
        roblox_container comes from setupQt
        hwnd comes from setupRobloxIntegration
        setupattachWindow requires 4 params: hwnd, size of container, width and height
        '''
        x, y = self.roblox_container
        if x is None or y is None:
            raise ValueError("roblox_container must be a tuple of (width, height)")
        self.container.setFixedSize(x, y)
        self.final_container = windows_util.setupattachWindow(self.hwnd, self.container, self.game_res[0], self.game_res[1])
        self.final_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.hbox.addWidget(self.final_container)
        
        self._debugWindowInfo()
        
    def deattachWindow(self):
        windows_util.removeParent(self.hwnd, self.game_res[0], self.game_res[1])
        
# --------------------------SETUP-------------------------------------- #

# ------------------------- THREAD ------------------------------- #
    def handle_location_found(self, location: tuple[int, int]):
        print(f"Found location in: {location}")
        self.state_manager.updateLocation(location) 
        
    def start_worker(self, template_match: template_matching.ImageProcessor, template_filename: str, rect: tuple):
        self.template_thread = QThread()
        self.template_worker = threading.Worker()
        self.template_worker.setup(template_match, template_filename, rect)
        self.template_worker.moveToThread(self.template_thread)
        
        self.template_worker.location_found.connect(self.handle_location_found)
        
        self.template_worker.finished.connect(self.template_thread.quit)
        self.template_worker.finished.connect(self.template_worker.deleteLater)
        self.template_thread.finished.connect(self.template_thread.deleteLater)
        
        self.template_thread.started.connect(self.template_worker.run)
        self.template_thread.start()
        
    def cleanupWorker(self):
        if self.template_thread and self.template_thread.isRunning():
            self.template_thread.quit()
            self.template_thread.wait()
        print("Worker cleaned up.")
# ------------------------- THREAD ------------------------------- #


    # --------------------- DEBUG TOOLS --------------------- #
    def _debugWindowInfo(self) -> None:
        ### --- DEBUG INFO --- ###
        print("=== Qt container ===")
        print("size:", self.final_container.size().width(), "x", self.final_container.size().height())
        print("geometry:", self.final_container.geometry())         # QRect: x,y,w,h
        print("contentsRect:", self.final_container.contentsRect()) # excludes margins

        rect = win32gui.GetWindowRect(self.hwnd)   # (left, top, right, bottom)
        client = win32gui.GetClientRect(self.hwnd) # (0,0,width,height) relative
        print("=== Roblox HWND ===")
        print("window rect:", rect, "=> w,h =", rect[2]-rect[0], "x", rect[3]-rect[1])
        print("client rect:", client, "=> w,h =", client[2]-client[0], "x", client[3]-client[1])
        ### --- DEBUG INFO END --- ###
        
        
    def printMouse(self) -> None:
        '''
        this function gets the relative positioning of the roblox application. By subtracting the position of the cursor and the x and y of the application
        we are able to find where the roblox window is and check if it is outside the boundary
        steps:
        1. get cursor x and y via getcursorpos()
        2. find top and left from getwindowrect(self.hwnd)
        3. subtract x - top, y - left to get relative x and y to the screen of the Roblox window
        4. left, top, right, bottom to detect the relative position of roblox window
        5. check if qt application is minimized first to stop unnecessary logs when qt is minimized
        6. if x is greater than left and less than right, then it is inside the boundary, same goes for y but top and bottom otherwise it is outside
        '''
        x, y = win32api.GetCursorPos()
        rect = win32gui.GetWindowRect(self.hwnd)
        relative_x, relative_y = (x - rect[0]), (y - rect[1])
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        
        minimized = self.qt_hwnd
        if win32gui.IsIconic(minimized):
            print("Window is minimized.")
        else:
            if left <= x <= right and top <= y <= bottom:
                relative_x, relative_y = x - left, y - top
                print((relative_x, relative_y))
            else:
                print("Mouse is outside boundary.")
    
    def buttonFunc(self):
        '''
        testing connectivity between backend and frontend
        '''
        current_roblox_rect = win32gui.GetWindowRect(self.hwnd)
        self.start_worker(self.template_match, "sjw.png", current_roblox_rect)
        
    
        
        
class GameState(ABC):
    def __init__(self, game_config: dict, click_function: clicks):
        self.game_mode = game_config.get('gamemode')
        self.location = None
        self.game_config = game_config
        self.click = click_function
    
    def initClicks(self, x: int, y: int):
        self.click(x, y)
        
    def updateLocation(self, location: tuple[int, int]):
        self.location = location
        self.clickLocation(self.location)
        
    def clickLocation(self, location: tuple[int, int]):
        self.click(location)
        
    @abstractmethod
    def initialGameClick(self):
        pass
    
    @abstractmethod
    def gameModeClick(self):
        pass