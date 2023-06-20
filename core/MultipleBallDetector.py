import enum

from Robot import *
from sender import *
from simulation import robotMoving, calculateRobotCoordinates
from objectdetectors import *
from robotCamera import RobotCamera
from util.mousecontroller import *
from core.driveController import *
from ObstacleRecoveryStrategies import DeliverToSmallGoalStrategy
from edgeFunctions import isCloseToEdge, getIntermediatePosition, getCloseOffset
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


def drawCirlesOnFrame(fr, green, blue, yellow, balls):
    for ((x, y), radius) in green:
        cv2.circle(fr, (int(x), int(y)), int(radius), (0, 255, 0), 1)
    for ((x, y), radius) in blue:
        cv2.circle(fr, (int(x), int(y)), int(radius), (0, 255, 0), 1)
    for ((x, y), radius) in yellow:
        cv2.circle(fr, (int(x), int(y)), int(radius), (0, 255, 0), 1)
    for ((x, y), radius) in balls:
        cv2.circle(fr, (int(x), int(y)), int(radius), (0, 255, 255), 5)

    return fr

currentStrategy = []
closePickupMode = False
lastRoundBallCount = 11
lastTargetBall = None
retryCount = 0
prevCommand = None
class ControlTypes(enum.Enum):
    PICK_UP_ORANGE = 1
    PICK_UP_WHITE = 2
    GO_TO_GOAL = 3
    RETRY_OLD_TARGET = 4
    FOLLOW_STRATEGY = 5
    GET_NEW_FRAME = 6
    DRIVE_NORMALLY = 7


def determineDriveMode(allBalls, activeBalls, robot, robotCamera, framePoints):
    if len(currentStrategy) > 0 and currentStrategy[0][0] == OrderType.TARGET and dist(robot.frontPoint,currentStrategy[0][1]) < 30:
        currentStrategy.pop(0)

        if len(currentStrategy) == 0:
            return determineDriveMode(allBalls, activeBalls, robot, robotCamera, framePoints)
        else:
            return ControlTypes.FOLLOW_STRATEGY
    if len(currentStrategy) != 0:
        return ControlTypes.FOLLOW_STRATEGY

    robotCamera.findBalls()
    whiteUnderRobot = robotCamera.detectedBall
    if whiteUnderRobot is not None and len(allBalls) != 0:
        currentStrategy.clear()
        return ControlTypes.PICK_UP_WHITE
    robotCamera.findOrange()
    orangeUnderRobot = robotCamera.detectedBall

    if orangeUnderRobot is not None and len(allBalls) == 0:
        currentStrategy.clear()
        return ControlTypes.PICK_UP_ORANGE
    if len(allBalls) < lastRoundBallCount and prevCommand != ControlTypes.GET_NEW_FRAME:
        return ControlTypes.GET_NEW_FRAME
    calcBalls = [x[0] for x in activeBalls]
    return getNewTargetBallStrategy(calcBalls, framePoints, robot)

    """
    if len(allBalls) < lastRoundBallCount:
        if prevCommand == ControlTypes.RETRY_OLD_TARGET:
            return ControlTypes.DRIVE_NORMALLY
        if prevCommand == ControlTypes.GET_NEW_FRAME and lastTargetBall is not None:
            return ControlTypes.RETRY_OLD_TARGET
        return ControlTypes.GET_NEW_FRAME
    elif len(allBalls) == 0:
        return ControlTypes.GO_TO_GOAL
    else:
        if lastTargetBall is not None and doesOldBallHaveACloseNewBalls(lastTargetBall, allBalls) and prevCommand != ControlTypes.RETRY_OLD_TARGET:
            return ControlTypes.RETRY_OLD_TARGET
        return ControlTypes.DRIVE_NORMALLY
"""


def doesOldBallHaveACloseNewBalls(last, all):
    for cor, r in all:
        if dist(last, cor) < 10:
            return True
    return False


def filterBalls(orange, all):
    if len(orange) == 0:
        return all
    elif len(orange) == 1 and len(allBalls) > 1:
        interBalls = []
        for ((x, y), radius) in allBalls:
            if dist((x,y), orangeBall[0][0]) > 10:
                interBalls.append(((x,y),radius))

        return interBalls
    elif len(allBalls) == 1:
        return orangeBall
    return all

