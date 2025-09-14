import pyautogui
import win32gui
from . import initializers
import win32con
import win32gui

def initWindow(title: str):
    hwnd = win32gui.FindWindow(None, title)
    while hwnd is None:
        print(f"Cannot find {title}, most likely not opened or a rare bug. Redoing...")
        hwnd = win32gui.FindWindow(None, title)
    return hwnd

def resolutionMid(window_width: int, window_height: int):
    screen_resolution = pyautogui.size()
    if window_width is None or window_height is None:
        print("Critical bug in windows_util, window_width or window_height is None. Perhaps the game is not open.")
        return
    x = (screen_resolution.width - window_width) // 2 # 1000x700 since roblox is at 800x600
    y = (screen_resolution.height- window_height) // 2 # this 1000x700 is primarily for the qt application
    middle_screen = (x, y)
    return middle_screen

def getWindowRes(title: str):
    game_res = initializers.resolutions.get(title)
    if game_res is None:
        print(f"Critical bug in initializers, no known names as {title} or {title} is not open yet.")
        return
    return game_res

def setupattachWindow(hwnd, container): # attaches roblox window to qt application
        current_style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        new_style = current_style & ~(
            win32con.WS_CAPTION | 
            win32con.WS_THICKFRAME | 
            win32con.WS_MINIMIZEBOX | 
            win32con.WS_MAXIMIZEBOX | 
            win32con.WS_SYSMENU
            ) # removes title bar and border
        win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, new_style)
        win32gui.SetParent(hwnd, int(container.winId())) # set qt window as parent application and roblox as child, so if user decides to move qt application roblox also moves
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE) #Grabs HWND and uses SW_RESTORE to prevent minimization
        win32gui.SetWindowPos(hwnd, None, 0, 0, initializers.width, initializers.height, win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED)
        return container
    
def removeParent(hwnd): # removes parent qt, restore bars and headers, roblox returns to the middle of the screen via resolutionMid()
    width, height = resolutionMid(initializers.width, initializers.height)
    win32gui.SetParent(hwnd, None)
    current_style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    new_style = current_style | (
        win32con.WS_CAPTION | 
        win32con.WS_THICKFRAME | 
        win32con.WS_MINIMIZEBOX | 
        win32con.WS_MAXIMIZEBOX | 
        win32con.WS_SYSMENU
        ) # adds title bar and border back
    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, new_style)
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE) #Grabs HWND and uses SW_RESTORE to prevent minimization
    win32gui.SetWindowPos(hwnd, None, width, height, initializers.width, initializers.height, win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED)