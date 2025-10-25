import cv2
import numpy as np
from pathlib import Path

class FindCoordinate():
    def __init__(self, mode: str, game_config: dict, logging: object):
        self.game_name = game_config["game_images"]
        self.mode = mode
        self.coordinates = []
        self.folder_dir = Path(f"Images/{self.game_name}/{self.mode}")

    def getCoordinate(self):
        #picture = self.folder_dir / {self.mode}
        picture = Path(f"Images/guardians/summer/summer_event.png")
        picture_np = cv2.imread(str(picture))
        if picture_np is None:
            print("NONE")
        cv2.imshow("Select Coordinate", picture_np)
        cv2.setMouseCallback("Select Coordinate", self.mouseCallback)
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key != 255:
                break
        cv2.destroyAllWindows()
        
        print(self.coordinates)
        

    def mouseCallback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.coordinates.append((x,y))
            cv2.rectangle
            
            

def greet():
    print("Hello")

s = "hello"
d = {
    "game_images": "hello"
}

l = FindCoordinate(s, d, greet)
l.getCoordinate()