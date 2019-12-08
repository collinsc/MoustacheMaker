from os import path

import cv2

from moustache_maker.video_stream import VideoStream, VideoSource
from moustache_maker.application import Application
from moustache_maker import settings


class Streamer(object):

    def loop(self):
        path_root = f"{path.dirname(__file__)}{path.sep}static{path.sep}content"
        alt_path = f"{path_root}{path.sep}no_webcam.mp4"
        with VideoStream(force_alt=True, alt_source_path=alt_path) as stream:
            cycle = 0
            app = Application()
            if stream.source != VideoSource.WEBCAM:
                settings.Process = False
            while(True):
                # Capture frame-by-frame
                frame = stream.get_frame()
                if settings.Process:
                    if cycle == 0:
                        app.update_model(frame)
                    app.draw(frame, cycle)
                cycle += 1
                if cycle > settings.AnimationPerUpdate:
                    cycle = 0

                frame = cv2.resize(
                    frame,
                    None,
                    fx=settings.ImageScale,
                    fy=settings.ImageScale)

                compressed = stream.webify_frame(frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' +
                       compressed +
                       b'\r\n\r\n')
