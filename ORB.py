import cv2 as cv
import numpy as py
import time
import matplotlib.pyplot as plt
import os
from pathlib import Path

class OrbHandler():
    def __init__(self, eValue = 1000, threshold = 0.90, currentThreshold = 0.00):
        self.eValue = eValue
        self.threshold = threshold
        self.currentThreshold = currentThreshold

    def orb(self):
        root = os.getcwd()
        imgPath = os.path.join(root, "Images", "currentScreen.jpg")
        imgGray = cv.imread(imgPath, cv.IMREAD_GRAYSCALE)

        orb = cv.ORB_create(nfeatures=self.eValue)
        keypoints = orb.detect(imgGray, None)
        keypoints, _ = orb.compute(imgGray, keypoints)
        imgGray = cv.drawKeypoints(imgGray, keypoints, None, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    def orbDetection(self):
        
        if self.currentThreshold >= self.threshold


        #WIP, MUST DO TEMPLATE MATCHING FIRST.
