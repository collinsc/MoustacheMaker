"""Command line application to run the face detector on a webcam"""
import math
import random

import numpy as np
import cv2
import dlib
from pykalman import UnscentedKalmanFilter
from imutils import face_utils, rotate_bound



class Settings:
    PicturePath                 = None #"data\\two_people.jpg"
    DrawFrame                   = False
    DrawMask                    = False
    DrawMoustacheDiagnostics    = False
    DrawMoustache               = True
    AnimationPerUpdate          = 3
    ImageScale                  = 1.0



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
    do_blur=True
    blur_size = (2,2)

    
class MoustachePicture2():
    path = "moustaches\\moustache2.png"
    picture = cv2.imread(path,-1)
    offset = (1.0,1.12)
    scale_fudge=5.0
    do_blur=True
    blur_size = (2,2)

class MoustachePicture3():
    path = "moustaches\\moustache3.png"
    picture = cv2.imread(path,-1)
    offset = (1.0,1.08)
    scale_fudge=6
    do_blur=True
    blur_size = (2,2)

class MoustachePicture4():
    path = "moustaches\\moustache4.png"
    picture = cv2.imread(path,-1)
    offset = (1.0,1.06)
    scale_fudge=6.5
    do_blur=True
    blur_size = (2,2)

class MoustachePicture5():
    path = "moustaches\\moustache5.png"
    picture = cv2.imread(path,-1)
    offset = (1.0,1.2)
    scale_fudge=5.0
    do_blur=True
    blur_size = (2,2)

class MoustachePicture6():
    path = "moustaches\\moustache6.png"
    picture = cv2.imread(path,-1)
    offset = (1.0,1.05)
    scale_fudge=4.2
    do_blur=True
    blur_size = (2,2)

class MoustachePicture7():
    path = "moustaches\\moustache7.png"
    picture = cv2.imread(path,-1)
    offset = (1.0,1.05)
    scale_fudge=3.5
    do_blur=True
    blur_size = (2,2)

class MoustachePicture8():
    path = "moustaches\\moustache8.png"
    picture = cv2.imread(path,-1)
    offset = (1.0,0.98)
    scale_fudge=5.0
    do_blur=True
    blur_size = (2,2)

MoustachePictures = [MoustachePicture1(), MoustachePicture2(), MoustachePicture3(), MoustachePicture4(),MoustachePicture5(),MoustachePicture6(),MoustachePicture7(),MoustachePicture8()]



class Moustaches():
    def __init__(self, tolerance = 500, missing_cycles =30):
        self.moustaches = {}
        self.counts = {}
        self.names = {}
        self.moustache_count = 0
        self.missing_cycles = missing_cycles
        self.matched = {}

    def items(self):
        for _,moustache in self.moustaches.items():
            yield moustache


    @staticmethod
    def calculate_distance(p1,p2):  
        dist = math.sqrt((p2[0] - p1[0])**2 + (p2[0] - p1[0])**2)  
        return dist 

    def get_closest_moustache(self, mask, tolerance):
        center = Moustache.calculate_averaged_center(mask)
        min_dist = 1000000000
        out_moustache = None
        for _, moustache in self.moustaches.items():
            distance = abs(self.calculate_distance(center, moustache.current_center))
            if distance < min_dist and distance < tolerance:
                out_moustache = moustache
                self.matched[moustache] = True

        return out_moustache

    def add_moustache(self, mask, name=None):
        self.moustache_count += 1
        if name is None:
            name = str(self.moustache_count)
        moustache = Moustache(mask, name=name, picture = random.choice(MoustachePictures))
        self.moustaches[name]=moustache
        self.counts[moustache]=0
        self.matched[moustache] = True
        return moustache


    def update(self):
        to_remove = []
        for _, moustache in self.moustaches.items():
            if not self.matched[moustache]:
                self.counts[moustache]  += 1
                moustache.reset_motion()
            else:
                self.counts[moustache]  = 0
                self.matched[moustache] = False
            if self.counts[moustache] >= self.missing_cycles:
                to_remove.append(moustache)

        for moustache in to_remove:
            self.counts.pop(moustache)
            self.moustaches.pop(moustache.name)
            self.matched.pop(moustache)

class Moustache():
    """Smoothed moustache using a kalman filter"""
    def __init__(self, mask, name="", picture = MoustachePicture1()):
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
        return int(round(xy[1]))

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
    keys = cv2.waitKeyEx(1)
    chars = keys  & 0xFF

    if chars == ord('q'):
        return True
    if chars == ord('d'):
        #turn on diagnostics
        Settings.DrawFrame                  = not Settings.DrawFrame
        Settings.DrawMask                   = not Settings.DrawMask
        Settings.DrawMoustacheDiagnostics   = not Settings.DrawMoustacheDiagnostics
    if chars == ord('m'):
        Settings.DrawMoustache              = not Settings.DrawMoustache
    if keys == 2621440:
        Settings.ImageScale = Settings.ImageScale + 0.1
    if keys == 2490368:
        Settings.ImageScale = max(Settings.ImageScale - 0.1, 0.1)
    print(keys, chars)

    return False

def main():
    cap = cv2.VideoCapture(0)
    detector = FaceDetector()
    moustaches = Moustaches(missing_cycles = 2)
    p_count = 0
    cycle = 0
    cv2.namedWindow('frame',cv2.WINDOW_AUTOSIZE)
    while(True):
        # Capture frame-by-frame
        if Settings.PicturePath is not None:
            frame = cv2.imread(Settings.PicturePath)
        else:
            ret, frame = cap.read()
        if cycle == 0:

            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rects = detector.get_faces(gray)
            names = []
            masks=[]
            for rect in rects:
                mask = detector.get_face_dots(gray, rect)
                masks.append(mask)
                hdim = rect.right() - rect.left()
                vdim = rect.bottom() - rect.top()
                moustache = moustaches.get_closest_moustache(mask, max([hdim,vdim ])*0.9)

                if moustache is None:
                    moustache = moustaches.add_moustache(mask)
                names.append(moustache.name)
                moustache.add_frame(mask)
                moustache.set_goal(Settings.AnimationPerUpdate)
            moustaches.update()
        



        for mask, rect, name in zip(masks, rects, names):
            if Settings.DrawFrame:
                detector.draw_bounding_rect(rect, frame,name)
            if Settings.DrawMask:
                detector.draw_mask(mask, frame, Moustache.get_landmark_idx())

        for moustache in moustaches.items():
            if Settings.DrawMoustache:
                moustache.draw_moustache(frame, cycle)
            if Settings.DrawMoustacheDiagnostics:
                moustache.draw_moustache_diagnostics(frame)
        

        
        cycle += 1
        if cycle > Settings.AnimationPerUpdate:
            cycle = 0
        if process_keys():
            break
        frame =  cv2.resize(frame, None, fx= Settings.ImageScale, fy=Settings.ImageScale )
        cv2.imshow('frame',frame)


   
    
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()