from core.objectdetectors import *
import cv2

frame = cv2.VideoCapture(0)
frame.set(3, 1280)
frame.set(4, 720)

while True:

    _, fr = frame.read()

    framePoints = getFramePoints(fr)
    balls = getBallsHough(fr)
    green = greenGetter(fr)
    blue = blueGetter(fr)
    yellow = yellowGetter(fr)

    for ((x, y), radius) in green:
        cv2.circle(fr, (int(x), int(y)), int(radius), (0, 255, 0), 1)
    for ((x, y), radius) in blue:
        cv2.circle(fr, (int(x), int(y)), int(radius), (0, 255, 0), 1)
    for ((x, y), radius) in yellow:
        cv2.circle(fr, (int(x), int(y)), int(radius), (0, 255, 0), 1)
    for ((x, y), radius) in balls:
        # To see the centroid clearly

        cv2.circle(fr, (int(x), int(y)), int(radius), (0, 255, 255), 5)

    cv2.imshow("t", fr)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
