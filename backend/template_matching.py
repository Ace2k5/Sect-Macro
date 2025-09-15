import cv2 as cv
import numpy as np
import time
import matplotlib.pyplot as plt
import os
from pathlib import Path
from mss import mss
from . import initializers
from frontend import guardians, mainwindow
folder_dir = Path("Images/")

class ImageProcessor():
    def __init__(self, max_thresh = 0.85):
        self.max_thresh = max_thresh
        self.mss = mss()
        self.mon_region = self.mss.monitors[1]
        self.center_x = None
        self.center_y = None
        self._init_images()

    def _init_images(self): #Initialize grey images
        self.templates_grey = {}
        print(f"Current working directory: {os.getcwd()}")
        print(f"Looking for images in: {folder_dir}")
        print(f"Absolute path: {folder_dir.absolute()}")
        print(f"Path exists: {folder_dir.exists()}")
        stored_images = Path(folder_dir).glob('*.png') #reads every single image file saved as .png using .glob
        for image in stored_images: #loops through .png files and cv reads, if not none, store on templates_grey using filename
            filename = image.name
            temp = cv.imread(str(image))
            if temp is not None:
                img_gray = cv.cvtColor(temp, cv.COLOR_BGR2GRAY)
                self.templates_grey[filename] = img_gray
            else:
                print("Problem in initializing images.")

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
            print(f"Error defining screenshot rectangle: {e}, returning None.")
            return None
        for i in range(5):
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
        print("Failed to capture screenshot after 5 attempts.")
        return None
        
    def template_matching(self, template_filename: str, rect): #Returns location of what to click
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
            return False
        

                
