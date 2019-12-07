import os

import dlib
import cv2
from imutils import face_utils


class FaceIndexes:
    NoseTip = 30
    NoseUnder = 33
    MouthTopCenter = 51
    MouthLeft = 48
    MouthRight = 54


class Face(object):
    def __init__(self, rect, mask, name=""):
        self.rect = rect
        self.mask = mask
        self.moustache = None


class FaceDetector():
    def __init__(self):
        # initialize dlib's face detector (HOG-based) and then create
        # the facial landmark predictor
        self.detector = dlib.get_frontal_face_detector()
        root_dir = os.path.dirname(__file__)
        model_path = f"{root_dir}{os.path.sep}data{os.path.sep}unzipped.dat"
        self.predictor = dlib.shape_predictor(model_path)

    def get_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = []
        rects = self.detector(gray, 1)
        for rect in rects:
            face = Face(rect, self.get_face_dots(gray, rect))
            faces.append(face)
        return faces

    def get_face_dots(self, gray_in, rect):
        shape = self.predictor(gray_in, rect)
        shape = face_utils.shape_to_np(shape)
        return shape
