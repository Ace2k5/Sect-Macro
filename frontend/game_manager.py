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
                 game_config: dict, mode: str, logger_button: QPushButton, logger_instance: object,
                 unit_window: object, unit_button: QPushButton):
        super().__init__()
        # Qt
        self.hbox = hbox
        self.game_config = game_config
        self.roblox_container = roblox_container
        self.container = container
        self.qt_hwnd = qt_window_handle
        self.vbox = layout
        #

        # Thread worker
        self.template_worker = None
        self.template_thread = None
        self.location = None
        #

        # instance setup
        #prefill worker so we only need template_filename for easy access
        self.prefilled_temp_match = lambda template_filename: self.start_worker(
            template_match=self.template_match,
            template_filename=template_filename,
            rect=win32gui.GetWindowRect(self.hwnd))
        self.mode = mode
        self.hwnd = self.setupHWND()
        self.game_res = self.setupRobloxIntegration()
        self.logger_instance = logger_instance
        self.logger_button = logger_button
        self.log = self.logger_instance.log_message
        self.debug = self.logger_instance.debug_message
        self.setupTemplateMatching()
        self.state_manager = self.gameInstance()
        self.unit_window_instance = unit_window
        self.unit_button = unit_button
        self.logger_button.clicked.connect(self.loggerShow)
        self.unit_button.clicked.connect(self.unitWindowShow)
        self.final_container = windows_util.setupattachWindow(self.hwnd, self.container, self.game_res[0], self.game_res[1])
        #
        
        
# --------------------------SETUP-------------------------------------- #
        
    def gameInstance(self):
        '''
        creates instance of the chosen mode in mainwindow.py
        '''
        if self.mode == "summer":
            from .guardians import summerEvent
            return summerEvent(self.game_config, self.prefilled_temp_match, self.handle_location_found)
        if self.mode == "infinite":
            from .guardians import infinite
            return infinite(self.game_config, self.prefilled_temp_match, self.handle_location_found)


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
        self.template_match = template_matching.ImageProcessor(self.game_images, self.logger_instance, self.mode)
        
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
        if location:
            self.log(f"Found location in: {location}")
            # log shit
        
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

        # args for this are prefilled using a lambda function
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
        self.debug("Worker cleaned up.")
# ------------------------- THREAD ------------------------------- #

# ----------------------- CALLABLES ----------------------- #

    def loggerShow(self):
        if self.logger_instance.isVisible():
            self.logger_instance.hide()
            self.logger_button.setText("Show Logger")
        else:
            self.logger_instance.show()
            self.logger_button.setText("Hide Logger")

    def unitWindowShow(self):
        if self.unit_window_instance.isVisible():
            self.unit_window_instance.hide()
            self.unit_button.setText("Unit Placement")
        else:
            self.unit_window_instance.show()
            self.unit_button.setText("Hide Unit\nPlacement")

    # --------------------- DEBUG TOOLS --------------------- #
    def _debugWindowInfo(self) -> None:
        ### --- DEBUG INFO --- ###
        self.debug("=== Qt container ===")
        self.debug(["size:", self.final_container.size().width(), "x", self.final_container.size().height()])
        self.debug(["geometry:", self.final_container.geometry()])         # QRect: x,y,w,h
        self.debug(["contentsRect:", self.final_container.contentsRect()]) # excludes margins

        rect = win32gui.GetWindowRect(self.hwnd)   # (left, top, right, bottom)
        client = win32gui.GetClientRect(self.hwnd) # (0,0,width,height) relative
        self.debug(["=== Roblox HWND ==="])
        self.debug(["window rect:", rect, "=> w,h =", rect[2]-rect[0], "x", rect[3]-rect[1]])
        self.debug(["client rect:", client, "=> w,h =", client[2]-client[0], "x", client[3]-client[1]])
        ### --- DEBUG INFO END --- ###