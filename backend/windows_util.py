import pyautogui
import win32gui
from . import initializers

def initWindow(title: str):
    hwnd = win32gui.FindWindow(None, title)
    while hwnd is None:
        print(f"Cannot find {title}, most likely not opened or a rare bug. Redoing...")
        hwnd = win32gui.FindWindow(None, title)
    return hwnd

def resolutionMid(window_width: int, window_height: int):
    screen_resolution = pyautogui.size()
    x = (screen_resolution.width - window_width) // 2 # 1000x700 since roblox is at 800x600
    y = (screen_resolution.height- window_height) // 2 # this 1000x700 is primarily for the qt application
    middle_screen = (x, y)
    return middle_screen

def getWindowRes(title: str):
    game_res = initializers.resolutions.get(title)
    if game_res is None:
        print(f"Critical bug in initializers, no known names as {title}")
        return
    return game_res