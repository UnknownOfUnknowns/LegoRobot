import cv2
import imutils
import numpy as np
def getFramePoints(image):
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    lowerBound = (128, 98, 0)
    upperBound = (179, 255, 255)
    mask = cv2.inRange(hsv, lowerBound, upperBound)
    return mask


def getBallsHough(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.medianBlur(gray, 5)

    rows = gray.shape[0]
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                               param1=200, param2=13,
                               minRadius=10, maxRadius=10)
    if circles is None:
        return []
    return [((circle[0], circle[1]), circle[2]) for circle in circles[0]]


def getBallsHough(image, p1 = 200, p2 = 13, min= 10, max = 11):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.medianBlur(gray, 5)

    rows = gray.shape[0]
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                               param1=p1, param2=p2,
                               minRadius=min, maxRadius=max)
    if circles is None:
        return []
    return [((circle[0], circle[1]), circle[2]) for circle in circles[0]]



def getBallCoordinates(image):
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    """

    lowerBound = (0, 0, 213)
    upperBound = (179, 255, 255)
"""
    lowerBound = (99, 63, 185)
    upperBound = (114, 139, 249)

    mask = cv2.inRange(hsv, lowerBound, upperBound)

    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    balls = []
    for points in cnts:
        ball = cv2.minEnclosingCircle(points)
        if 7 > ball[1] > 3:
            balls.append(ball)

    return balls


def getRobotCoordinates(image):
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    lowerBound = (20, 0, 50)
    upperBound = (50, 205, 255)

    mask = cv2.inRange(hsv, lowerBound, upperBound)

    mask = cv2.erode(mask, None, iterations=3)
    mask = cv2.dilate(mask, None, iterations=3)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    rectangles = []
    for points in cnts:
        rect = cv2.minAreaRect(points)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        rectangles.append(box)

    return rectangles


def mapOutFrame(image):
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    lowerBound = (169, 49, 0)
    upperBound = (179, 255, 255)
    mask = cv2.inRange(hsv, lowerBound, upperBound)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    rectangles = []
    for points in cnts:
        rect = cv2.boundingRect(points)
        rectangles.append(rect)

    return rectangles


def blueGetter(image):
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    lowerBound = (0, 195, 190)
    upperBound = (179, 255, 255)
    mask = cv2.inRange(hsv, lowerBound, upperBound)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    rectangles = []
    for points in cnts:
        rect = cv2.minEnclosingCircle(points)
        ((x, y), r) = rect
        if r > 3:
            rectangles.append(rect)

    return rectangles


def yellowGetter(image):
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    lowerBound = (21, 42, 156)
    upperBound = (69, 129, 255)
    mask = cv2.inRange(hsv, lowerBound, upperBound)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    rectangles = []
    for points in cnts:
        rect = cv2.minEnclosingCircle(points)
        rectangles.append(rect)

    return rectangles


def greenGetter(image):
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    lowerBound = (82, 170, 85)
    upperBound = (97, 255, 149)
    mask = cv2.inRange(hsv, lowerBound, upperBound)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    rectangles = []
    for points in cnts:
        rect = cv2.minEnclosingCircle(points)
        rectangles.append(rect)

    return rectangles
