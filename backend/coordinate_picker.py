import cv2
import numpy as np
from pathlib import Path
import win32api
from . import coordinates_json

class FindCoordinate():
    def __init__(self, mode: str, game_config: dict, logging: object, unit_window: object):
        self.game_name = game_config["game_images"]
        self.mode = mode
        self.logging = logging
        self.unit_window = unit_window.returnUnitButtons()
        self.loadExistingCoordinates()
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
        '''
        This function utilizes OpenCV's mouse callback to get the location of the left click input of a mouse.
        '''
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
        
    def loadExistingCoordinates(self):
        '''
        This function will read the saved locations inside of coordinates.json and apply it to the
        empty box inside of unit_window's QLineEdits.
        '''
        data = coordinates_json.loadFromJson()
        if data and len(data) > 0 and "Unit" in data[0]:
            units = data[0]["Unit"]
            for index, unit_data in enumerate(self.unit_window):
                key = str(index + 1)
                if key in units:
                    x, y = units[key]
                    unit_data["x"].setText(str(x))
                    unit_data["y"].setText(str(y))
    
    def saveCoordinate(self, index):
        '''
        params: index
        Root is in unit_window. This function is possible due to the dot operator from PyQt (clicked.connect) and utilizing lambda
        to catch the function call, freeze each individual buttons saved inside of unit_windows.returnUnitButton() and save those locations
        inside of coordinates.json.
        '''
        self.getCoordinate()
        if self.coordinates:
            x, y = self.coordinates
            self.unit_window[index]["x"].setText(str(x))
            self.unit_window[index]["y"].setText(str(y))
            print(f"Saved ({x}, {y}) to Unit {index + 1}")
            
            coordinates_json.saveToJson(index, x, y)
            self.logging.log_message(f"Saved as {x} and {y} to Unit {index + 1}")
        

    def mouseCallback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.coordinates = (x, y)