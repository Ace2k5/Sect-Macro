import cv2 as cv
import numpy as np
import time
import matplotlib.pyplot as plt
import os
from pathlib import Path

class OrbHandler():
    def __init__(self, nfeatures=1000, threshold=0.75, min_matches=10):
        self.orb = cv.ORB_create(nfeatures=nfeatures)
        self.bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=False)
        self.threshold = threshold
        self.min_matches = min_matches

    def orb_matching(self, template_img, gray_img):
        """
        Perform ORB-based template matching between template and target image.
        
        Args:
            template_img: Template image (grayscale)
            gray_img: Target image to search in (grayscale)
            
        Returns:
            tuple: ((center_x, center_y), bounding_box_corners) or (None, None) if no match
        """
        # Detect and compute keypoints and descriptors
        kp1, des1 = self.orb.detectAndCompute(template_img, None)
        kp2, des2 = self.orb.detectAndCompute(gray_img, None)
        
        # Check if descriptors were found
        if des1 is None or des2 is None:
            print("No descriptors found in one or both images")
            return None, None
        
        if len(des1) < 2 or len(des2) < 2:
            print("Not enough descriptors for matching")
            return None, None
        
        try:
            # KNN match with k=2 for Lowe's ratio test
            matches = self.bf.knnMatch(des1, des2, k=2)
        except cv.error as e:
            print(f"Matching failed: {e}")
            return None, None
        
        # Filter matches that don't have 2 neighbors
        matches = [m for m in matches if len(m) == 2]
        
        if len(matches) == 0:
            print("No valid matches found")
            return None, None
        
        # Apply Lowe's ratio test
        good_matches = []
        for m, n in matches:
            if m.distance < self.threshold * n.distance:
                good_matches.append(m)
        
        print(f"Good matches: {len(good_matches)} / {len(matches)}")
        
        # Need enough points for reliable homography
        if len(good_matches) < self.min_matches:
            print(f"Not enough good matches ({len(good_matches)} < {self.min_matches})")
            return None, None
        
        # Extract matching points
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        
        # Find homography using RANSAC
        try:
            M, mask = cv.findHomography(src_pts, dst_pts, 
                                      method=cv.RANSAC, 
                                      ransacReprojThreshold=5.0,
                                      confidence=0.99,
                                      maxIters=2000)
        except cv.error as e:
            print(f"Homography computation failed: {e}")
            return None, None
        
        if M is None:
            print("Could not compute valid homography")
            return None, None
        
        # Get template corners and transform them
        h, w = template_img.shape[:2]
        template_corners = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
        
        try:
            transformed_corners = cv.perspectiveTransform(template_corners, M)
        except cv.error as e:
            print(f"Perspective transformation failed: {e}")
            return None, None
        
        # Calculate center of detected object
        center_x = int(np.mean(transformed_corners[:, 0, 0]))
        center_y = int(np.mean(transformed_corners[:, 0, 1]))
        
        return (center_x, center_y), transformed_corners
    
    def draw_matches(self, gray_img, center=None, corners=None): # only ever really needed for seeing what the computer sees
        """
        Utility function to visualize the matching results.
        """
        if center is None or corners is None:
            return gray_img
        
        # Convert to color for visualization
        result_img = cv.cvtColor(gray_img, cv.COLOR_GRAY2BGR)
        
        # Draw bounding box
        pts = np.int32(corners).reshape((-1, 1, 2))
        result_img = cv.polylines(result_img, [pts], True, (0, 255, 0), 3)
        
        # Draw center point
        cv.circle(result_img, center, 5, (0, 0, 255), -1)
        
        return result_img
