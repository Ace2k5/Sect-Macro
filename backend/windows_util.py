import pyautogui
import win32gui
import win32con

def initWindow(title: str) -> int:
    '''
    simply grabs hwnd of screen which is based on initializers. (implementation location is in setupRobloxIntegration)
    steps:
    1. grab hwnd from the arg
    2. return hwnd
    '''
    hwnd = win32gui.FindWindow(None, title)
    if hwnd is None or hwnd == 0:
        raise RuntimeError(f"Window not found, HWND is: {hwnd}")
    return hwnd

def resolutionMid(window_width: int, window_height: int) -> tuple:
    '''
    Centers the application in the middle of the monitor's screen resolution.
    steps:
    1. grab user's current screen res in pyautogui
    2. window_width and height depends on args based on generic game window (currently robloxwindow.py)
    3. formula uses (screen_res_x - gui_window_width) // 2
                    (screen_res_y - gui_window_height) // 2 to center window, this gives us x and y because now we know
                    where the top left window of the gui is located relative to the screen
    4. set a tuple and return middle_screen
    '''
    screen_resolution = pyautogui.size()
    if window_width is None or window_height is None:
        raise ValueError(f"Critical bug in windows_util, window_width or window_height is None: {window_height}, {window_width}")
    x = (screen_resolution.width - window_width) // 2 # 1000x700 since roblox is at 800x600
    y = (screen_resolution.height- window_height) // 2 # this 1000x700 is primarily for the qt application
    center_coords = (x, y)
    return center_coords

def setupattachWindow(hwnd, container: object, width: int, height: int): # attaches roblox window to qt application
        '''
        Removes borders and attaches to a GUI
        steps:
        1. get current look of window
        2. remove window borders
        3. set the new style
        4. set it as a child of container(which comes from robloxwindows.py in the setupQt func)
        5. restore to prevent minimization
        6. setwindowpos by grabbing hwnd, set 0 to 0 so it fits in container -
        - width and height(3,4), noZorder means no layering and check if frame has changed.
        '''
        if hwnd is None:
             raise ValueError(f"HWND problem in setupattachWindow {hwnd}")
        if container is None:
             raise RuntimeError(f"Container problem in setupattachWindow {container}")
        current_style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        new_window_style_flags = current_style & ~(
            win32con.WS_CAPTION | 
            win32con.WS_THICKFRAME | 
            win32con.WS_MINIMIZEBOX | 
            win32con.WS_MAXIMIZEBOX | 
            win32con.WS_SYSMENU
            ) # removes title bar and border
        win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, new_window_style_flags)
        win32gui.SetParent(hwnd, int(container.winId())) # set qt window as parent application and roblox as child, so if user decides to move qt application roblox also moves
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE) #Grabs HWND and uses SW_RESTORE to prevent minimization
        win32gui.SetWindowPos(hwnd, None, 0, 0, width, height, win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED)
        return container
    
def removeParent(hwnd, width: int, height: int): # removes parent qt, restore bars and headers, roblox returns to the middle of the screen via resolutionMid()
    '''
    Removes the embedding of the chosen application when user exits gui.
    steps:
    1. get x and y from resolutionMid, resolutionMid centers the screen, args required are the game resolution 
        located in initializers.py (Implementation is in robloxwindow.py, closeEvent())
    2. set hwnd of chosen application to None for safe deattachment
    3-5. reset current style back to standardized window application
    6. show window to user
    7. center the window and flag that the screen has changed.
    '''
    if hwnd is None:
        raise ValueError(f"HNWD problem in removeParent: {hwnd}")

    x, y = resolutionMid(width, height)
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
    win32gui.SetWindowPos(hwnd, None, x, y, width, height, win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED)
    return