import cv2 as cv
import numpy as np
import time
import os
from pathlib import Path
from . import ORB

class ImageProcessor():
    '''
    setup for the fast screenshot(mss), folder directory(folder_dir), which monitor to use(monitor[1] because
    monitor[0] would mean every single display, but monitor[1] focuses on primary display), thresh set as 0.85 since 0.90
    is strict, game_images comes from the partial set in mainwindow.py where each game should be linking towards a
    different folder in Images. ORB is a fallback image detection system incase original template_matching fails.
    '''
    def __init__(self, game_images=None, max_thresh = 0.85):
        self.max_thresh = max_thresh
        self.game_images = game_images
        self.folder_dir = Path(f"Images/{self.game_images}")
        self.center_x = None
        self.center_y = None
        self._init_images()
        self.orb = ORB.OrbHandler()

    def _init_images(self): #Initialize grey images
        '''
        caches grey images for easier runtime.
        steps:
        1. set up dictionary of empty grey_images
        2. print debug statements for where the program fails
        3. use glob to see what images are being seen in .png format
        4. for image in stored_images every file in folder_dir gets read and turns into grey using read_image(filename)
        '''
        self.templates_grey = {}
        print(f"Current working directory: {os.getcwd()}")
        print(f"Looking for images in: {self.folder_dir}")
        print(f"Absolute path: {self.folder_dir.absolute()}")
        print(f"Path exists: {self.folder_dir.exists()}")
        stored_images = self.folder_dir.glob('*.png') #reads every single image file saved as .png using .glob
        for image in stored_images: #loops through .png files and cv reads, if not none, store on templates_grey using filename
            filename = image.name
            self.read_image(filename)
    
    def read_image(self, filename): # Reads image and converts to grey, stores in templates_grey
        '''
        turns every img into gray.
        steps:
        1. set image path, this is based on initializers and set on partial located in mainwindow.py
        2. read image first
        3. turn it into gray
        4. the coloured version of the image gets replaced by the gray image in templates_grey
        '''
        image_path = self.folder_dir / filename
        if not image_path.exists():
            print(f"Image file {filename} does not exist in {self.folder_dir}.")
        img = cv.imread(str(image_path))
        if img is None:
            print(f"Failed to read image {filename}.")
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        self.templates_grey[filename] = gray_img
        return gray_img

    def screenshot(self, rect, mss): #Returns gray image of the current game
        '''
        responsible for what the computer sees
        steps:
        1. get rect, grab x and y (relative to screen) and size of the game's width and height
        2. try up to 5 times
        3. return as a gray image
        '''
        try:
            if rect is not None: #grabs region from init.window_info()
                final_rect = {
                    "left": rect[0],
                    "top": rect[1],
                    "width": rect[2] - rect[0],
                    "height": rect[3] - rect[1]
                }
            else:
                print("Rect is None in 'screenshot' in template_matching.py")
        except Exception as e:
            print(f"Error defining screenshot rectangle: {e}, returning None.") # no point in retrying this. GetWindowsRect() should work always.
        for i in range(5): # try to capture screenshot up to 5 times
            try:
                temp_img = mss.grab(final_rect)
                img_np = np.array(temp_img)
                if img_np.size == 0:
                    print("Captured image is empty.")
                print(f"[DEBUG] Screenshot rect: {final_rect}, image shape: {img_np.shape}")
                return cv.cvtColor(img_np, cv.COLOR_BGRA2GRAY)
            except Exception as e:
                print(f"Error capturing screenshot (attempt {i+1}/5): {e}")
                time.sleep(0.1)
        print("Failed to capture screenshot after 5 attempts.")
        
    def both_methods(self, template_filename: str, rect, mss): # Uses both methods of template_matching and a fallback of ORB.
        '''
        includes both template matching and ORB
        steps:
        1. get screenshot based on what rect is given (located in frontend)
        2. given filename is being searched if it exists in templates_grey
        3. grab confidence value
        4. centers the x and y coords
        5. return location
        ------ IF FAILS ------
        6. ORB takes the wheel and compares current gray image to the template_img
        7. gives center by adding x and y of game to the already centered screen (explanation: We must add x and y so we
        know where the game is located.)
        '''
        current_gray = self.screenshot(rect, mss)
        if current_gray is None:
            print("Screenshot has failed. Please fix.")
            return
        template_img = self.templates_grey.get(template_filename) #uses the templates_grey dictionary to find
                                                                    #specific filename
        if template_img is not None:
            result = cv.matchTemplate(current_gray, template_img, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

            if max_val >= self.max_thresh:
                self.center_x = rect[0] + max_loc[0] + (template_img.shape[1] // 2)
                self.center_y = rect[1] + max_loc[1] + (template_img.shape[0] // 2)
                print(f"Found values: X = {self.center_x}, Y = {self.center_y} with confidence level of {max_val}")
                location = (self.center_x, self.center_y)
                return location
            else:
                print(f"Confidence level was too low using {template_filename} in 'template_matching' in template_matching.py. Trying ORB...")
                ### ORB ###
                center, corners = self.orb.orb_matching(template_img, current_gray)
                if center is None or center == (0,0):
                    print("ORB has failed. Reconnection is required.")
                    return None
                else:
                    self.center_x = rect[0] + center[0]
                    self.center_y = rect[1] + center[1]
                    print(f"Found location using ORB in coordinates X: {self.center_x}, and Y: {self.center_y}")
                    location = (self.center_x, self.center_y)
                    return location
            
        else:
            print(f"Image: {template_filename} was not found in 'template_matching' in template_matching.py")
    
    
    
    
        '''def template_matching(self, template_filename: str, rect): #Returns location of what to click
        current_gray = self.screenshot(rect)
        if current_gray is None:
            print("Problems regarding screenshot(), immediate fix is required, shutting down program.")
            os._exit(1)
        template_img = self.templates_grey.get(template_filename) #uses the templates_grey dictionary to find
                                                                    #specific filename
        if template_img is not None:
            result = cv.matchTemplate(current_gray, template_img, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        else:
            print(f"Image {template_filename} was not found in 'template_matching' in template_matching.py")
            return False

        if max_val >= self.max_thresh:
            self.center_x = rect[0] + max_loc[0] + (template_img.shape[1] // 2)
            self.center_y = rect[1] + max_loc[1] + (template_img.shape[0] // 2)
            print(f"Found values: X = {self.center_x}, Y = {self.center_y} with confidence level of {max_val}")
            location = (self.center_x, self.center_y)
            return location
        else:
            print(f"Confidence level was too low using {template_filename} in 'template_matching' in template_matching.py")
            return False''' # Just to save the code in case I need it for something.