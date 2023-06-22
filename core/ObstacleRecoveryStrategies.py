from math import sqrt, cos, sin, dist
from enum import Enum
from core.configuration.configLoader import current_config

quadrants = [(1, current_config["quadrant 1"]), (2, current_config["quadrant 2"]),
             (3, current_config["quadrant 3"]), (4, current_config["quadrant 4"])]


class OrderType(Enum):
    TARGET = 1
    DRIVE_COMMAND = 2


def calculateQuadrant(point):
    minDistanceQuadrant = 1
    minDistance = 100000
    for (n, (x, y)) in quadrants:
        if dist((x,y), point) < minDistance:
            minDistanceQuadrant = n
            minDistance = dist((x,y), point)
    return minDistanceQuadrant


class StandardStrategy:
    def __init__(self, front, angle, target):
        self.robotFront = front
        self.robotAngle = angle
        self.target = target

    def createStrategy(self):
        BACKOFF_DISTANCE = -20
        commands = []
        robotPositionAfterReverse = (self.robotFront[0] + BACKOFF_DISTANCE * cos(self.robotAngle / 57.2958),
                                     (self.robotFront[1] - BACKOFF_DISTANCE * sin(self.robotAngle / 57.2958)))
        robotQuadrant = calculateQuadrant(robotPositionAfterReverse)
        commands.append((OrderType.TARGET, quadrants[robotQuadrant - 1][1]))
        targetQuadrant = calculateQuadrant(self.target)

        if robotQuadrant == 1 and targetQuadrant == 4:
            commands.append((OrderType.TARGET, quadrants[1][1]))
        elif robotQuadrant == 2 and targetQuadrant == 3:
            commands.append((OrderType.TARGET, quadrants[0][1]))
        elif robotQuadrant == 3 and targetQuadrant == 2:
            commands.append((OrderType.TARGET, quadrants[0][1]))
        elif robotQuadrant == 4 and targetQuadrant == 1:
            commands.append((OrderType.TARGET, quadrants[1][1]))
        commands.append((OrderType.TARGET, quadrants[targetQuadrant - 1][1]))

        return commands

    def createStrategyWithDirectDrive(self):
        robotQuadrant = calculateQuadrant(self.robotFront)
        targetQuadrant = calculateQuadrant(self.target)
        if targetQuadrant != robotQuadrant:
            return self.createStrategy()
        return []


class DeliverToSmallGoalStrategy:
    def createStrategy(self, robotFront):
        robotQuadrant = calculateQuadrant(robotFront)
        commands = [(OrderType.TARGET, current_config["goal 3"]), (OrderType.TARGET, current_config["goal 2"]),
                    (OrderType.TARGET, current_config["goal 1"])]

        if robotQuadrant == 3:
            commands.insert(0, (OrderType.TARGET, quadrants[0]))

        elif robotQuadrant == 4:
            commands.insert(0, (OrderType.TARGET, quadrants[1]))
        return commands
