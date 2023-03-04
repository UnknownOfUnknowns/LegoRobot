import cv2

import imutils
import numpy as np

frame = cv2.imread("balls.jpg")
width, height = frame.shape[:2]


def showImage(image):
    while True:
        cv2.imshow("image", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


def getBallCoordinates(image):
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    lowerBound = (0, 0, 220)
    upperBound = (255, 35, 255)

    mask = cv2.inRange(hsv, lowerBound, upperBound)

    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    balls = []
    for points in cnts:
        balls.append(cv2.minEnclosingCircle(points))

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


for ((x, y), radius) in getBallCoordinates(frame):

    # To see the centroid clearly
    if radius > 10:
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 5)
        cv2.imwrite("circled_frame.png", cv2.resize(frame, (int(height / 2), int(width / 2))))
        cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)

for box in getRobotCoordinates(frame):
    cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)

"""
lowerBound = (20, 0, 50)
upperBound = (50, 205, 255)
mask = cv2.inRange(hsv, lowerBound, upperBound)
showImage(mask)
"""
