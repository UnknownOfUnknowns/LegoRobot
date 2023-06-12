import glob
import os

import cv2


def getNewestPhoneImage():
    os.chdir("C:\\Users\\hans\\Pictures\\CameraHub")

    files = []
    for file in glob.glob("*.png"):
        files.append(file)

    sorted(files)
    return cv2.imread("C:\\Users\\hans\\Pictures\\CameraHub\\" + files[-1])

