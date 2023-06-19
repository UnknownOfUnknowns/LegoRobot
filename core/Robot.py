from math import atan, sin, cos, sqrt, acos, fabs


from core.ObstacleRecoveryStrategies import OrderType

import math
from core.simulation import *

PIXEL_TO_MM_CONVERSION = 1.7
SMALL_CAM_PIX_TO_MM = 0.12


class CollisionSimulatedException(Exception):
    pass


class Robot:

    def __init__(self, blue, green, yellow, sender):
        self.blue = blue
        self.frontPoint = ((blue[0] + yellow[0]) / 2, (blue[1] + yellow[1]) / 2)
        self.green = green
        self.dir = self.direction()
        self.front = (self.frontPoint[0] + 30 * cos(self.dir / 57.2958), (self.frontPoint[1] - 30 * sin(self.dir / 57.2958)))
        self.yellow = yellow
        self.sender = sender

    def direction(self):
        if self.frontPoint[0] - self.green[0] == 0:
            if self.frontPoint[1] > self.green[1]:
                return 90
            else:
                return -90
        m = -(self.frontPoint[1] - self.green[1]) / (self.frontPoint[0] - self.green[0])
        v = atan(m) * 57.2958
        return v

    def findClosestBall(self, balls):
        closest_ball = ()
        closest_distance = 30000
        for ((x, y), radius) in balls:
            a = self.front[0] - x
            b = self.front[1] - y
            c = sqrt(a ** 2 + b ** 2)
            if c < closest_distance:
                closest_distance = c
                closest_ball = (x, y)
        return closest_ball

    def calculateAngleToBall(self, closestBall):
        angle = -angleBetweenPoints(self.green, closestBall) * 57.2958
        robotAngle = angleBetweenPoints(self.green, self.frontPoint)
        if robotAngle is not None:
            robotAngle = -robotAngle * 57
            if self.frontPoint[0] < self.green[0] and closestBall[1] > self.green[1] and self.frontPoint[1] <= self.green[1]:
                angle = abs(180 - robotAngle) + abs(angle + 180)
            elif self.frontPoint[0] < self.green[0] and closestBall[1] > self.green[1]:
                angle = 180 + angle
                robotAngle = 180 + robotAngle
                angle = angle - robotAngle
            elif self.frontPoint[0] < self.green[0] and closestBall[1] < self.green[1] and self.frontPoint[1] >= self.green[1]:
                angle = (180 - angle)
                robotAngle = (180 + robotAngle)
                angle = -(angle + robotAngle)
            elif self.frontPoint[0] < self.green[0] and closestBall[1] < self.green[1]:
                angle = -(180 - angle)
                robotAngle = -(180 - robotAngle)
                angle = angle - robotAngle
            else:
                angle = angle - robotAngle

            return angle
        robotVector = (self.frontPoint[0] - self.green[0], (self.frontPoint[1] - self.green[1]))
        ballVector = (closestBall[0] - self.green[0], (closestBall[1] - self.green[1]))
        scalarProduct = robotVector[0] * ballVector[0] + robotVector[1] * ballVector[1]
        lengthMultiple = sqrt(robotVector[0] ** 2 + robotVector[1] ** 2) * sqrt(ballVector[0] ** 2 + ballVector[1] ** 2)
        vinkel = acos(scalarProduct / lengthMultiple) * 57.2958
        left = self.isBallLeft(closestBall)
        if not left:
            return -vinkel
        return vinkel

    def calculateDistance(self, point):
        a = self.front[0] - point[0]
        b = self.front[1] - point[1]
        c = sqrt(a ** 2 + b ** 2)
        return c

    def isBallLeft(self, ball):
        a1 = self.blue[0] - ball[0]
        a2 = self.yellow[0] - ball[0]
        b1 = self.blue[1] - ball[1]
        b2 = self.yellow[1] - ball[1]
        c1 = sqrt(a1 ** 2 + b1 ** 2)
        c2 = sqrt(a2 ** 2 + b2 ** 2)
        if c1 > c2:
            return True
        else:
            return False

    def generateRobotPoints(self):
        robotPoints = []
        for x in range(int(self.green[0]), int(self.green[0] + 100)):
            for y in range(int(self.green[1] - 48), int(self.green[1] + 48)):
                robotPoints.append((x, y))
        return robotTurning(robotPoints, self.green, -self.dir / 57.2958)

    def driveToBall(self, closestBall, court):
        angle = self.calculateAngleToBall(closestBall)
        if fabs(angle) > 5:
            #if obstacleCollision(robotTurning(self.generateRobotPoints(), self.green, angle),court):
            #    raise CollisionSimulatedException
            self.sender.turn(1.7 * angle)
            return False
        distance = self.calculateDistance(closestBall)
        #if not robotMoving(self.generateRobotPoints(), self.blue, self.green, court):
            #raise CollisionSimulatedException
        if distance > 5:
            self.sender.drive(distance * PIXEL_TO_MM_CONVERSION * 0.75)
            return False
        return True

    def obstacle(self, frame, goal):
        m = -(goal[1] - self.front[1]) / (goal[0] - self.front[0])
        angle = atan(m) - math.pi
        dx = int(goal[0] - self.front[0])
        for x in range(0, dx + 1):
            y = int(cos(angle) * x)
            frame[int(self.front[0]) + x, int(self.front[1]) + y] = 100
        print(frame)

    def drive(self, distance, largeCam=True):
        self.sender.drive(distance * (PIXEL_TO_MM_CONVERSION if largeCam else SMALL_CAM_PIX_TO_MM) * 0.9)

    def pickUpBall(self):
        self.sender.closeClaw()
        self.sender.openClaw()

    def turnRobot(self, angle):
        self.sender.turn(angle)

    def executeStrategyElement(self, command, framePoints):
        if command[0].name == OrderType.TARGET.name:
            self.driveToBall(command[1], framePoints)

    def closeBay(self):
        self.sender.closeClaw()