import cv2
from enum import Enum

class VideoSource(Enum):
    WEBCAM  = 0
    VIDEO   = 1
    PICTURE = 2



class VideoStream(object):
    """loosely based on https://github.com/log0/video_streaming_with_flask_example"""
    def __init__(self, use_alt=False, alt_source_path=None):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        self.webcam = True

        self.alt_source_path = alt_source_path
        self.source = VideoSource.WEBCAM
        if use_alt:
            if alt_source_path.lower().endswith(".mp4"):
                self.video = cv2.VideoCapture(alt_video_path)
                self.source = VideoSource.VIDEO
            if alt_source_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.source = VideoSource.PICTURE



    def __enter__(self):
        return self
    def __exit__(self, exception_type, exception_value, traceback):
        del(self)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        if self.source == VideoSource.PICTURE:
            image = cv2.imread(Settings.PicturePath)
        else:
            success, image = self.video.read()
            if image is None and not self.webcam:
                self.video = cv2.VideoCapture(alt_video_path)
                success, image = self.video.read()
        return image
