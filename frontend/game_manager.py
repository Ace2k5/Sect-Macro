from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QSizePolicy, QTextEdit)
from PyQt5.QtCore import QTimer, QObject
from backend import windows_util, template_matching, initializers
from . import threading, debug_utils
import win32gui
from pathlib import Path
import win32api
TITLE = "Sect v0.0.1"
class gameManager(QObject):
    def __init__(self, hbox, roblox_container, container, game_config: dict):
        super().__init__()
        self.hbox = hbox
        self.game_config = game_config
        self.roblox_container = roblox_container
        self.container = container
        
    def setupTemplateMatching(self):
        '''
        sets up template_matching class
        '''
        self.game_images = self.game_config.get("game_images")
        self.template_match = template_matching.ImageProcessor(self.game_images)
        
    def setupRobloxIntegration(self):
        '''
        attaches roblox to qt and also gets the resolution from dict in initializers.py
        '''
        title = self.game_config.get("window_title")
        print(title)
        self.game_res = self.game_config.get("resolution")
        self.hwnd = windows_util.initWindow(title)
        if self.hwnd is None or self.hwnd == 0:
            print("HWND is invalid.")
            return
        
    def setupRobloxWindow(self):
        '''
        Attachment of the roblox container to Qt GUI:
        roblox_container comes from setupQt
        hwnd comes from setupRobloxIntegration
        setupattachWindow requires 4 params: hwnd, size of container, width and height
        '''
        x, y = self.roblox_container
        self.container.setFixedSize(x, y)
        self.final_container = windows_util.setupattachWindow(self.hwnd, self.container, self.game_res[0], self.game_res[1])
        self.final_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.hbox.addWidget(self.final_container)
        
        self._debugWindowInfo()
        
    def deattachWindow(self):
        windows_util.removeParent(self.hwnd, self.game_res[0], self.game_res[1])
        
        
        
        
    # --------------------- DEBUG TOOLS
    def _debugWindowInfo(self):
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
        
        
    def printMouse(self):
        '''
        this function gets the relative positioning of the roblox application. By subtracting the position of the cursor and the x and y of the application
        we are able to find where the roblox window is and check if it is outside the boundary
        steps:
        1. get cursor x and y via getcursorpos()
        2. find top and left from getwindowrect(self.hwnd)
        3. subtract x - top, y - left to get relative x and y to the screen of the Roblox window
        4. left, top, right, bottom to detect the relative position of roblox window
        5. check if qt application is minimized first to stop unnecessary logs when qt is minimized
        6. if x is greater than left and less than right, then it is outside the boundary, same goes for y but top and bottom
        '''
        x, y = win32api.GetCursorPos()
        rect = win32gui.GetWindowRect(self.hwnd)
        relative_x, relative_y = (x - rect[0]), (y - rect[1])
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        
        minimized = self.qt_hwnd()
        if win32gui.IsIconic(minimized):
            print("Window is minimized.")
        else:
            if left <= x <= right and top <= y <= bottom:
                relative_x, relative_y = x - left, y - top
                print((relative_x, relative_y))
            else:
                print("Mouse is outside boundary.")
    
    def buttonFunc(self):
        current_roblox_rect = win32gui.GetWindowRect(self.hwnd)
        location = self.template_match.both_methods("main_menu.png", current_roblox_rect)
        if location is None:
            print("No location has been given, skipping the process...")
            return
        return location
        
    def qt_hwnd(self):
        hwnd = win32gui.FindWindow(None, (f"{TITLE} | {self.game_config['display_name']}"))
        return hwnd
    