import cv2 as cv
import numpy as np
import time
import matplotlib.pyplot as plt
import os
from pathlib import Path
from mss import mss
import initializers as init

folder_dir = Path("Sect/Images/game_elements")

class ImageProcessor():
    def __init__(self, max_thresh = 0.85):
        self.max_thresh = max_thresh
        self.mss = mss()
        self.mon_region = self.mss.monitors[1]
        self.center_x = None
        self.center_y = None
        self._init_images()
        self.rect = init.window_info()

    def _init_images(self): #Initialize grey images
        self.templates_grey = {}
        stored_images = Path(folder_dir).glob('*.png') #reads every single image file saved as .png using .glob
        for image in stored_images: #loops through .png files and cv reads, if not none, store on templates_grey using filename
            filename = image.name
            temp = cv.imread(str(image))
            if temp is not None:
                img_gray = cv.cvtColor(temp, cv.COLOR_BGR2GRAY)
                self.templates_grey[filename] = img_gray
            else:
                print("Problem in initializing images.")

    def screenshot(self, region=None): #Returns gray image of the current game
        self.rect = init.window_info() #FORCE ROBLOX ON TOP and gives window information such as res
        while self.rect is None:
            time.sleep(0.2)
            self.rect = init.window_info()
        if region is None and self.rect: #grabs region from init.window_info()
            region = {
                "left": self.rect[0],
                "top": self.rect[1],
                "width": self.rect[2] - self.rect[0],
                "height": self.rect[3] - self.rect[1]
            }
        temp_img = self.mss.grab(region)

        img_np = np.array(temp_img)
        return cv.cvtColor(img_np, cv.COLOR_BGRA2GRAY)
    
    def template_matching(self, template_filename: str): #Returns location of what to click
        current_gray = self.screenshot()
        template_img = self.templates_grey.get(template_filename) #uses the templates_grey dictionary to find
                                                                    #specific filename
        if template_img is not None:
            result = cv.matchTemplate(current_gray, template_img, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        else:
            print(f"Image {template_filename} was not found in 'template_matching' in template_matching.py")
            return False

        if max_val >= self.max_thresh:
            self.center_x = max_loc[0] + (template_img.shape[1] // 2)
            self.center_y = max_loc[1] + (template_img.shape[0] // 2)
            print(f"Found values: X = {self.center_x}, Y = {self.center_y} with confidence level of {max_val}")
            location = (self.center_x, self.center_y)
            return location
        else:
            print(f"Confidence level was too low using {template_filename} in 'template_matching' in template_matching.py")
            return False
        

                
