"""Command line application to run the face detector on a webcam"""
import os

import cv2

import moustache_maker
from moustache_maker.video_stream import VideoStream
from moustache_maker.streaming_session import StreamingSession
from moustache_maker.settings import Settings

SETTINGS_PATH=f"{os.path.dirname(moustache_maker.__file__)}{os.path.sep}data{os.path.sep}defaults.json"


def process_keys(stream):
    keys = cv2.waitKeyEx(1)
    chars = keys & 0xFF

    if chars == ord('q'):
        return True
    if chars == ord('d'):
        # turn on diagnostics
        stream.settings.DrawFrame = not stream.settings.DrawFrame
        stream.settings.DrawMask = not stream.settings.DrawMask
        stream.settings.DrawMoustacheDiagnostics = not stream.settings.DrawMoustacheDiagnostics
    if chars == ord('m'):
        stream.settings.DrawMoustache = not stream.settings.DrawMoustache
    if keys == 2490368:
        stream.settings.ImageScale = stream.settings.ImageScale + 0.1
    if keys == 2621440:
        stream.settings.ImageScale = max(stream.settings.ImageScale - 0.1, 0.1)
    return False


def main_loop():
    force = False
    stream = StreamingSession()
    stream.settings = Settings.from_json(SETTINGS_PATH)
    if stream.settings.AltPath is not None:
        force = True
    with VideoStream(force_alt=force,
                     alt_source_path=stream.settings.AltPath) as video:
        cycle = 0
        cv2.namedWindow('frame', cv2.WINDOW_AUTOSIZE)

        while(True):
            # Capture frame-by-frame
            frame = video.get_frame()
            if cycle == 0:
                stream.update_model(frame)
            stream.draw(frame, cycle)
            cycle += 1
            if cycle > stream.settings.AnimationPerUpdate:
                cycle = 0
            if process_keys(stream):
                break
            frame = cv2.resize(frame,
                               None,
                               fx=stream.settings.ImageScale,
                               fy=stream.settings.ImageScale)
            cv2.imshow('frame', frame)

    cv2.destroyAllWindows()
    stream.settings.to_json(SETTINGS_PATH)


main_loop()
