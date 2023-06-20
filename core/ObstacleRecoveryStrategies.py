from math import sqrt, cos, sin
from enum import Enum
from core.configuration.configLoader import current_config
quadrants = [(1, current_config["quadrant 1"]), (2, current_config["quadrant 2"]),
             (3, current_config["quadrant 3"]), (4, current_config["quadrant 4"])]


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
        commands = []
        robotPositionAfterReverse = (self.robotFront[0] + BACKOFF_DISTANCE * cos(self.robotAngle / 57.2958),
                                     (self.robotFront[1] - BACKOFF_DISTANCE * sin(self.robotAngle / 57.2958)))
        robotQuadrant = self.calculateQuadrant(robotPositionAfterReverse)
        commands.append((OrderType.TARGET, quadrants[robotQuadrant - 1][1]))
        targetQuadrant = self.calculateQuadrant(self.target)
        if robotQuadrant == 1 and targetQuadrant == 4:
            commands.append((OrderType.TARGET, quadrants[1][1]))
        elif robotQuadrant == 2 and targetQuadrant == 3:
            commands.append((OrderType.TARGET, quadrants[0][1]))
        elif robotQuadrant == 3 and targetQuadrant == 2:
            commands.append((OrderType.TARGET, quadrants[0][1]))
        elif robotQuadrant == 4 and targetQuadrant == 1:
            commands.append((OrderType.TARGET, quadrants[1][1]))
        commands.append((OrderType.TARGET, quadrants[targetQuadrant-1][1]))

        return commands


class DeliverToSmallGoalStrategy:
    def createStrategy(self):
        return [(OrderType.TARGET, current_config["goal 3"]), (OrderType.TARGET, current_config["goal 2"]), (OrderType.TARGET, current_config["goal 1"])]
