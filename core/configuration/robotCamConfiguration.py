from util.imageFilesReader import getNewestPhoneImage
from core.robotCamera import RobotCamera
import cv2
from core.objectdetectors import greenGetterRobot
from configLoader import saveConfig

image = getNewestPhoneImage()

greenPoints = greenGetterRobot(image)

greenPoints.sort(key=lambda x: x[0][0])

newConfig = {}

assert len(greenPoints) == 2

((x,_),_) = greenPoints[0]

newConfig["left left"] = x - 40
newConfig["left right"] = x + 40


((x,_),_) = greenPoints[1]

newConfig["right left"] = x - 40
newConfig["right right"] = x + 40

saveConfig("robotCamConfig", newConfig)
