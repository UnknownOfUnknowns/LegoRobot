import cv2
import numpy as np
image = cv2.imread("../resources/full_court.jpg", cv2.IMREAD_COLOR)

"""

circles = getBallsHough(image)
circles = np.round(circles)
for i in circles[0, :]:
    center = (i[0], i[1])
    # circle center
    cv2.circle(image, center, 1, (0, 100, 100), 3)
    # circle outline
    radius = int(i[2])
    cv2.circle(image, center, radius, (255, 0, 255), 3)

cv2.imshow("detected circles", image)
cv2.waitKey(0)

"""
