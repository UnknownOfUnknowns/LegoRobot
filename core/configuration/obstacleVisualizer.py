from core.simulation import *
from core.objectdetectors import *

cam = cv2.VideoCapture(0)

def nothing(x):
    pass

cv2.namedWindow("Simulator")
cv2.createTrackbar("turn","Simulator", 0, 100, nothing)

cv2.createTrackbar("width back","Simulator", 10, 100, nothing)
cv2.createTrackbar("width front","Simulator", 10, 100, nothing)

cv2.createTrackbar("height","Simulator",10, 100, nothing)

while(True):
    #ret,frame = cam.read()
    frame = cv2.imread("../../resources/collisionSide.png")
    turn = cv2.getTrackbarPos("turn", "Simulator")
    green = greenGetter(frame)
    blue = blueGetter(frame)

    if len(green) == 1 and len(blue) == 1:

        obstacles = getFramePoints(frame)
        robotPoints = []
        green = green[0][0]
        wb = cv2.getTrackbarPos("width back", "Simulator")
        wf = cv2.getTrackbarPos("width front", "Simulator")
        h = cv2.getTrackbarPos("height", "Simulator")
        for x in range(int(green[0]-wb), int(green[0]+wf)):
            for y in range(int(green[1]-h), int(green[1]+h)):
                robotPoints.append((x,y))
        #minus is used in front of angle to compensate for different coordinate set
        turnedPoints = robotTurning(robotPoints, green, -turn*pi/50)
        for x,y in robotPoints:
            cv2.circle(frame, (x,y), 1, (255,0,0))
        for x, y in turnedPoints:
            cv2.circle(frame, (x, y), 1, (0, 0, 255))
        hits = False
        for x,y in turnedPoints:
            #Axis are switched in image hence we need to check the axis switched in the if statement
            if obstacles[y,x] == 255:
                hits = True
        print(hits)
    cv2.imshow('Simulator',frame)
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

cam.release()
cv2.destroyAllWindows()
