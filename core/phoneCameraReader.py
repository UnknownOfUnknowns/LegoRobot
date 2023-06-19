import cv2

phoneCamera = cv2.VideoCapture(2)

def getPhoneImage():
    while True:
        success, frame = phoneCamera.read()
        if success:
            return frame