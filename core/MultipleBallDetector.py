from Robot import *
from sender import *
from objectdetectors import *
from robotCamera import RobotCamera
from util.mousecontroller import *
from core.driveController import *
from ObstacleRecoveryStrategies import DeliverToSmallGoalStrategy

sender = Sender()
frame = cv2.VideoCapture(2)
frame.set(3, 1280)
frame.set(4, 720)


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

while True:
    phoneImgName = getNewestImageName() #getImageNameFromPhone()
    _, fr = frame.read()
    #fr = cv2.imread("collisionSide.png")
    time.sleep(0.5)
    frames = [getImage(phoneImgName)]

    framePoints = getFramePoints(fr)
    balls = getBallsHough(fr)
    green = greenGetter(fr)
    blue = blueGetter(fr)
    yellow = yellowGetter(fr)

    for ((x, y), radius) in green:
        cv2.circle(fr, (int(x), int(y)), int(radius), (0, 255, 0), 1)
    for ((x, y), radius) in blue:
        cv2.circle(fr, (int(x), int(y)), int(radius), (0, 255, 0), 1)
    for ((x, y), radius) in yellow:
        cv2.circle(fr, (int(x), int(y)), int(radius), (0, 255, 0), 1)
    for ((x, y), radius) in balls:
        # To see the centroid clearly

        cv2.circle(fr, (int(x), int(y)), int(radius), (0, 255, 255), 5)

    cv2.imshow("t", fr)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

    if len(green) > 0 and len(blue) > 0:
        ((x, y), _) = green[0]
        centrumGreen = (x,y)
        ((x, y), _) = blue[0]
        centrumBlue = (x,y)
        ((x, y), _) = yellow[0]
        centrumYellow = (x,y)
       # print(centrumBlue,centrumGreen)
        robot = Robot(centrumBlue,centrumGreen,centrumYellow, sender)


        if len(currentStrategy) > 0 and currentStrategy[0][0] == OrderType.TARGET and dist(robot.frontPoint, currentStrategy[0][1]) < 5:
            currentStrategy.pop(0)

        if len(currentStrategy) > 0:
            order = currentStrategy[0]
            if order[0] == OrderType.TARGET:
                robot.driveToBall(order[1], framePoints)
                continue
        roboCam = RobotCamera(frames)

        roboCam.findBalls()

        if len(balls) == 0 and roboCam.detectedBall is None:
            currentStrategy = DeliverToSmallGoalStrategy().createStrategy()
            continue

        roboCamDistance = roboCam.distanceToBall()
        if roboCamDistance == 0:
            robot.pickUpBall()
        elif roboCamDistance > 0:
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
            closestBall = robot.findClosestBall(balls)
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
