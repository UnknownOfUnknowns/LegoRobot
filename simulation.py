import cv2
import numpy as np
from objectdetectors import *
"""
frame = cv2.VideoCapture(0)

_, fr = frame.read()
np.save("image", fr)
cv2.imshow("t", fr)
"""

#
image = np.load("image.npy")

edges = getFramePoints(image)
edges[0,1] = 30
print(edges)