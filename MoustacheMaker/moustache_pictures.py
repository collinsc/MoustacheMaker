"""Module containing shifts and offets for individual moustaches"""

import cv2


class MoustachePicture1():
    path = "moustaches\\moustache1.png"
    picture = cv2.imread(path,-1)
    offset = (1.0,1.05)
    scale_fudge=4.5
    do_blur=True
    blur_size = (2,2)

    
class MoustachePicture2():
    path = "moustaches\\moustache2.png"
    picture = cv2.imread(path,-1)
    offset = (1.0,1.12)
    scale_fudge=5.0
    do_blur=True
    blur_size = (2,2)

class MoustachePicture3():
    path = "moustaches\\moustache3.png"
    picture = cv2.imread(path,-1)
    offset = (1.0,1.08)
    scale_fudge=6
    do_blur=True
    blur_size = (2,2)

class MoustachePicture4():
    path = "moustaches\\moustache4.png"
    picture = cv2.imread(path,-1)
    offset = (1.0,1.06)
    scale_fudge=6.5
    do_blur=True
    blur_size = (2,2)

class MoustachePicture5():
    path = "moustaches\\moustache5.png"
    picture = cv2.imread(path,-1)
    offset = (1.0,1.2)
    scale_fudge=5.0
    do_blur=True
    blur_size = (2,2)

class MoustachePicture6():
    path = "moustaches\\moustache6.png"
    picture = cv2.imread(path,-1)
    offset = (1.0,1.05)
    scale_fudge=4.2
    do_blur=True
    blur_size = (2,2)

class MoustachePicture7():
    path = "moustaches\\moustache7.png"
    picture = cv2.imread(path,-1)
    offset = (1.0,1.05)
    scale_fudge=3.5
    do_blur=True
    blur_size = (2,2)

class MoustachePicture8():
    path = "moustaches\\moustache8.png"
    picture = cv2.imread(path,-1)
    offset = (1.0,0.98)
    scale_fudge=5.0
    do_blur=True
    blur_size = (2,2)


MoustachePictures = [MoustachePicture1(), MoustachePicture2(), MoustachePicture3(), MoustachePicture4(),MoustachePicture5(),MoustachePicture6(),MoustachePicture7(),MoustachePicture8()]
