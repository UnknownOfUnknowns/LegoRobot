import math

import cv2
import numpy as np
from objectdetectors import *
from math import *
import matplotlib.pyplot as plt

"""
frame = cv2.VideoCapture(0)

_, fr = frame.read()
np.save("image", fr)
cv2.imshow("t", fr)
"""

#
image = np.load("image.npy")

edges = getFramePoints(image)

# edges[477,3] = 200

point = (100, 200)


def robotSize(angle):
    robot = []
    x_shift = cos(angle)
    for x in range(int(point[0] - 10 * x_shift), int(point[0] + 5 * x_shift)):
        y_shift = (x - point[0]) * sin(angle)
        for y in range(int(y_shift + point[1] - 5), int(y_shift + point[1] + 5)):
            robot.append((x, y))
    return robot


def robotMoving(coordinates, blue_point, green_point, court):
    if blue_point[0] > green_point[0]:
        max_x_min_y_coord = max(coordinates, key=lambda coord: (coord[0], coord[1]))
        max_x_max_y_coord = max(coordinates, key=lambda coord: (coord[0], -coord[1]))
        moved_coordinates = moveCoordinates(max_x_min_y_coord, max_x_max_y_coord, 50, pi / 6)
    else:
        min_x_min_y_coord = min(coordinates, key=lambda coord: (coord[0], coord[1]))
        min_x_max_y_coord = min(coordinates, key=lambda coord: (coord[0], -coord[1]))
        moved_coordinates = moveCoordinates(min_x_min_y_coord, min_x_max_y_coord, -50, pi / 6)

    return not obstacleCollision(moved_coordinates, court)


def angleBetweenPoints(p1, p2):
    xGrowth = p2[0] - p1[0]
    if xGrowth == 0:
        return pi / 2
    return atan((p2[1] - p1[1]) / xGrowth)


def robotTurning(coordinates, green_point, angle, court):
    green_x, green_y = green_point
    newCoordinates = []
    for coordinate in coordinates:
        x, y = coordinate
        newAngle = angleBetweenPoints(green_point, coordinate) + angle
        dist = sqrt((x - green_x) ** 2 + (y - green_y) ** 2)
        newCoordinates.append((int(green_x + cos(newAngle) * dist), int(green_y + sin(newAngle) * dist)))
    return newCoordinates


def moveCoordinates(coord1, coord2, movement_distance, angle):
    moved_coordinates = []

    x_shift = cos(angle)

    y_shift = sin(angle)

    for i in range(1, movement_distance + 1):
        x1 = int(coord1[0] + x_shift * i)
        x2 = int(coord2[0] + x_shift * i)
        for x in range(min(x1, x2), max(x1, x2) + 1):
            y1 = int(coord1[1] + y_shift * i)
            y2 = int(coord2[1] + y_shift * i)
            for y in range(min(y1, y2), max(y1, y2) + 1):
                moved_coordinates.append((x, y))

    return moved_coordinates


def obstacleCollision(coordinates, court):
    for (x, y) in coordinates:
        if court[x, y] == 255:
            return True
    return False


"""
print(edges)

flipped_image = np.flipud(edges)
robot_points = [(x,y) for y in range(100,120) for x in range(100, 150)]#robotSize(pi / 6)
for point in robotTurning(robot_points, (120,110), pi/7, []):
    flipped_image[point[0], point[1]] = 50
flipped_image[110, 200] = 255
robotMoving(robot_points, point, (90, 200), flipped_image)
print(flipped_image, robotSize(pi / 6))

        start_x = max(0,x-expansion_x)
        end_x = min(image.shape[1],x+expansion_x)
        start_y = max(0, y- expansion_y)
        end_y = min(image.shape[1], y + expansion_y)

        robot = points[start_y:end_y,start_x:end_x]

"""
