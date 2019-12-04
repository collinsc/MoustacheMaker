
import cv2
from imutils import face_utils

from face_detector import FaceDetector
from moustaches import Moustaches
from moustache import Moustache
import settings

class Application(object):
    def __init__(self):
        self.face_detector = FaceDetector()
        self.moustaches = Moustaches(missing_cycles = settings.MissingCycles)

    def update_model(self, frame):
        # Our operations on the frame come here
        self.faces = self.face_detector.get_faces(frame)
        for face in self.faces:
            hdim = face.rect.right() -  face.rect.left()
            vdim = face.rect.bottom() - face.rect.top()
            moustache = self.moustaches.get_closest_moustache(face.mask, max([hdim,vdim]) * settings.ToleranceScale)
        
            if moustache is None:
                moustache = self.moustaches.add_moustache(face.mask)
            face.moustache  = moustache
            moustache.add_frame(face.mask)
            moustache.set_goal(settings.AnimationPerUpdate)
        self.moustaches.update()
        
    def draw(self, frame, idx):
        for face in self.faces:
            if settings.DrawFrame:
                self.draw_bounding_rect(face.rect, frame, face.moustache.name)
            if settings.DrawMask:
                self.draw_mask(face.mask, frame, Moustache.get_landmark_idx())
            if settings.DrawMoustache:
                face.moustache.draw_moustache(frame, idx)
            if settings.DrawMoustacheDiagnostics:
                face.moustache.draw_moustache_diagnostics(frame)

    def draw_mask(self, shape, out, important_idx=[]):
        for i, (x, y) in enumerate(shape):
            if i in important_idx:
                color = (255, 0, 0)
            else:
                color = (0, 0, 255)
            cv2.circle(out, (x, y), 1, color, -1)

    def draw_bounding_rect(self, rect, out, name=""):
        x, y, w, h = face_utils.rect_to_bb(rect)
        cv2.rectangle(out, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(out, f"Face {name}", (x - 10, y - 10),
	    	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

