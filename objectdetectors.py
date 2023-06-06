import cv2
def getFramePoints(image):
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    lowerBound = (128, 98, 0)
    upperBound = (179, 255, 255)
    mask = cv2.inRange(hsv, lowerBound, upperBound)
    return mask