import cv2


imcap = cv2.VideoCapture(1)
image = cv2.imread("../coverImg.jfif")
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml")

while True:
    success, img = imcap.read() # capture frame from video
    # converting image from color to grayscale
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Getting corners around the face
    # 1.3 = scale factor, 5 = minimum neighbor can be detected
    faces = faceCascade.detectMultiScale(imgGray, 1.3, 5)

    # drawing bounding box around face
    for (x, y, w, h) in faces:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), -1)

    eyes = eyeCascade.detectMultiScale(imgGray)
    # drawing bounding box for eyes
    for (ex, ey, ew, eh) in eyes:
        img = cv2.rectangle(img, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 3)
    # displaying image with bounding box
    cv2.imshow('face_detect', img)
    # loop will be broken when 'q' is pressed on the keyboard
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

imcap.release()
cv2.destroyWindow('face_detect')
