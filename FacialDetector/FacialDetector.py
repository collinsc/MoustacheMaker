"""Command line application to run the face detector on a webcam"""
import math


import numpy as np
import cv2
import dlib
from pykalman import UnscentedKalmanFilter
from imutils import face_utils


class Settings:
    PicturePath                 = None
    DrawFrame                   = False
    DrawMask                    = False
    DrawMoustacheDiagnostics    = False
    DrawMoustache               = True


class FaceIndexes:
    NoseTip = 30
    NoseUnder = 33
    MouthTopCenter = 51
    MouthLeft = 48
    MouthRight = 54


class MoustachePicture1():
    path = "moustaches\\moustache1.png"
    picture = cv2.imread(path,-1)
    offset = (1.0,1.05)
    scale_fudge=4.5


class Moustaches():
    def __init__(self, tolerance = 500, max_counts =30):
        self.moustaches = []
        self.counts = {}
        self.names = {}
        self.moustache_count = 0
        self.max_count = 5
        self.matched = {}

    def items(self):
        for moustache in self.moustaches:
            yield moustache


    @staticmethod
    def calculate_distance(p1,p2):  
        dist = math.sqrt((p2[0] - p1[0])**2 + (p2[0] - p1[0])**2)  
        return dist 

    def get_closest_moustache(self, mask, tolerance):
        center = Moustache.calculate_averaged_center(mask)
        min_dist = 1000000000
        out_moustache = None
        for moustache in self.moustaches:
            distance = abs(self.calculate_distance(center, moustache.center))
            if distance < min_dist and distance < tolerance:
                out_moustache = moustache
                self.matched[moustache] = True

        return out_moustache

    def add_moustache(self, name=None):
        self.moustache_count += 1
        if name is None:
            name = self.moustache_count
        moustache = Moustache(name=name)
        self.moustaches.append(moustache)
        self.counts[moustache]=0
        self.matched[moustache] = True
        return moustache



    def update(self):

        to_remove = []
        for moustache in self.moustaches:
            if not self.matched[moustache]:
                self.counts[moustache]  += 1
            self.matched[moustache] = False
            if self.counts[moustache] > self.max_count:
                to_remove.append(moustache)
        for moustache in to_remove:
            self.counts.pop(moustache)
            self.moustaches.remove(moustache)
            self.matched.pop(moustache)

class Moustache():
    """Smoothed moustache using a kalman filter"""
    def __init__(self, name="", picture = MoustachePicture1()):
        self.center = None
        self.height = None
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
        return int(round(xy[1]))

    def __len__(s):
        return len(self.centers)


    def add_frame(self, mask):
        self.center = self.calculate_averaged_center(mask)
        self.height = self.calculate_averaged_height(mask)



    def get_name(self):
        return self.name
    
    def draw_moustache(self, out):
        picture = self.picture.picture
        height = self.height
        height_ratio = height/picture.shape[1] * self.picture.scale_fudge
        scaled = cv2.resize(picture, None, fx=height_ratio, fy=height_ratio)
        center = self.center
        x1 = int(round((center[0]-scaled.shape[1]//2) * self.picture.offset[0]))
        y1 = int(round((center[1]-scaled.shape[0]//2) * self.picture.offset[1]))
        x2 = x1 + scaled.shape[1]
        y2 = y1 + scaled.shape[0]
        alpha_s = scaled[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            out[y1:y2, x1:x2, c] = (alpha_s * scaled[:, :, c] +
                              alpha_l * out[y1:y2, x1:x2, c])

    def draw_moustache_diagnostics(self, out):
        height = self.height
        height = int(round(height/2.0))
        cross_length = int(round(height/4.0))
        cross_thickness = 2
        color = (0, 55, 200)
        center = self.center
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

def process_keys():
    keys = cv2.waitKey(1) & 0xFF
    if keys == ord('q'):
        return True
    if keys == ord('d'):
        #turn on diagnostics
        Settings.DrawFrame                  = not Settings.DrawFrame
        Settings.DrawMask                   = not Settings.DrawMask
        Settings.DrawMoustacheDiagnostics   = not Settings.DrawMoustacheDiagnostics
    if keys == ord('m'):
        Settings.DrawMoustache              = not Settings.DrawMoustache
    return False

def main():
    cap = cv2.VideoCapture(0)
    detector = FaceDetector()
    moustaches = Moustaches()
    p_count = 0
    while(True):
        # Capture frame-by-frame
        if Settings.PicturePath is not None:
            frame = cv2.imread(Settings.PicturePath)
        else:
            ret, frame = cap.read()
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector.get_faces(gray)

        for rect in rects:
            mask = detector.get_face_dots(gray, rect)
            hdim = rect.right() - rect.left()
            vdim = rect.bottom() - rect.top()
            moustache = moustaches.get_closest_moustache(mask, max([hdim,vdim ]))
            if moustache is None:
                moustache = moustaches.add_moustache()
            moustache.add_frame(mask)
            if Settings.DrawFrame:
                detector.draw_bounding_rect(rect, frame,moustache.get_name())
            if Settings.DrawMask:
                detector.draw_mask(mask, frame, Moustache.get_landmark_idx())
        for moustache in moustaches.items():
            if Settings.DrawMoustache:
                moustache.draw_moustache(frame)
            if Settings.DrawMoustacheDiagnostics:
                moustache.draw_moustache_diagnostics(frame)
        moustaches.update()

        cv2.imshow('frame',frame)
        if process_keys():
            break
   
    
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()