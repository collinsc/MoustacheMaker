from enum import Enum
from queue import Queue
from threading import Thread

import cv2

from . import settings


class VideoSource(Enum):
    WEBCAM = 0
    VIDEO = 1
    PICTURE = 2


class VideoStream(object):
    """loosely based on
    https://github.com/log0/video_streaming_with_flask_example"""

    def __init__(self,
                 force_alt=False,
                 alt_source_path=None,
                 queue_size=128,
                 frame_rate=25):
        # Using OpenCV to capture from device 0.  If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)

        self.alt_source_path = alt_source_path
        self.source = VideoSource.WEBCAM
        if force_alt:
            if alt_source_path.lower().endswith(".mp4"):
                self.video = cv2.VideoCapture(alt_source_path)
                self.source = VideoSource.VIDEO
            if alt_source_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.source = VideoSource.PICTURE
        self.frame_rate = frame_rate
        if self.video is not None:
            self.video.set(cv2.CAP_PROP_FPS, self.frame_rate)
        self.q = Queue(queue_size)
        self.stopped = False

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        del(self)

    def __del__(self):
        self.video.release()

    def start(self):
        # start a thread to read frames from the file video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()

    def update(self):
        while True:
            if self.stopped:
                return
            if not self.q.full():
                frame = self.read_image()
                # add the frame to the queue
                self.q.put(frame)

    def read_image(self):
        if self.source == VideoSource.PICTURE:
            image = cv2.imread(settings.PicturePath)
        else:
            success, image = self.video.read()
            if image is None and not self.source == VideoSource.WEBCAM:
                self.video = cv2.VideoCapture(self.alt_source_path)
                if self.video is not None:
                    self.video.set(cv2.CAP_PROP_FPS, self.frame_rate)
                success, image = self.video.read()
        return image

    def get_frame(self):
        return self.q.get()

    def webify_frame(self, frame):
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
