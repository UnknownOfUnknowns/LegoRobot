import math

import cv2
import numpy as np
from objectdetectors import *
from math import *

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


def robotSize():
    robot = []
    x_shift = cos(math.pi / 6)
    for x in range(int(point[0] - 10 * x_shift), int(point[0] + 5 * x_shift)):
        y_shift = (x - point[0]) * sin(pi / 6)
        for y in range(int(y_shift + point[1] - 5), int(y_shift + point[1] + 5)):
            robot.append((x, y))
    return robot


def robotMoving(coordinates, blue_point, green_point, court):
    old_one = ()
    old_two = ()
    if blue_point[0] > green_point[0]:
        max_x_min_y_coord = max(coordinates, key=lambda coord: (coord[0], coord[1]))
        max_x_max_y_coord = max(coordinates, key=lambda coord: (coord[0], -coord[1]))
        old_one = max_x_min_y_coord
        old_two = max_x_max_y_coord
        moved_coordinates = moveCoordinates(coordinates, max_x_min_y_coord, max_x_max_y_coord, 50)
    else:
        min_x_min_y_coord = min(coordinates, key=lambda coord: (coord[0], coord[1]))
        min_x_max_y_coord = min(coordinates, key=lambda coord: (coord[0], -coord[1]))
        old_one = min_x_max_y_coord
        old_two = min_x_min_y_coord
        moved_coordinates = moveCoordinates(coordinates, min_x_min_y_coord, min_x_max_y_coord, -50)

    moved_coordinates.append(old_one)
    moved_coordinates.append(old_two)
    return not obstacleCollision(moved_coordinates, court)


def moveCoordinates(coordinates, coord1, coord2, movement_distance, angle):
    moved_coordinates = []

    x_shift = cos(angle)
    coord1[0] += x_shift*movement_distance
    coord2[0] += x_shift*movement_distance

    y_shift = sin(angle)

    coord1[1] += y_shift * movement_distance
    coord2[1] += y_shift * movement_distance
    moved_coordinates.append(coord1)
    moved_coordinates.append(coord2)
    return moved_coordinates





def obstacleCollision(coordinates, court):
    x_values = [coord[0] for coord in coordinates]
    y_values = [coord[1] for coord in coordinates]
    min_x = min(x_values)
    max_x = max(x_values)
    min_y = min(y_values)
    max_y = max(y_values)

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if court[x, y] == 255:
                return True
    return False


print(edges)

flipped_image = np.flipud(edges)
robot_points = robotSize()
for point in robot_points:
    flipped_image[point[0], point[1]] = 50
flipped_image[110, 200] = 255
robotMoving(robot_points, point, (90, 200), flipped_image)
print(flipped_image, robotSize())

"""
        start_x = max(0,x-expansion_x)
        end_x = min(image.shape[1],x+expansion_x)
        start_y = max(0, y- expansion_y)
        end_y = min(image.shape[1], y + expansion_y)

        robot = points[start_y:end_y,start_x:end_x]

"""
