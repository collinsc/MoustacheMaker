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
    offset = (0,10)
    scale_fudge=4


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
            distance = abs(self.calculate_distance(center, moustache.get_center()))
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
    def __init__(self, size =5, name="", picture = MoustachePicture1()):
        self.centers = []
        self.heights = []
        self.masks = []
        self.size = size
        self.name = name
        self.covariance = 1e-2
        self.picture = picture



    def _calculate_kalman(self, arr):
        if len(arr) < 3:
            return arr[-1]
        try:
            dim = len(arr[0])
        except:
            dim = 1
        if dim ==1:
            obs_covariance = self.covariance
        if dim == 2:
            obs_covariance = [[self.covariance,0],[0,self.covariance]]
        kf = UnscentedKalmanFilter(initial_state_mean=arr[0], n_dim_state=dim,n_dim_obs=dim, observation_covariance=obs_covariance)
        means, covariances = kf.smooth(arr)
        return  [int(round(x)) for x in means[-1]]
    @staticmethod
    def calculate_averaged_center(mask):
        xy = sum([mask[FaceIndexes.NoseTip], mask[FaceIndexes.MouthTopCenter], mask[FaceIndexes.NoseUnder]])/3.0
        return [int(round(x)) for x in xy]

    @staticmethod
    def calculate_averaged_height(mask):
        xy = mask[FaceIndexes.MouthTopCenter] - mask[FaceIndexes.NoseUnder]
        return int(round(xy[1]))

    @staticmethod
    def _smooth_avg(x, window ):
        if type(x) is not np.array:
            x = np.array(x)
        if x.ndim != 1:
            raise ValueError("smooth only accepts 1 dimension arrays.")
    
        window_len = len(x)
        if window_len < 3:
            return x[-1].item()
        if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
            raise ValueError( "Window is not one of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

        if window == 'flat': #moving average
            w=np.ones((window_len),'d')
        else:
            w=eval(f"np.{window}({window_len})")
    
        y=np.convolve(w/w.sum(),x,mode='valid')
        return int(round(y.item()))
    def __len__(s):
        return len(self.centers)


    def add_frame(self, mask):
        self.centers.append( self.calculate_averaged_center(mask))
        self.heights.append(self.calculate_averaged_height(mask))

        if len(self.centers)  > self.size:
            self.centers = self.centers[1:self.size]

    def get_center(self):
        return self._calculate_kalman(self.centers)

    def get_height(self):
        height =  self._calculate_kalman(self.heights)
        if type(height) != int:
            height = height[0]
        return height

    def get_name(self):
        return self.name
    
    def draw_moustache(self, out):
        picture = self.picture.picture
        height = self.get_height()
        height_ratio = height/picture.shape[1] * self.picture.scale_fudge
        scaled = cv2.resize(picture, None, fx=height_ratio, fy=height_ratio)
        center = self.get_center()
        x1 = center[0]-scaled.shape[1]//2 + self.picture.offset[0]
        y1 = center[1]-scaled.shape[0]//2 + self.picture.offset[1]
        x2 = x1 + scaled.shape[1]
        y2 = y1 + scaled.shape[0]
        alpha_s = scaled[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            out[y1:y2, x1:x2, c] = (alpha_s * scaled[:, :, c] +
                              alpha_l * out[y1:y2, x1:x2, c])

    def draw_moustache_diagnostics(self, out):
        height = self.get_height()

        height = int(round(height/2.0))
        cross_length = int(round(height/4.0))
        cross_thickness = 2
        color = (0, 55, 200)
        center = self.get_center()
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
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()