import cv2
import matplotlib.pyplot as plt
import time
cap = cv2.VideoCapture(0)


_, fr = cap.read()

cv2.imwrite("collisionSide.png",fr)


