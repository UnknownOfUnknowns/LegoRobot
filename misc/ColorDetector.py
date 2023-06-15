from core import MultipleBallDetector as mbd

import cv2


imcap = cv2.VideoCapture(0)

imcap.set(3, 1280)
imcap.set(4, 720)


while True:
    success, frame = imcap.read() # capture frame from video

    width, height = frame.shape[:2]
    # converting image from color to grayscale
    for ((x, y), radius) in mbd.getBallCoordinates(frame):

        # To see the centroid clearly
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 5)
        cv2.imwrite("../resources/circled_frame.png", cv2.resize(frame, (int(height / 2), int(width / 2))))
        cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)

    cv2.imshow('court cam', frame)
    # loop will be broken when 'q' is pressed on the keyboard
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

imcap.release()
cv2.destroyWindow('face_detect')
