from core.objectdetectors import getBallsHough, getFramePointsPhone
from core.configuration.configLoader import robot_cam_config
"""
frame = cv2.VideoCapture(3)
#fhigh = cv2.VideoCapture(0)
frame.set(3, 480)
frame.set(4, 320)
"""


class RobotCamera:

    def __init__(self, images):
        self.images = images
        self.detectedBall = None

        self.middle = 1920 / 2
        self.threshold = (self.middle - 655) / 2

    def relationToThreshold(self):
        if self.detectedBall is None:
            return 0

        if self.detectedBall[0][0] < (self.middle - self.threshold):
            return -1
        if self.detectedBall[0][0] > (self.middle + self.threshold):
            return 1
        return 0

    def findBalls(self):
        for image in self.images:
            balls = getBallsHough(image, 200, 15, 90, 100)
            #second condition is to avoid balls being detected in the bay
            if len(balls) > 1:
                print("many balls")
            if len(balls) == 1 and balls[0][0][1] < 860:
                self.detectedBall = balls[0]
                return

    def findOrange(self):
        for image in self.images:
            balls = getBallsHough(image, 200, 10, 90, 100)
            # second condition is to avoid balls being detected in the bay
            balls.sort(key=lambda x: x[0][1])

            if len(balls) >= 1 and balls[0][0][1] < 860:
                self.detectedBall = balls[0]
                return

    def distanceToBall(self):
        if self.detectedBall is None:
            return -1
        return max(0, 714 - self.detectedBall[0][1])

    def inPositionToOpen(self):
        image = self.images[0]
        framePoints = getFramePointsPhone(image)
        hitCount = 0
        for x in [300, 390]:
            for point in framePoints[x]:
                if point == 255:
                    hitCount += 1
                    break
        return hitCount == 2

    def findFirstRedEdge(self):
        image = self.images[0]
        framePoints = getFramePointsPhone(image)
        for x in range(0, len(framePoints)):
                if framePoints[x, 960] == 255:
                    return x
        return -1
    def isStraightOnForOpenClaw(self, greenPoints):
        x, _ = greenPoints[0]
        if x < robot_cam_config["left left"]:
            return 1
        if x >  robot_cam_config["left right"]:
            return -1
        x, y = greenPoints[1]
        if x <  robot_cam_config["right left"]:
            return 1
        if x >  robot_cam_config["right right"]:
            return -1

        return 0

    #680, 1170, 551

    def driveToPickupByEdge(self):
        image = self.images[0]
        frame = getFramePointsPhone(image)
        count = 0
        for i in range(730, 1100):
            for j in range(300, 700):
                if frame[j,i] == 255:
                    count +=1
                    #make sure it is not an erroneous detection
                    if count > 100:
                        return False

        return True
