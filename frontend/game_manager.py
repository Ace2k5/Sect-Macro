from PyQt5.QtWidgets import ( QVBoxLayout, QHBoxLayout,
                             QPushButton, QSizePolicy)
from PyQt5.QtCore import QObject, QThread
from backend import windows_util, template_matching
from . import threading
import win32gui
import win32api
from functools import partial
TITLE = "Sect v0.0.1"
class GameManager(QObject):
    def __init__(self, hbox: QHBoxLayout, roblox_container: tuple[int, int],
                 container: QObject, qt_window_handle: int, layout: QVBoxLayout,
                 game_config: dict, mode: str, log_window: object):
        super().__init__()
        self.hbox = hbox
        self.game_config = game_config
        self.roblox_container = roblox_container
        self.container = container
        self.qt_hwnd = qt_window_handle
        self.vbox = layout
        self.template_worker = None
        self.template_thread = None
        self.location = None
        self.mode = mode
        self.hwnd = self.setupHWND()
        self.game_res = self.setupRobloxIntegration()
        self.setupTemplateMatching()
        self.state_manager = self.gameInstance()
        self.logger = log_window
        self.final_container = windows_util.setupattachWindow(self.hwnd, self.container, self.game_res[0], self.game_res[1])  
        
        
# --------------------------SETUP-------------------------------------- #
        
    def gameInstance(self):
        '''
        creates instance of the chosen mode in mainwindow.py
        '''
        #prefill worker so we only need template_filename for easy access
        prefilled_temp_match = partial(self.start_worker, template_match=self.template_match, rect=win32gui.GetWindowRect(self.hwnd))
        if self.mode == "summer":
            from .guardians import summerEvent
            return summerEvent(self.game_config, prefilled_temp_match, self.handle_location_found)
        if self.mode == "infinite":
            from .guardians import infinite
            return infinite(self.game_config, prefilled_temp_match, self.handle_location_found)


    def setupHWND(self):
        self.title = self.game_config.get("window_title")
        self.hwnd = windows_util.initWindow(self.title)
        return self.hwnd

    def setupTemplateMatching(self):
        '''
        sets up template_matching class
        '''
        self.game_images = self.game_config.get('game_images')
        if self.game_images is None:
            raise KeyError(f"The key type of game_config[{self.game_images}] does not exist.")
        self.template_match = template_matching.ImageProcessor(self.game_images)
        
    def setupRobloxIntegration(self):
        '''
        attaches roblox to qt and also gets the resolution from dict in initializers.py
        '''
        if self.title is None:
            raise KeyError(f"The key type of game_config['{self.title}'] does not exist.")
        print(self.title)
        self.game_res = self.game_config.get("resolution")
        if self.game_res is None or self.game_res == 0:
            raise KeyError(f"The key type of game_config['{self.game_res}'] does not exist.")
        return self.game_res
        
# --------------------------SETUP-------------------------------------- #

# ------------------------- THREAD ------------------------------- #
    def handle_location_found(self, location: tuple[int, int]):
        '''
        params:
        location -> tuple [int, int]

        this code handles the location emitted and referenced by the thread worker
        '''
        print(f"Found location in: {location}")
        self.location.updateLocation(location) 
        
    def start_worker(self, template_match: template_matching.ImageProcessor, template_filename: str, rect: tuple):
        '''
        params:
        template matching -> object
        template filname -> str
        rect(window x,y,w,h) -> tuple

        uses parallelism for template-matching so the gui doesn't freeze
        '''
        self.template_thread = QThread()
        self.template_worker = threading.Worker()

        # prefill args so only filename is required
        self.template_worker.setup(self.template_match, template_filename, win32gui.GetWindowRect(self.hwnd))
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