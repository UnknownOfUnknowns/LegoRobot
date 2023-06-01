from math import atan, sin, cos, sqrt, acos, fabs
import cv2
from sender import *
import math
class Robot:

    def __init__(self, blue, green):
        self.blue = blue
        self.green = green
        self.dir = self.direction()
        self.front = (blue[0] + 5 * cos(self.dir / 57.2958), (blue[1] - 5 * sin(self.dir / 57.2958)))


    def direction(self):
        if self.blue[0] - self.green[0] == 0:
            if self.blue[1] > self.green[1]:
                return 90
            else:
                return -90
        m = -(self.blue[1] - self.green[1]) / (self.blue[0] - self.green[0])
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
        robotVector = (self.blue[0] - self.green[0], (self.blue[1] - self.green[1]))
        ballVector = (closestBall[0] - self.blue[0]  , (closestBall[1] - self.blue[1]))
        scalarProduct = robotVector[0] * ballVector[0] + robotVector[1] * ballVector[1]
        lengthMultiple = sqrt(robotVector[0] ** 2 + robotVector[1] ** 2) * sqrt(ballVector[0] ** 2 + ballVector[1] ** 2)
        vinkel = acos(scalarProduct / lengthMultiple) * 57.2958
        ball_angle = atan(-ballVector[0]/ballVector[1]) * 57.2958
        if ball_angle < vinkel:
            return -vinkel
        return vinkel

    def calculateDistance(self, point):
        a = self.front[0] - point[0]
        b = self.front[1] - point[1]
        c = sqrt(a ** 2 + b ** 2)
        return c

    def driveToBall(self, closestBall):
        if fabs(self.calculateAngleToBall(closestBall)) > 2:
            turn(self.calculateAngleToBall(closestBall))
            return False

        if self.calculateDistance(closestBall) > 5:
            # drive forward
            return False
        return True

    def obstacle(self, frame, goal):
        m = -(goal[1] - self.front[1]) / (goal[0] - self.front[0])
        angle = atan(m) - math.pi
        dx = int(goal[0] - self.front[0])
        for x in range(0, dx + 1):
            y =int( cos(angle) * x)
            frame[int(self.front[0])+x, int(self.front[1])+y] = 100
        print(frame)
