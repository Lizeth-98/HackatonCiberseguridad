# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 17:00:26 2024

@author: cs940
"""

import cv2

class Camera:
    def __init__(self):
        self.video_capture = cv2.VideoCapture(1)
        
    def get_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            return frame
        else:
            return None
        
    def release(self):
        self.video_capture.release()
