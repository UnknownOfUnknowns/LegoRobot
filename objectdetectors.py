import cv2


def getFramePoints(image):
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    lowerBound = (128, 98, 0)
    upperBound = (179, 255, 255)
    mask = cv2.inRange(hsv, lowerBound, upperBound)
    return mask


def getBallsHough(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.medianBlur(gray, 5)

    rows = gray.shape[0]
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                               param1=200, param2=13,
                               minRadius=10, maxRadius=10)
    if circles is None:
        return []
    return [((circle[0], circle[1]), circle[2]) for circle in circles[0]]


def getBallsHough(image, p1 = 200, p2 = 13, min= 10, max = 11):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.medianBlur(gray, 5)

    rows = gray.shape[0]
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                               param1=p1, param2=p2,
                               minRadius=min, maxRadius=max)
    if circles is None:
        return []
    return [((circle[0], circle[1]), circle[2]) for circle in circles[0]]
