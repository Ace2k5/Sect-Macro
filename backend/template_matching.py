import cv2 as cv
import numpy as np
import time
import matplotlib.pyplot as plt
import os
from pathlib import Path
from mss import mss
from . import initializers, ORB
from frontend import RobloxWindow, mainwindow
folder_dir = Path("Images/")

class ImageProcessor():
    def __init__(self, max_thresh = 0.85):
        self.max_thresh = max_thresh
        self.mss = mss()
        self.mon_region = self.mss.monitors[1]
        self.center_x = None
        self.center_y = None
        self._init_images()
        self.orb = ORB.OrbHandler()
        self.guardianWindow = mainwindow.button

    def _init_images(self): #Initialize grey images
        self.templates_grey = {}
        print(f"Current working directory: {os.getcwd()}")
        print(f"Looking for images in: {folder_dir}")
        print(f"Absolute path: {folder_dir.absolute()}")
        print(f"Path exists: {folder_dir.exists()}")
        stored_images = Path(folder_dir).glob('*.png') #reads every single image file saved as .png using .glob
        for image in stored_images: #loops through .png files and cv reads, if not none, store on templates_grey using filename
            filename = image.name
            self.read_image(filename)
    
    def read_image(self, filename): # Reads image and converts to grey, stores in templates_grey
        image_path = folder_dir / filename
        if not image_path.exists():
            raise RuntimeError(f"Image file {filename} does not exist in {folder_dir}.")
        img = cv.imread(str(image_path))
        if img is None:
            raise RuntimeError(f"Failed to read image {filename}.")
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        self.templates_grey[filename] = gray_img
        return gray_img

    def screenshot(self, rect): #Returns gray image of the current game
        try:
            if rect != None: #grabs region from init.window_info()
                final_rect = {
                    "left": rect[0],
                    "top": rect[1],
                    "width": rect[2] - rect[0],
                    "height": rect[3] - rect[1]
                }
            else:
                raise RuntimeError("Rect is None in 'screenshot' in template_matching.py")
        except Exception as e:
            raise RuntimeError(f"Error defining screenshot rectangle: {e}, returning None.") # no point in retrying this. GetWindowsRect() should work always.
        for i in range(5): # try to capture screenshot up to 5 times
            try:
                temp_img = self.mss.grab(final_rect)
                img_np = np.array(temp_img)
                if img_np.size == 0:
                    raise RuntimeError("Captured image is empty.")
                print(f"[DEBUG] Screenshot rect: {final_rect}, image shape: {img_np.shape}")
                return cv.cvtColor(img_np, cv.COLOR_BGRA2GRAY)
            except Exception as e:
                print(f"Error capturing screenshot (attempt {i+1}/5): {e}")
                time.sleep(0.1)
        raise RuntimeError("Failed to capture screenshot after 5 attempts.")
        
    def both_methods(self, template_filename: str, rect): # Uses both methods of template_matching and a fallback of ORB.
        current_gray = self.screenshot(rect)
        if current_gray is None:
            attempts = 0
            for i in range(5):
                current_gray = self.screenshot(rect)
                attempts += 1
                print(f"Attempt: {attempts}")
                if current_gray is not None:
                    break
            if current_gray is None:
                raise RuntimeError("All 5 attempts of getting a screenshot failed. Immediate fix is required.")
        template_img = self.templates_grey.get(template_filename) #uses the templates_grey dictionary to find
                                                                    #specific filename
        if template_img is not None:
            result = cv.matchTemplate(current_gray, template_img, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        else:
            raise RuntimeError(f"Image {template_filename} was not found in 'template_matching' in template_matching.py")

        if max_val >= self.max_thresh:
            self.center_x = rect[0] + max_loc[0] + (template_img.shape[1] // 2)
            self.center_y = rect[1] + max_loc[1] + (template_img.shape[0] // 2)
            print(f"Found values: X = {self.center_x}, Y = {self.center_y} with confidence level of {max_val}")
            location = (self.center_x, self.center_y)
            return location
        else:
            print(f"Confidence level was too low using {template_filename} in 'template_matching' in template_matching.py. Trying ORB...")
            center, corners = self.orb.orb_matching(template_img, current_gray)
            if center is None:
                print("redoing five times. There was a failure in orb matching.")
                attempts = 0
                for i in range(5):
                    center, corners = self.orb.orb_matching(template_img, current_gray)
                    attempts += 1
                    print(f"Attempt: {attempts}")
                    if center is not None:
                        break
            if center is None:
                raise RuntimeError("All ORB attempts have been failed, fix is required.")
        self.center_x = rect[0] + center[0]
        self.center_y = rect[1] + center[1]
        print(f"Found location using ORB in coordinates X: {self.center_x}, and Y: {self.center_y}")
        location = (self.center_x, self.center_y)
        return location
    
    
    
    
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