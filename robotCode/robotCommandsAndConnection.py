#!/usr/bin/env pybricks-micropython
from socket import *
from time import *
from pybricks.hubs import EV3Brick
from pybricks.tools import wait
from pybricks.robotics import DriveBase
from pybricks.ev3devices import Motor
from pybricks.parameters import Port

ev3 = EV3Brick()
motor_left = Motor(Port.A)
motor_right = Motor(Port.B)
deploy_motor = Motor(Port.C)
claw_motor = Motor(Port.D)
robot = DriveBase(motor_left, motor_right, wheel_diameter=55.5, axle_track=236)
serverName = '192.168.94.92'
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
sentence = "bdf"


def drive_straight(direction, distance):
    robot.straight(-distance)
    print("hi")


def turn(direction, angle):
    if direction == "r":
        angle = angle * -1
    robot.turn(angle)


def run_motorClaw(speed, duration, isOpen):
    isOpen = True
    # Set the motor speed
    # run_time(speed, duration, then=Stop.HOLD, wait=False)
    claw_motor.dc(speed)
    # claw_motor.stop()
    wait(duration)


def run_motorDeploy(speed, duration, isDeployed):
    isDeployed = False
    deploy_motor.dc(speed)
    wait(duration)


# Call the run_motor function to run the motor forward for 2 seconds
def CloseClaw():
    run_motorClaw(-100, 500, False)
    print("Close")


def OpenClaw():
    run_motorClaw(100, 500, True)


def DeployBalls():
    run_motorDeploy(100, 10000, True)


def UnDeployBalls():
    run_motorDeploy(-50, 450, False)


# clientSocket.send(sentence.encode('utf-8'))
start = time()
while True:
    print("yo")
    modifiedSentence = clientSocket.recv(1024)
    print(time() - start)

    decoded = modifiedSentence.decode('utf-8')

    inp = decoded.split(" ")

    if inp[0] == 'd':
        direction = inp[1]
        distance = float(inp[2])

        print(direction)
        print(distance)
        drive_straight(direction, distance)

    if inp[0] == "t":
        direction = inp[1]
        distance = float(inp[2])
        turn(direction, distance)

    if decoded == "c":
        CloseClaw()
    if decoded == "oc":
        OpenClaw()

    if decoded == "deploy":
        DeployBalls()

    if decoded == "undeploy":
        UnDeployBalls()
    print(time() - start)
    print("Done diego")
    clientSocket.send(sentence.encode('utf-8'))

clientSocket.close()
