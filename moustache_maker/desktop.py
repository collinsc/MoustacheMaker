"""Command line application to run the face detector on a webcam"""
import cv2
from video_stream import VideoStream
import settings
from application import Application




def process_keys():
    keys = cv2.waitKeyEx(1)
    chars = keys  & 0xFF

    if chars == ord('q'):
        return True
    if chars == ord('d'):
        #turn on diagnostics
        settings.DrawFrame                  = not settings.DrawFrame
        settings.DrawMask                   = not settings.DrawMask
        settings.DrawMoustacheDiagnostics   = not settings.DrawMoustacheDiagnostics
    if chars == ord('m'):
        settings.DrawMoustache              = not settings.DrawMoustache
    if keys == 2490368:
        settings.ImageScale = settings.ImageScale + 0.1
    if keys == 2621440:
        settings.ImageScale = max(settings.ImageScale - 0.1, 0.1)
    return False

def main_loop():
    force = False

    if settings.AltPath  is not None:
        force = True
    with VideoStream(force_alt = force, alt_source_path = settings.AltPath) as stream:
        cycle = 0
        cv2.namedWindow('frame',cv2.WINDOW_AUTOSIZE)
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
            if process_keys():
                break
            frame =  cv2.resize(frame, None, fx= settings.ImageScale, fy=settings.ImageScale )
            cv2.imshow('frame',frame)
        
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main_loop()