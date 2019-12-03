import dlib
import numpy as np
import cv2
import dlib
from imutils import face_utils

class FaceIndexes:
    NoseTip = 30
    NoseUnder = 33
    MouthTopCenter = 51
    MouthLeft = 48
    MouthRight = 54

class FaceDetector():
    def __init__(self):
        # initialize dlib's face detector (HOG-based) and then create
        # the facial landmark predictor
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("data\\unzipped.dat")

    def get_faces(self, gray_in):
        return self.detector(gray_in, 1)

    def get_face_dots(self, gray_in, rect):
        shape = self.predictor(gray_in, rect)
        shape = face_utils.shape_to_np(shape)
        return shape

    def draw_mask(self, shape, out, important_idx=[]):
        for i, (x, y) in enumerate(shape):
            if i in important_idx:
                color = (255, 0, 0)
            else:
                color = (0, 0, 255)
            cv2.circle(out, (x, y), 1, color, -1)

    def draw_bounding_rect(self, rect, out, name = ""):
        x, y, w, h = face_utils.rect_to_bb(rect)
        cv2.rectangle(out, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(out, f"Face {name}", (x - 10, y - 10),
	    	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
