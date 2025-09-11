import pyautogui
from frontend import guardians

class windowsUtils():
    def __init__(self):
          self.resolutionMid()

    def resolutionMid(self):
            screen_resolution = pyautogui.size()
            x = (screen_resolution.width - 1000) // 2 # 1000x700 since roblox is at 800x600
            y = (screen_resolution.height- 700) // 2 # this 1000x700 is primarily for the qt application
            middle_screen = (x, y)
            return middle_screen