import cv2
import numpy as np
from pathlib import Path
import win32api
import autoit

class FindCoordinate():
    def __init__(self, mode: str, game_config: dict, logging: object, unit_window: object):
        self.game_name = game_config["game_images"]
        self.mode = mode
        self.logging = logging
        self.unit_window = unit_window.returnUnitButtons()
        self.coordinates = None
        self.folder_dir = Path(f"Images/{self.game_name}/{self.mode}/{self.mode}.png")
        if self.folder_dir.absolute():
            print(f"Current folder to look in is: {self.folder_dir.absolute()}")
            self.logging.debug_message(f"Current looking in: {self.folder_dir.absolute()}")
        else:
            print(f"Folder: {self.mode} could not be found.")
            self.logging.debug_message(f"Folder: {self.mode} could not be found.")
        print(f"The path exists: {self.folder_dir.exists()}")
        self.logging.debug_message(f"The path exists: {self.folder_dir.exists()}")
        for index, unit in enumerate(self.unit_window):
            button = unit["button"]
            button.clicked.connect(lambda _, i=index: self.saveCoordinate(i))
        

    def getCoordinate(self):
        picture = self.folder_dir
        picture_np = cv2.imread(str(picture))
        if picture_np is None:
            print("NONE")
        cv2.imshow("Select Coordinate", picture_np)
        cv2.setMouseCallback("Select Coordinate", self.mouseCallback)
        while True:
            cv2.waitKey(1) & 0xFF
            if win32api.GetKeyState(0x01) < 0: 
                break
        cv2.destroyAllWindows()
        
        
    def saveCoordinate(self, index):
        self.getCoordinate()
        if self.coordinates:
            x, y = self.coordinates
            self.unit_window[index]["x"].setText(str(x))
            self.unit_window[index]["y"].setText(str(y))
            print(f"Saved ({x}, {y}) to Unit {index + 1}")
        
        

    def mouseCallback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.coordinates = (x, y)