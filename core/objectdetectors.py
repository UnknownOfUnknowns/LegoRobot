import cv2
import imutils
import numpy as np
from core.configuration.configLoader import current_config
def getFramePoints(image):
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    lowerBound = current_config["red lower"]
    upperBound = current_config["red upper"]
    mask = cv2.inRange(hsv, lowerBound, upperBound)
    return mask

def getFramePointsPhone(image):
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    lowerBound = (5, 34, 156)
    upperBound = (6, 214, 255)
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
    lowerBound = current_config["blue lower"]
    upperBound = current_config["blue upper"]
    mask = cv2.inRange(hsv, lowerBound, upperBound)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    rectangle = ((0,0), 0)
    for points in cnts:
        rect = cv2.minEnclosingCircle(points)
        ((x, y), r) = rect
        if r > rectangle[1]:
            rectangle = rect

    return [rectangle]


def yellowGetter(image):
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    #lowerBound = (21, 42, 156)
    #upperBound = (69, 129, 255)
    lowerBound = current_config["yellow lower"]
    upperBound = current_config["yellow upper"]
    mask = cv2.inRange(hsv, lowerBound, upperBound)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    rectangles = []
    for points in cnts:
        rect = cv2.minEnclosingCircle(points)
        rectangles.append(rect)

    rectangles.sort(key= lambda x : x[1])
    if len(rectangles) > 0:
        return [rectangles[-1]]
    return []

def greenGetter(image):
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    #lowerBound = (82, 170, 85)
    #upperBound = (97, 255, 149)

    lowerBound = current_config["green lower"]
    upperBound = current_config["green upper"]
    mask = cv2.inRange(hsv, lowerBound, upperBound)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    rectangle = ((0,0), 0)
    for points in cnts:
        rect = cv2.minEnclosingCircle(points)
        ((x, y), r) = rect
        if r > rectangle[1]:
            rectangle = rect

    return [rectangle]

def greenGetterRobot(image):
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    #lowerBound = (82, 170, 85)
    #upperBound = (97, 255, 149)
    lowerBound = (37, 124, 166)
    upperBound = (73, 157, 246)
    mask = cv2.inRange(hsv, lowerBound, upperBound)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    rectangles = []
    for points in cnts:
        rect = cv2.minEnclosingCircle(points)
        rectangles.append(rect)
    return rectangles


def getOrangeBall(image):
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    lowerBound = (11, 68, 202)
    upperBound = (21, 255, 255)
    mask = cv2.inRange(hsv, lowerBound, upperBound)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    rectangle = ((0,0), 0)
    for points in cnts:
        rect = cv2.minEnclosingCircle(points)
        ((x, y), r) = rect
        if r > rectangle[1] and r > 7 and r < 12:
            rectangle = rect
    if rectangle == ((0,0), 0):
        return []
    return [rectangle]
