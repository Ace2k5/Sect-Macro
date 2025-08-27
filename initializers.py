import win32gui
import win32con
import time

def window_info():
    try:
        hwnd = win32gui.FindWindow(None, "Roblox")
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE) #Grabs HWND and uses SW_RESTORE to prevent minimization
        rect = win32gui.GetWindowRect(hwnd)
        x, y = rect[0], rect[1]
        win32gui.MoveWindow(hwnd, x, y, 800, 600, True) #Makes sure 800x600 is constant. Grabs x and y from rect
        win32gui.SetForegroundWindow(hwnd) #Makes sure roblox handle is always the focus
        return win32gui.GetWindowRect(hwnd) #Returns left, top, right and bottom
    except Exception as e:
        print("There was a problem getting the Roblox windows handle, perhaps it is not open? Redoing..." \
        " (Most likely Roblox is not open.)")
        time.sleep(0.5)
        return None
