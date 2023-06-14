from Robot import CollisionSimulatedException
from ObstacleRecoveryStrategies import StandardStrategy, OrderType


def drive(robot, roboCam, balls, framePoints):
    roboCam.findBalls()
    roboCamDistance = roboCam.distanceToBall()
    newBalls = balls
    try:
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
            newBalls = list(filter(lambda x : x[0] != closestBall, newBalls))
            robot.driveToBall(closestBall, framePoints)
    except CollisionSimulatedException:
        if len(newBalls) != 0:
            drive(robot, roboCam, newBalls, framePoints)
        else:
            ball = balls[0]
            strategy = StandardStrategy(robot.front, robot.angle, ball).createStrategy()
            for method, value in strategy:
                if method == OrderType.DRIVE_COMMAND:
                    robot.drive(value, largeCam=True)
                else:
                    robot.driveToBall(value, framePoints)
