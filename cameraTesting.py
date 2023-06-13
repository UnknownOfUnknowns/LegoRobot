import cv2
import matplotlib.pyplot as plt
import time
cap = cv2.VideoCapture(0)

while True:
    _, fr = cap.read()
    plt.imshow(fr)
    plt.show()
    cv2.imshow("Trackbars", fr)



    key = cv2.waitKey(1)
    if key == 27:
        break
