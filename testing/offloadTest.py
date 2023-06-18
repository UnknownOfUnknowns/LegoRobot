import math
import time

from core.Robot import Robot
from core.robotCamera import RobotCamera
from core.sender import Sender
from util.imageFilesReader import getImage
from util.mousecontroller import getImageNameFromPhone
from core.objectdetectors import greenGetterRobot
s = Sender()
while True:

    name = getImageNameFromPhone()
    time.sleep(2)
    frame = getImage(name)
    robot = Robot((1,1),(2,2),(3,3), s)
    camera = RobotCamera([frame])
    greenPoints = []
    for (x, y), r in greenGetterRobot(frame):
        greenPoints.append((x, y))
    greenPoints.sort(key=lambda x: x[0])
    dir = camera.isStraightOnForOpenClaw(greenPoints)
    if dir < 0:
        s.turn(-5)
        continue
    if dir > 0:
        s.turn(5)
        continue
    if camera.inPositionToOpen():
        s.openClaw()
        s.turn(-5)
        s.deploy()
    else:
        distance = 300 - camera.findFirstRedEdge()
        if 0 > distance > -50:
            distance = -50
        elif distance < 50:
            distance = 50
        robot.drive(distance, largeCam=False)
