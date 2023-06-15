from util.imageFilesReader import getNewestPhoneImage
from core.robotCamera import RobotCamera
import cv2

test = RobotCamera([getNewestPhoneImage()])
test.findBalls()
print(test.relationToThreshold())


def nothing(x):
    pass


cv2.namedWindow("Trackbars")

HEIGHT = 1080
WIDTH = 1920
cv2.createTrackbar("P1", "Trackbars", 10, HEIGHT, nothing)
cv2.createTrackbar("SIDES", "Trackbars", 10, WIDTH, nothing)

while True:
    image = getNewestPhoneImage()
    bar = cv2.getTrackbarPos("P1", "Trackbars")
    width_bar = cv2.getTrackbarPos("SIDES", "Trackbars")
    robotCamera = RobotCamera([image])
    cv2.line(image, (0, bar), (1900, bar), (0, 255, 0), 1)
    cv2.line(image, (width_bar, 0), (width_bar, 1079), (0, 255, 0), 1)
    cv2.imshow("Trackbars", image)

    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
