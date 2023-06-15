import math


s = Sender()
while True:

    name = getImageNameFromPhone()
    time.sleep(2)
    frame = getImage(name)
    robot = Robot((1,1),(2,2),(3,3), s)
    camera = RobotCamera([frame])
    if camera.inPositionToOpen():
        s.openClaw()
        s.turn(-5)
        s.deploy()
    else:
        distance = 300 - camera.findFirstRedEdge()
        if 0 > distance > -50:
            distance = -50
        elif distance < 50:
            distance = 50
        robot.drive(distance, largeCam=False)
