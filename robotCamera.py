import cv2
from objectdetectors import getBallsHough
frame = cv2.VideoCapture(3)
#fhigh = cv2.VideoCapture(0)
frame.set(3, 480)
frame.set(4, 320)



class RobotCamera:

    def __init__(self, images):
        self.images = images
        self.detectedBall = None

        self.middle = 1920/2
        self.threshold = (self.middle-655)/2


    def relationToThreshold(self):
        if self.detectedBall is None:
            return 0

        if self.detectedBall[0][0] < (self.middle-self.threshold):
            return -1
        if self.detectedBall[0][0] > (self.middle + self.threshold):
            return 1
        return 0

    def findBalls(self):
        for image in self.images:
            balls = getBallsHough(image, 200, 14, 93, 93)
            if len(balls) == 1:
                self.detectedBall = balls[0]
                return
        self.detectedBall = None

    def distanceToBall(self):
        if self.detectedBall is None:
            return -1
        return max(0, 714 - self.detectedBall[0][1])
"""
while True:
    #_, frh = fhigh.read()
    frames = []
    for i in range(0,5):
        _, fr = frame.read()
        frames.append(fr)

    roboCam = RobotCamera(frames)
    roboCam.findBalls()
    print(roboCam.distanceToBall())
    if roboCam.detectedBall is not None:
        ((x,y), radius) = roboCam.detectedBall
        cv2.circle(frames[0], (int(x), int(y)), int(radius), (0, 255, 255), 5)

    cv2.imshow("Robot camera", frames[0])
    #cv2.imshow("High cam", frh)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
"""