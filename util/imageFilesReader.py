import glob
import os

import cv2


def getNewestPhoneImage():

    list_of_files = glob.glob('/Users/ChristianKjeldgaardJensen/Desktop/imgs/*.png')
    latest_file = max(list_of_files, key=os.path.getctime)

    return cv2.imread(latest_file)


def getImage(name):
    return cv2.imread(name)


def getNewestImageName():
    os.chdir("/Users/ChristianKjeldgaardJensen/Desktop/imgs")
    list_of_files = glob.glob('/Users/ChristianKjeldgaardJensen/Desktop/imgs/*.png')
    latest_file = max(list_of_files, key=os.path.getctime)
    files = []
    for file in glob.glob("*.png"):
        files.append(file)

    sorted(files)
    return latest_file
