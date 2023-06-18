import cv2
import numpy as np
from configLoader import saveConfig
from util.imageFilesReader import getNewestPhoneImage
cap = cv2.VideoCapture(4)
cap.set(3, 1280)
cap.set(4, 720)


def nothing(x):
    pass


def createBarsForColorFrame(windowName):
    cv2.namedWindow(windowName)
    cv2.createTrackbar("L - H", windowName, 0, 179, nothing)
    cv2.createTrackbar("L - S", windowName, 0, 255, nothing)
    cv2.createTrackbar("L - V", windowName, 0, 255, nothing)
    cv2.createTrackbar("U - H", windowName, 179, 179, nothing)
    cv2.createTrackbar("U - S", windowName, 255, 255, nothing)
    cv2.createTrackbar("U - V", windowName, 255, 255, nothing)


def createBarsForPointFrame(windowName, pointCount):
    cv2.namedWindow(windowName)
    for n in range(1, pointCount + 1):
        cv2.createTrackbar("x" + str(n), windowName, 0, 1280, nothing)
        cv2.createTrackbar("y" + str(n), windowName, 0, 720, nothing)

def pointConfigActions(frame, windowName, pointCount):

    for n in range(1, pointCount + 1):
        x = cv2.getTrackbarPos("x" + str(n), windowName)
        y = cv2.getTrackbarPos("y" + str(n), windowName)

        cv2.circle(frame, (int(x), int(y)), int(10), (0, 255, 0), 2)
    scale = (640, 360)
    frame = cv2.resize(frame, scale)
    return frame

def pointGetValuesToSave(windowName, pointCount):
    res = []
    for n in range(1, pointCount + 1):
        x = cv2.getTrackbarPos("x" + str(n), windowName)
        y = cv2.getTrackbarPos("y" + str(n), windowName)
        res.append((windowName + " " + str(n), (x,y)))
    return res

def colorConfigActions(frame, windowName):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L - H", windowName)
    l_s = cv2.getTrackbarPos("L - S", windowName)
    l_v = cv2.getTrackbarPos("L - V", windowName)
    u_h = cv2.getTrackbarPos("U - H", windowName)
    u_s = cv2.getTrackbarPos("U - S", windowName)
    u_v = cv2.getTrackbarPos("U - V", windowName)

    lower_range = np.array([l_h, l_s, l_v])
    upper_range = np.array([u_h, u_s, u_v])

    hsv = cv2.GaussianBlur(hsv, (11, 11), 0)
    mask = cv2.inRange(hsv, lower_range, upper_range)

    res = cv2.bitwise_and(frame, frame, mask=mask)

    mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    scale = (640, 360)
    mask_3 = cv2.resize(mask_3, scale)
    res = cv2.resize(res, scale)

    stacked = np.hstack((mask_3, cv2.resize(frame, scale), res))
    return stacked


def colorGetValuesToSave(windowName):
    l_h = cv2.getTrackbarPos("L - H", windowName)
    l_s = cv2.getTrackbarPos("L - S", windowName)
    l_v = cv2.getTrackbarPos("L - V", windowName)
    u_h = cv2.getTrackbarPos("U - H", windowName)
    u_s = cv2.getTrackbarPos("U - S", windowName)
    u_v = cv2.getTrackbarPos("U - V", windowName)

    lower_range = [l_h, l_s, l_v]
    upper_range = [u_h, u_s, u_v]
    return [(windowName + " lower", lower_range), (windowName + " upper", upper_range)]


def blueConfigActions(frame):
    return colorConfigActions(frame, "blue")


def blueGetValuesToBeSaved():
    return colorGetValuesToSave("blue")


def blueConfigSetup():
    createBarsForColorFrame("blue")
    return "blue", blueConfigActions, blueGetValuesToBeSaved


def yellowConfigActions(frame):
    return colorConfigActions(frame, "yellow")


def yellowGetValuesToBeSaved():
    return colorGetValuesToSave("yellow")


def yellowConfigSetup():
    createBarsForColorFrame("yellow")
    return "yellow", yellowConfigActions, yellowGetValuesToBeSaved


def greenConfigActions(frame):
    return colorConfigActions(frame, "green")


def greenGetValuesToBeSaved():
    return colorGetValuesToSave("green")


def greenConfigSetup():
    createBarsForColorFrame("green")
    return "green", greenConfigActions, greenGetValuesToBeSaved


def redConfigActions(frame):
    return colorConfigActions(frame, "red")


def redGetValuesToBeSaved():
    return colorGetValuesToSave("red")


def redConfigSetup():
    createBarsForColorFrame("red")
    return "red", redConfigActions, redGetValuesToBeSaved


def quadrantGetValuesToBeSaved():
    return pointGetValuesToSave("quadrant", 4)

def quadrantConfigActions(frame):
    return pointConfigActions(frame, "quadrant", 4)

def quadrantConfigSetup():
    createBarsForPointFrame("quadrant", 4)
    return "quadrant", quadrantConfigActions, quadrantGetValuesToBeSaved

def goalGetValuesToBeSaved():
    return pointGetValuesToSave("goal", 2)

def goalConfigActions(frame):
    return pointConfigActions(frame, "goal", 2)

def goalConfigSetup():
    createBarsForPointFrame("goal", 2)
    return "goal", goalConfigActions, goalGetValuesToBeSaved


def identity(frame):
    return frame


def identityValues(name):
    return []


windows = [goalConfigSetup, quadrantConfigSetup, blueConfigSetup, yellowConfigSetup, greenConfigSetup, redConfigSetup]
stepCount = 0
windowName, currentAction, getValuesAction = windows[0]()

fileName = ""
saveMode = False
newConfig = {}
while True:
    ret, frame = cap.read()
    #frame = getNewestPhoneImage()
    frame = currentAction(frame)

    cv2.imshow(windowName, frame)

    key = cv2.waitKey(1)
    if saveMode:
        if key == 13:
            saveConfig(fileName, newConfig)
            break
        try:
            fileName += chr(key)
        except:
            pass
        continue
    if key == 27:
        break
    if key == 110:
        stepCount += 1
        if not stepCount < len(windows):
            continue

        for name, value in getValuesAction():
            newConfig[name] = value
        cv2.destroyAllWindows()
        windowName, currentAction, getValuesAction = windows[stepCount]()

    if key == ord('s'):
        saveMode = True

cap.release()
cv2.destroyAllWindows()