def doesRobotHitObstacle(image, court, robotPoints, target):
    tx, ty= target
    tx, ty = int(tx), int(ty)
    for point in robotPoints:
        cv2.line(image, point, (tx,ty), (10, 10 ,10), 1)
    for x in range(0,1280):
        for y in range(0,720):
            if court[y,x] == 255 and (image[y,x] == [10,10,10]).all():
                return True
    return False




def getNewTargetBallStrategy(balls, framePoints, robot):
    if len(balls) == 0:
        return []
    priorityArray = [balls[0]]
    for ball in balls[1:]:
        if isCloseToEdge(ball, framePoints):
            priorityArray.append(ball)
        angle = robot.calculateAngleToBall(ball)
        if abs(angle) > 90:
            priorityArray.append(ball)
        distance = robot.calculateDistance(ball)
        if distance < robot.calculateDistance(priorityArray[0]):
            priorityArray.insert(0, ball)
        else:
            priorityArray.append(ball)

    chosenBall = priorityArray[0]

    commands =[]
    close = isCloseToEdge(chosenBall, framePoints)

    if close is not None:
        commands.append((OrderType.TARGET, getIntermediatePosition(chosenBall, close)))
        commands.append((OrderType.TARGET, getCloseOffset(chosenBall, close)))
    else:
        robotCor = calculateRobotCoordinates(robot)

        robotAngle = angleBetweenPoints(robot.green, robot.frontPoint)
        if robotAngle is not None:
            robotAngle = -robotAngle * 57
        else:
            robotAngle = 0
        if doesRobotHitObstacle(fr, framePoints, robotCor, chosenBall):

            strategy = StandardStrategy(robot.frontPoint, robotAngle, chosenBall)
            commands = strategy.createStrategy()

        commands.append((OrderType.TARGET, chosenBall))
    return commands





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

    orangeBall = getOrangeBall(fr)
    balls = filterBalls(orangeBall, allBalls)


    cv2.imshow("t", drawCirlesOnFrame(fr, green, blue, yellow, balls))
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

    if len(green) > 0 and len(blue) > 0 and len(yellow) > 0:
        ((x, y), _) = green[0]
        centrumGreen = (x, y)
        ((x, y), _) = blue[0]
        centrumBlue = (x, y)
        ((x, y), _) = yellow[0]
        centrumYellow = (x, y)

        robot = Robot(centrumBlue, centrumGreen, centrumYellow, sender)
        roboCam = RobotCamera(frames)

        driveMode = determineDriveMode(allBalls, balls, robot, roboCam, framePoints)
        prevCommand = driveMode
        if driveMode == ControlTypes.DRIVE_NORMALLY:
            lastRoundBallCount = len(allBalls)
            closestBall = robot.findClosestBall(balls)
            lastTargetBall = closestBall
            closeToEdge = isCloseToEdge(closestBall, framePoints)
            if closeToEdge is not None and not closePickupMode:
                closePickupMode = True
                currentStrategy = [(OrderType.TARGET, getIntermediatePosition(closestBall, closeToEdge))]
                continue
            robot.driveToBall(closestBall, framePoints)
        elif driveMode == ControlTypes.FOLLOW_STRATEGY:
            order = currentStrategy[0]
            robot.executeStrategyElement(order, framePoints)
        elif driveMode == ControlTypes.GET_NEW_FRAME:
            continue
        elif driveMode == ControlTypes.GO_TO_GOAL:
            currentStrategy = DeliverToSmallGoalStrategy().createStrategy()
        elif driveMode == ControlTypes.PICK_UP_ORANGE:
            roboCam.findOrange()
            roboCamDistance = roboCam.distanceToBall()
            if roboCamDistance == 0 or not roboCam.driveToPickupByEdge() == True:
                lastRoundBallCount -= 1
                robot.closeBay()
                robot.drive(-100)
            elif roboCamDistance > 0:
                # we have a ball on the small cam so we dont save it for the large cam later on
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
        elif driveMode == ControlTypes.PICK_UP_WHITE:
            roboCam.findBalls()
            roboCamDistance = roboCam.distanceToBall()
            if (roboCamDistance == 0 or not roboCam.driveToPickupByEdge() == True):
                lastRoundBallCount -=1
                robot.pickUpBall()
                robot.drive(-100)
            elif roboCamDistance > 0:
                # we have a ball on the small cam so we dont save it for the large cam later on
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
        elif driveMode == ControlTypes.RETRY_OLD_TARGET:
            robot.driveToBall(lastTargetBall, framePoints)
        else:
            currentStrategy = driveMode
        """
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
