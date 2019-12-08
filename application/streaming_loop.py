from os import path

import cv2

from moustache_maker.video_stream import VideoStream, VideoSource
from moustache_maker.streaming_session import StreamingSession


class Streamer(object):

    def loop(self):
        path_root = f"{path.dirname(__file__)}{path.sep}static{path.sep}content"
        alt_path = f"{path_root}{path.sep}no_webcam.mp4"
        with VideoStream(force_alt=True, alt_source_path=alt_path) as video:
            cycle = 0
            stream = StreamingSession()
            if video.source != VideoSource.WEBCAM:
                stream.settings.Process = False
            while(True):
                # Capture frame-by-frame
                frame = video.get_frame()
                if stream.settings.Process:
                    if cycle == 0:
                        stream.update_model(frame)
                    stream.draw(frame, cycle)
                cycle += 1
                if cycle > stream.settings.AnimationPerUpdate:
                    cycle = 0

                frame = cv2.resize(
                    frame,
                    None,
                    fx=stream.settings.ImageScale,
                    fy=stream.settings.ImageScale)

                compressed = video.webify_frame(frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' +
                       compressed +
                       b'\r\n\r\n')
