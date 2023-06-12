import time

import cv2
from Robot import *
from sender import *
import imutils
import numpy as np
from objectdetectors import *
from robotCamera import RobotCamera
from imageFilesReader import getNewestPhoneImage
frame = cv2.VideoCapture(0)
frame.set(3, 1280)
frame.set(4, 720)

# frame = cv2.resize(frame, (960, 540))

# width, height = frame.shape[:2]


def showImage(image):
    while True:
        cv2.imshow("image", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


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
    lowerBound = (0, 221, 141)
    upperBound = (151, 255, 215)
    mask = cv2.inRange(hsv, lowerBound, upperBound)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    rectangles = []
    for points in cnts:
        rect = cv2.minEnclosingCircle(points)
        ((x,y),r) =rect
        if r > 8:
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


# court_box =  mapOutFrame(frame)
# for box in court_box:
#    cv2.rectangle(frame, box, (0, 0, 255), 2)

# court_box = court_box[0]
# cropped = frame[court_box[1]:court_box[1]+court_box[3], court_box[0]:court_box[0]+court_box[2]]


while True:

    _, fr = frame.read()
    frames = [getNewestPhoneImage()]

    framePoints = getFramePoints(fr)
    balls = getBallsHough(fr)
    green = greenGetter(fr)
    blue = blueGetter(fr)
    yellow = yellowGetter(fr)

    for ((x, y), radius) in green:
        cv2.circle(fr, (int(x), int(y)), int(radius), (0, 255, 0), 1)
    for ((x, y), radius) in blue:
        cv2.circle(fr, (int(x), int(y)), int(radius), (0, 255, 0), 1)
    for ((x, y), radius) in yellow:
        cv2.circle(fr, (int(x), int(y)), int(radius), (0, 255, 0), 1)
    for ((x, y), radius) in balls:
        # To see the centroid clearly

        cv2.circle(fr, (int(x), int(y)), int(radius), (0, 255, 255), 5)

    cv2.imshow("t", fr)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

    if len(green) > 0 and len(blue) > 0:
        ((x, y), _) = green[0]
        centrumGreen = (x,y)
        ((x, y), _) = blue[0]
        centrumBlue = (x,y)
        ((x, y), _) = yellow[0]
        centrumYellow = (x,y)
       # print(centrumBlue,centrumGreen)
        robot = Robot(centrumBlue,centrumGreen,centrumYellow)
        roboCam = RobotCamera(frames)
        roboCam.findBalls()
        roboCamDistance = roboCam.distanceToBall()
        if roboCamDistance == 0:
            robot.pickUpBall()
        elif roboCamDistance > 0:
            isStraightOn = roboCam.relationToThreshold()
            if isStraightOn < 0:
                robot.turnRobot(10)
            elif isStraightOn > 0:
                robot.turnRobot(-10)
            else:
                driveDistance = roboCamDistance
                if driveDistance < 10:
                    driveDistance = 10
                robot.drive(driveDistance, largeCam=False)
        elif robot.driveToBall(robot.findClosestBall(balls)):
            robot.pickUpBall()

"""
for box in getRobotCoordinates(frame):
    cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)

lowerBound = (20, 0, 50)
upperBound = (50, 205, 255)
mask = cv2.inRange(hsv, lowerBound, upperBound)
showImage(mask)
"""

"""
    for ((x, y), radius) in getBallCoordinates(fr):
        # To see the centroid clearly

        cv2.circle(fr, (int(x), int(y)), int(radius), (0, 255, 255), 5)
        # cv2.imwrite("circled_course.png", cv2.resize(frame, (int(height / 2), int(width / 2))))
        cv2.circle(fr, (int(x), int(y)), 5, (0, 0, 255), -1)
"""
