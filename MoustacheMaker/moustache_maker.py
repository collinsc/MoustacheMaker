"""Command line application to run the face detector on a webcam"""
import cv2
from face_detector import FaceDetector
from moustaches import Moustaches
from moustache import Moustache


class Settings:
    VideoPath                   = None #"data\walkers.mp4"
    PicturePath                 = None #"data\\alt_five_people.jpg"
    DrawFrame                   = False
    DrawMask                    = False
    DrawMoustacheDiagnostics    = False
    DrawMoustache               = True
    AnimationPerUpdate          = 2
    MissingCycles               = 3
    ImageScale                  = 1.0
    ToleranceScale              = 1.0

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
    if keys == 2490368:
        Settings.ImageScale = Settings.ImageScale + 0.1
    if keys == 2621440:
        Settings.ImageScale = max(Settings.ImageScale - 0.1, 0.1)
    return False

def main():
    capture = 0
    if Settings.VideoPath is not None:
        capture = Settings.VideoPath
    cap = cv2.VideoCapture(capture)
    detector = FaceDetector()
    moustaches = Moustaches(missing_cycles = Settings.MissingCycles)
    p_count = 0
    cycle = 0
    cv2.namedWindow('frame',cv2.WINDOW_AUTOSIZE)
    while(True):
        # Capture frame-by-frame
        if Settings.PicturePath is not None:
            frame = cv2.imread(Settings.PicturePath)
        else:
            ret, frame = cap.read()
        if frame is None and Settings.VideoPath is not None:
            cap = cv2.VideoCapture(capture)
            continue
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
                moustache = moustaches.get_closest_moustache(mask, max([hdim,vdim ])*Settings.ToleranceScale)

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