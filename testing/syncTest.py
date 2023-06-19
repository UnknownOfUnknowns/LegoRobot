import cv2

from core.sender import Sender
from core.phoneCameraReader import getPhoneImage
s = Sender()

cap = cv2.VideoCapture(0)

cap.set(3, 1280)
cap.set(4, 720)
while True:
    phoneImg = getPhoneImage()
    _, largeImg = cap.read()

    print("ok")

    s.drive(1000)