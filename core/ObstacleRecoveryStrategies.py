from math import sqrt, cos, sin
from enum import Enum
from core.configuration.configLoader import current_config
quadrants = [(1, (150, 100)), (2, (500, 100)), (3, (150, 370)), (4, (500, 370))]


class OrderType(Enum):
    TARGET = 1
    DRIVE_COMMAND = 2


class StandardStrategy:
    def __init__(self, front, angle, target):
        self.robotFront = front
        self.robotAngle = angle
        self.target = target

    def calculateQuadrant(self, point):
        minDistanceQuadrant = 1
        minDistance = 100000
        for (n, (x, y)) in quadrants:
            if sqrt((point[0] - x) ** 2 + (point[1] - y) ** 2) < minDistance:
                minDistanceQuadrant = n
        return minDistanceQuadrant

    def createStrategy(self):
        BACKOFF_DISTANCE = -20
        commands = [(OrderType.DRIVE_COMMAND, BACKOFF_DISTANCE)]
        robotPositionAfterReverse = (self.robotFront[0] + BACKOFF_DISTANCE * cos(self.robotAngle / 57.2958),
                                     (self.robotFront[1] - BACKOFF_DISTANCE * sin(self.robotAngle / 57.2958)))
        robotQuadrant = self.calculateQuadrant(robotPositionAfterReverse)
        commands.append((OrderType.TARGET, quadrants[robotQuadrant - 1][1]))
        targetQuadrant = self.calculateQuadrant(self.target)
        if robotQuadrant == 1 and targetQuadrant == 4:
            commands.append((OrderType.TARGET, 2))
        elif robotQuadrant == 2 and targetQuadrant == 3:
            commands.append((OrderType.TARGET, 1))
        elif robotQuadrant == 3 and targetQuadrant == 2:
            commands.append((OrderType.TARGET, 1))
        elif robotQuadrant == 4 and targetQuadrant == 1:
            commands.append((OrderType.TARGET, 2))
        commands.append((OrderType.TARGET, targetQuadrant))

        return commands


class DeliverToSmallGoalStrategy:
    def createStrategy(self):
        return [(OrderType.TARGET, current_config["goal 3"]), (OrderType.TARGET, current_config["goal 2"]), (OrderType.TARGET, current_config["goal 1"])]
