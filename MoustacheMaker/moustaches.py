import random
import math 

from moustache import Moustache
from face_detector import FaceIndexes
from moustache_pictures import  MoustachePictures

class Moustaches():
    """Class for managing moustache state"""
    def __init__(self, tolerance = 500, missing_cycles =30):
        self.moustaches = {}
        self.counts = {}
        self.names = {}
        self.moustache_count = 0
        self.missing_cycles = missing_cycles
        self.matched = {}

    def items(self):
        for _,moustache in self.moustaches.items():
            yield moustache


    @staticmethod
    def calculate_distance(p1,p2):  
        dist = math.sqrt((p2[0] - p1[0])**2 + (p2[0] - p1[0])**2)  
        return dist 

    def get_closest_moustache(self, mask, tolerance):
        center = Moustache.calculate_averaged_center(mask)
        min_dist = 1000000000
        out_moustache = None
        for _, moustache in self.moustaches.items():
            distance = abs(self.calculate_distance(center, moustache.current_center))
            if distance < min_dist and distance < tolerance:
                out_moustache = moustache
                self.matched[moustache] = True

        return out_moustache

    def add_moustache(self, mask, name=None):
        self.moustache_count += 1
        if name is None:
            name = str(self.moustache_count)
        moustache = Moustache(mask, name=name, picture = random.choice(MoustachePictures))
        self.moustaches[name]=moustache
        self.counts[moustache]=0
        self.matched[moustache] = True
        return moustache


    def update(self):
        to_remove = []
        for _, moustache in self.moustaches.items():
            if not self.matched[moustache]:
                self.counts[moustache]  += 1
                moustache.reset_motion()
            else:
                self.counts[moustache]  = 0
                self.matched[moustache] = False
            if self.counts[moustache] >= self.missing_cycles:
                to_remove.append(moustache)

        for moustache in to_remove:
            self.counts.pop(moustache)
            self.moustaches.pop(moustache.name)
            self.matched.pop(moustache)

