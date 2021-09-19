from os import path

import cv2

from moustache_maker.video_stream import VideoStream, VideoSource
from moustache_maker.streaming_session import StreamingSession


class Streamer(object):
    def __init__(self):
        path_root = f"{path.dirname(__file__)}{path.sep}static{path.sep}content"
        self.alt_path = f"{path_root}{path.sep}no_webcam.mp4"
        self.video = VideoStream(force_alt=True, alt_source_path=self.alt_path)
        self.cycle = 0
        self.stream = StreamingSession()
        if self.video.source != VideoSource.WEBCAM:
            self.stream.settings.Process = False

    def __del__(self):
        del(self.video)

    def process_image(self, frame):
        if self.stream.settings.Process:
            if self.cycle == 0:
                self.stream.update_model(frame)
            self.stream.draw(frame, self.cycle)
            self.cycle += 1
            if self.cycle > self.stream.settings.AnimationPerUpdate:
                self.cycle = 0

            frame = cv2.resize(
                frame,
                None,
                fx=self.stream.settings.ImageScale,
                fy=self.stream.settings.ImageScale)
            return self.Processvideo.webify_frame(frame)
        else:
            return frame

    def loop(self):

            while(True):
                # Capture frame-by-frame
                frame = self.video.get_frame()
                compressed = self.process_image(frame)
                yield compressed
