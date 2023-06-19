from Robot import *
from sender import *
from objectdetectors import *
from robotCamera import RobotCamera
from util.mousecontroller import *
from core.driveController import *
from ObstacleRecoveryStrategies import DeliverToSmallGoalStrategy
from edgeFunctions import isCloseToEdge, getIntermediatePosition
from phoneCameraReader import getPhoneImage
import matplotlib.pyplot as plt
sender = Sender()
frame = cv2.VideoCapture(0)
frame.set(3, 1280)
frame.set(4, 720)

def showCaptures(caps):
    for x in caps:
        bls = getBallsHough(x, 200, 15, 90, 100)
        plt.imshow(x)
        print("balls")
        print(bls)
        plt.show()
# frame = cv2.resize(frame, (960, 540))

# width, height = frame.shape[:2]


def showImage(image):
    while True:
        cv2.imshow("image", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


# court_box =  mapOutFrame(frame)
# for box in court_box:
#    cv2.rectangle(frame, box, (0, 0, 255), 2)

# court_box = court_box[0]
# cropped = frame[court_box[1]:court_box[1]+court_box[3], court_box[0]:court_box[0]+court_box[2]]
currentStrategy = []
closePickupMode = False
lastRoundBallCount = 0
lastTargetBall = None
retryCount = 0
while True:
    #phoneImgName = getNewestImageName()
    readOk, fr = frame.read()
    if not readOk:
        continue
    # fr = cv2.imread("collisionSide.png")

    frames = [getPhoneImage(), getPhoneImage(), getPhoneImage()]

    framePoints = getFramePoints(fr)
    allBalls = getBallsHough(fr)
    green = greenGetter(fr)
    blue = blueGetter(fr)
    yellow = yellowGetter(fr)
    balls =[]
    orangeBall = getOrangeBall(fr)
    if len(orangeBall) == 0:
        allBalls = balls
    elif len(orangeBall) == 1 and len(allBalls) > 1:
        for ((x, y), radius) in allBalls:
            if dist((x,y), orangeBall[0][0]) > 10:
                balls.append(((x,y),radius))
    elif len(allBalls) == 1:
        balls = orangeBall
    for ((x, y), radius) in green:
        cv2.circle(fr, (int(x), int(y)), int(radius), (0, 255, 0), 1)
    for ((x, y), radius) in blue:
        cv2.circle(fr, (int(x), int(y)), int(radius), (0, 255, 0), 1)
    for ((x, y), radius) in yellow:
        cv2.circle(fr, (int(x), int(y)), int(radius), (0, 255, 0), 1)
    for ((x, y), radius) in balls:
        cv2.circle(fr, (int(x), int(y)), int(radius), (0, 255, 255), 5)

    cv2.imshow("t", fr)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

    if len(green) > 0 and len(blue) > 0:
        ((x, y), _) = green[0]
        centrumGreen = (x, y)
        ((x, y), _) = blue[0]
        centrumBlue = (x, y)
        ((x, y), _) = yellow[0]
        centrumYellow = (x, y)
        # print(centrumBlue,centrumGreen)
        robot = Robot(centrumBlue, centrumGreen, centrumYellow, sender)

        if len(currentStrategy) > 0 and currentStrategy[0][0] == OrderType.TARGET and dist(robot.frontPoint, currentStrategy[0][1]) < 100:
            currentStrategy.pop(0)

        if len(currentStrategy) > 0:
            order = currentStrategy[0]
            robot.executeStrategyElement(order, framePoints)
            continue

        roboCam = RobotCamera(frames)
        if len(allBalls) < 1:
            roboCam.findOrange()
        else:
            roboCam.findBalls()



        roboCamDistance = roboCam.distanceToBall()

        if len(allBalls) < lastRoundBallCount - 1 and roboCamDistance == -1:
            continue
        else:
            lastRoundBallCount = len(allBalls)
        if roboCamDistance >= 0:
            closePickupMode = False
        if (roboCamDistance == 0 or not roboCam.driveToPickupByEdge() == True) and len(allBalls) == 0 and roboCam.detectedBall is not None:
            robot.closeBay()
            robot.drive(-100)
        elif (roboCamDistance == 0 or not roboCam.driveToPickupByEdge() == True) and roboCam.detectedBall is not None:
            robot.pickUpBall()
            robot.drive(-100)
        elif roboCamDistance > 0:
            #we have a ball on the small cam so we dont save it for the large cam later on
            lastTargetBall = None
            isStraightOn = roboCam.relationToThreshold()
            if isStraightOn < 0:
                robot.turnRobot(10)
            elif isStraightOn > 0:
                robot.turnRobot(-10)
            else:
                driveDistance = roboCamDistance
                if driveDistance < 50:
                    driveDistance = 50
                else:
                    driveDistance *= 1.5
                robot.drive(driveDistance, largeCam=False)
        else:
            if len(balls) == 0 and roboCam.detectedBall is None:
                currentStrategy = DeliverToSmallGoalStrategy().createStrategy()
                continue

            closestBall = robot.findClosestBall(balls)
            if retryCount > 3:
                lastTargetBall = None
                retryCount = 0
            if lastTargetBall is None:
                lastTargetBall = closestBall
            if dist(closestBall, lastTargetBall) > 20:
                retryCount += 1
                robot.driveToBall(lastTargetBall,framePoints)
                continue
            closeToEdge = isCloseToEdge(closestBall, framePoints)
            if closeToEdge is not None and not closePickupMode:
                closePickupMode = True
                currentStrategy = [(OrderType.TARGET, getIntermediatePosition(closestBall, closeToEdge))]
                continue
            lastTargetBall = closestBall
            robot.driveToBall(closestBall, framePoints)


"""
for box in getRobotCoordinates(frame):
    cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)

lowerBound = (20, 0, 50)
upperBound = (50, 205, 255)
mask = cv2.inRange(hsv, lowerBound, upperBound)
showImage(mask)
"""

"""
    for ((x, y), radius) in getBallCoordinates(fr):
        # To see the centroid clearly

        cv2.circle(fr, (int(x), int(y)), int(radius), (0, 255, 255), 5)
        # cv2.imwrite("circled_course.png", cv2.resize(frame, (int(height / 2), int(width / 2))))
        cv2.circle(fr, (int(x), int(y)), 5, (0, 0, 255), -1)
"""
