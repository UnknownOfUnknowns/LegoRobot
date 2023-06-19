from core.objectdetectors import *
from math import *
cap = cv2.VideoCapture(2)
cap.set(3, 1280)
cap.set(4, 720)


def nothing(x):
    pass


cv2.namedWindow("Trackbars")

cv2.createTrackbar("P1", "Trackbars", 10, 200, nothing)
cv2.createTrackbar("P2", "Trackbars", 10, 100, nothing)
cv2.createTrackbar("MIN", "Trackbars", 10, 100, nothing)
cv2.createTrackbar("MAX", "Trackbars", 10, 100, nothing)


while True:

    # Start reading the webcam feed frame by frame.
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the BGR image to HSV image.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get the new values of the trackbar in real time as the user changes
    # them
    p1 = cv2.getTrackbarPos("P1", "Trackbars")
    p2 = cv2.getTrackbarPos("P2", "Trackbars")
    min = cv2.getTrackbarPos("MIN", "Trackbars")
    max = cv2.getTrackbarPos("MAX", "Trackbars")
    if min == 0 or max == 0 or p1 == 0 or p2 == 0:
        continue
    balls = getBallsHough(frame, p1, p2, min, max)
    orangeBall = getOrangeBall(frame)
    print(len(balls) == 1)
    """
    if len(orangeBall) != 1:
        print("err")
        cv2.imshow("Trackbars", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
        continue
                """
    for ((x, y), radius) in balls:

        #if dist((x,y), orangeBall[0][0]) > 5:
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 5)

    cv2.imshow("Trackbars", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
