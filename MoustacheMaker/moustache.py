import math

import numpy as np
import cv2
from imutils import rotate_bound

from face_detector import FaceIndexes

class Moustache():
    """Draws and animates a moustache on an image"""
    def __init__(self, mask, picture, name=""):
        self.start_center = (0,0)
        self.start_height = 0
        self.start_angle = 0
        self.current_center = self.calculate_averaged_center(mask)
        self.current_height = 1
        self.current_angle = self.calculate_angle(mask)
        self.finish_center = (0,0)
        self.finish_height = 0
        self.finish_angle = 0
        self.centers = []
        self.heights = []
        self.mask = None
        self.name = name
        self.picture = picture

    @staticmethod
    def calculate_averaged_center(mask):
        xy = sum([mask[FaceIndexes.NoseTip], mask[FaceIndexes.MouthTopCenter], mask[FaceIndexes.NoseUnder]])/3.0
        return [int(round(x)) for x in xy]

    @staticmethod
    def calculate_averaged_height(mask):
        xy = mask[FaceIndexes.MouthTopCenter] - mask[FaceIndexes.NoseUnder]
        print()
        return int(round(math.sqrt(xy[0]*xy[0] + xy[1] * xy[1])))

    @staticmethod
    def calculate_angle(mask):
        delta = mask[FaceIndexes.NoseTip] - mask[FaceIndexes.MouthTopCenter]
        return math.atan2(delta[1], delta[0])*180/math.pi + 90

    def __len__(s):
        return len(self.centers)


    def add_frame(self, mask):
        self.start_center = self.current_center
        self.start_height = self.current_height
        self.start_angle = self.current_angle
        self.finish_center = self.calculate_averaged_center(mask)
        self.finish_height = self.calculate_averaged_height(mask)
        self.finish_angle = self.calculate_angle(mask)

    def reset_motion(self):
        self.start_center = self.current_center
        self.start_height = self.current_height
        self.start_angle = self.current_angle
        self.finish_center = self.current_center
        self.finish_height = self.current_height
        self.finish_angle = self.current_angle
        self.angles = [self.current_angle for _ in self.angles]
        self.centers = [self.current_center for _ in self.centers]
        self.heights = [self.current_height for _ in  self.heights]


    def get_name(self):
        return self.name

    def set_goal(self, frames):
        center_delta = np.divide(np.subtract(self.finish_center,self.start_center), frames)
        self.centers = [np.add(self.start_center, np.multiply(i,center_delta)) for i in range(0,frames)]
        self.centers.append(self.finish_center)
        height_delta = (self.finish_height - self.start_height)/frames
        self.heights = [self.start_height + i*height_delta for i in range(0,frames)]
        self.heights.append(self.finish_height)
        angle_delta = (self.finish_angle - self.start_angle)/frames
        self.angles = [self.start_angle + i*angle_delta for i in range(0,frames)]
        self.angles.append(self.finish_angle)
        
    
    def draw_moustache(self, out, cycle):
        self.current_center = np.round(self.centers[cycle])
        self.current_height = round(self.heights[cycle])
        self.current_angle = round(self.angles[cycle])
        raw = self.picture.picture
        height_ratio = self.current_height/raw.shape[1] * self.picture.scale_fudge
        scaled = cv2.resize(raw, None, fx=height_ratio, fy=height_ratio)
        rotated = rotate_bound(scaled, self.current_angle)
        if self.picture.do_blur:
            rotated = cv2.blur(rotated, self.picture.blur_size)
        x1 = int(round((self.current_center[0]-rotated.shape[1]//2) * self.picture.offset[0]))
        y1 = int(round((self.current_center[1]-rotated.shape[0]//2) * self.picture.offset[1]))
        x2 = x1 + rotated.shape[1]
        y2 = y1 + rotated.shape[0]
        alpha_s = rotated[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            out[y1:y2, x1:x2, c] = (alpha_s * rotated[:, :, c] +
                              alpha_l * out[y1:y2, x1:x2, c])

    def draw_moustache_diagnostics(self, out):
        height = self.current_height
        height = int(round(height/2.0))
        cross_length = int(round(height/4.0))
        cross_thickness = 2
        color = (0, 55, 200)
        center = (int(self.current_center[0]), int(self.current_center[1]))
        #draw center cross
        cv2.line(
            out, 
            (center[0]-cross_length, center[1]),
            (center[0]+cross_length, center[1]),
            color,
            thickness = cross_thickness
        )
        cv2.line(
            out, 
            (center[0], center[1]-cross_length),
            (center[0], center[1]+cross_length),
            color,
            thickness = cross_thickness
        )
        #draw horizontal lines
        cv2.line(
            out, 
            (center[0]-height, center[1]+height),
            (center[0]+height, center[1]+height),
            color,
            thickness = cross_thickness
        )
        cv2.line(
            out, 
            (center[0]-height, center[1]-height),
            (center[0]+height, center[1]-height),
            color,
            thickness = cross_thickness
        )

    @staticmethod
    def get_landmark_idx():
        picture_indexes = [ 
            FaceIndexes.MouthLeft, 
            FaceIndexes.MouthTopCenter,
            FaceIndexes.MouthRight,
            FaceIndexes.NoseUnder,
            FaceIndexes.NoseTip
           ]
        return picture_indexes

