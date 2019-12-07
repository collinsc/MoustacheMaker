"""Module containing shifts and offets for individual moustaches"""
import os
import cv2


def get_root():
    return f"{os.path.dirname(__file__)}{os.path.sep}"


class MoustachePicture1():
    path = f"{get_root()}moustaches{os.path.sep}moustache1.png"
    picture = cv2.imread(path, -1)
    offset = (1.0, 1.05)
    scale_fudge = 4.5
    do_blur = True
    blur_size = (2, 2)


class MoustachePicture2():
    path = f"{get_root()}moustaches{os.path.sep}moustache2.png"
    picture = cv2.imread(path, -1)
    offset = (1.0, 1.12)
    scale_fudge = 5.0
    do_blur = True
    blur_size = (2, 2)


class MoustachePicture3():
    path = f"{get_root()}moustaches{os.path.sep}moustache3.png"
    picture = cv2.imread(path, -1)
    offset = (1.0, 1.08)
    scale_fudge = 6
    do_blur = True
    blur_size = (2, 2)


class MoustachePicture4():
    path = f"{get_root()}moustaches{os.path.sep}moustache4.png"
    picture = cv2.imread(path, -1)
    offset = (1.0, 1.06)
    scale_fudge = 6.5
    do_blur = True
    blur_size = (2, 2)


class MoustachePicture5():
    path = f"{get_root()}moustaches{os.path.sep}moustache5.png"
    picture = cv2.imread(path, -1)
    offset = (1.0, 1.2)
    scale_fudge = 5.0
    do_blur = True
    blur_size = (2, 2)


class MoustachePicture6():
    path = f"{get_root()}moustaches{os.path.sep}moustache6.png"
    picture = cv2.imread(path, -1)
    offset = (1.0, 1.05)
    scale_fudge = 4.2
    do_blur = True
    blur_size = (2, 2)


class MoustachePicture7():
    path = f"{get_root()}moustaches{os.path.sep}moustache7.png"
    picture = cv2.imread(path, -1)
    offset = (1.0, 1.05)
    scale_fudge = 3.5
    do_blur = True
    blur_size = (2, 2)


class MoustachePicture8():
    path = f"{get_root()}moustaches{os.path.sep}moustache8.png"
    picture = cv2.imread(path, -1)
    offset = (1.0, 0.98)
    scale_fudge = 5.0
    do_blur = True
    blur_size = (2, 2)


MoustachePictures = [
    MoustachePicture1(),
    MoustachePicture2(),
    MoustachePicture3(),
    MoustachePicture4(),
    MoustachePicture5(),
    MoustachePicture6(),
    MoustachePicture7(),
    MoustachePicture8()]
