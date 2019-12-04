import os

import cv2

from moustache_maker.video_stream import VideoStream
from moustache_maker.application import Application
from moustache_maker import settings



class Streamer(object):

    def loop(self):
        alt_path = f"{os.path.dirname(__file__)}{os.path.sep}static{os.path.sep}no_webcam.mp4"
        with VideoStream(force_alt=False, alt_source_path = alt_path) as stream:
            cycle = 0
            app = Application()
            while(True):
                # Capture frame-by-frame
                frame = stream.get_frame()
                if cycle == 0:
                    app.update_model(frame)
                app.draw(frame, cycle)
                cycle += 1
                if cycle > settings.AnimationPerUpdate:
                    cycle = 0
                frame =  cv2.resize(frame, None, fx= settings.ImageScale, fy=settings.ImageScale )
                compressed = stream.webify_frame(frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + compressed + b'\r\n\r\n')
