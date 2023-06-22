import math
import time

from core.Robot import Robot
from core.robotCamera import RobotCamera
from core.sender import Sender
from util.imageFilesReader import getImage
from util.mousecontroller import *
from core.objectdetectors import greenGetterRobot
from core.phoneCameraReader import getPhoneImage
s = Sender()
turnCount = 0
turnLeftTest = True
while True:

#    name = getNewestImageName()

#    frame = getImage(name)

    frame = getPhoneImage()
    robot = Robot((1,1),(2,2),(3,3), s)
    camera = RobotCamera([frame])
    greenPoints = []
    for (x, y), r in greenGetterRobot(frame):
        greenPoints.append((x, y))
    greenPoints.sort(key=lambda x: x[0])

    if len(greenPoints) == 0:
        redFound = camera.findFirstRedEdge()
        if redFound == -1:
            robot.drive(300, largeCam=False)

        else:
            if turnCount == 2:
                turnCount = -2
                turnLeftTest = not turnLeftTest
            if turnLeftTest == True:
                s.turn(10)
            else:
                s.turn(-10)
            turnCount += 1
        continue
    elif len(greenPoints) == 1:
        if greenPoints[0][0] < camera.middle:
            s.turn(5)
        else:
            s.turn(-5)
        continue
    dir = camera.isStraightOnForOpenClaw(greenPoints)
    if dir < 0:
        s.turn(-5)
        continue
    if dir > 0:
        s.turn(5)
        continue
    if camera.inPositionToOpen():
        s.openClaw()
        s.turn(10)
        robot.drive(100, largeCam=False)
        s.deploy()
    else:
        distance = 300 - camera.findFirstRedEdge()
        if 0 > distance > -50:
            distance = -50
        elif distance < 50:
            distance = 50
        robot.drive(distance, largeCam=False)
