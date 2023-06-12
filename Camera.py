import cv2
import imutils
vid = cv2.VideoCapture(0)

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
    ret, frame = vid.read()
    blue = blueGetter(frame)
    for ((x, y), radius) in blue:
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 1)
    # Display the resulting frame
    cv2.imshow('frame', frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
