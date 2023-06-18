import cv2
import imutils
from core.simulation import angleBetweenPoints
#vid = cv2.VideoCapture(2)
"""
vid.set(3, 1280)
vid.set(4, 720)
"""
def nothing(x):
    pass

cv2.namedWindow("Trackbars")

# Now create 6 trackbars that will control the lower and upper range of
# H,S and V channels. The Arguments are like this: Name of trackbar,
# window name, range,callback function. For Hue the range is 0-179 and
# for S,V its 0-255.
cv2.createTrackbar("x1", "Trackbars", 0, 300, nothing)
cv2.createTrackbar("x2", "Trackbars", 0, 700, nothing)
cv2.createTrackbar("y1", "Trackbars", 0, 500, nothing)
cv2.createTrackbar("y2", "Trackbars", 179, 500, nothing)

cv2.createTrackbar("x3", "Trackbars", 0, 500, nothing)
cv2.createTrackbar("y3", "Trackbars", 179, 500, nothing)

while (True):
    def blueGetter(image):
        blurred = cv2.GaussianBlur(image, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        lowerBound = (0, 195, 190)
        upperBound = (179, 255, 255)
        mask = cv2.inRange(hsv, lowerBound, upperBound)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        rectangles = []
        for points in cnts:
            rect = cv2.minEnclosingCircle(points)
            ((x, y), r) = rect
            if r > 3:
                rectangles.append(rect)

        return rectangles
    # Capture the video frame
    # by frame
    frame = cv2.imread("../../resources/collisionSide.png")

    red = [(cv2.getTrackbarPos("x1", "Trackbars"), cv2.getTrackbarPos("y1", "Trackbars"))]
    green = [(cv2.getTrackbarPos("x2", "Trackbars"), cv2.getTrackbarPos("y2", "Trackbars"))]
    blue = [(cv2.getTrackbarPos("x3", "Trackbars"), cv2.getTrackbarPos("y3", "Trackbars"))]
    for ((x, y)) in red:
        cv2.circle(frame, (int(x), int(y)), int(10), (0, 0, 255), 1)

    for ((x, y)) in green:
        cv2.circle(frame, (int(x), int(y)), int(10), (0,  255, 0), 1)

    for ((x, y)) in blue:
        cv2.circle(frame, (int(x), int(y)), int(10), (255, 0,0), 1)

    angle = -angleBetweenPoints(green[0], red[0])*57
    robotAngle = angleBetweenPoints(green[0], blue[0])
    if robotAngle is not None:
        robotAngle = -robotAngle*57
        if blue[0][0] < green[0][0] and red[0][1] > green[0][1] and blue[0][1] <= green[0][1]:
            angle = abs(180-robotAngle) + abs(angle+180)
        elif blue[0][0] < green[0][0] and red[0][1] > green[0][1]:
            angle = 180+angle
            robotAngle = 180 + robotAngle
            angle = angle - robotAngle
        elif blue[0][0] < green[0][0] and red[0][1] < green[0][1] and blue[0][1] >= green[0][1]:
            angle = (180-angle)
            robotAngle = (180+robotAngle)
            angle = -(angle+robotAngle)
        elif blue[0][0] < green[0][0] and red[0][1] < green[0][1]:
            angle = -(180-angle)
            robotAngle = -(180 - robotAngle)
            angle = angle - robotAngle
        else:
            angle = angle - robotAngle

        print(angle)

    # Display the resulting frame
    cv2.imshow('Trackbars', frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
#vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
