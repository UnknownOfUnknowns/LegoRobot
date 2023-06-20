

def isCloseToEdge(ball, framePoints):
    for i in range(1, 50):
        try:

            if framePoints[int(ball[1]), int(ball[0]-i)] == 255:
                return "Left"
            if framePoints[int(ball[1]),int(ball[0] + i)] == 255:
                return "Right"
            if framePoints[int(ball[1]+i), int(ball[0])] == 255:
                return "Down"
            if framePoints[ int(ball[1]-i), int(ball[0])] == 255:
                return "Up"
        except:
            pass
    return None

PICKUP_OFFSET = 250
def getIntermediatePosition(ball, frameDir):
    x,y = ball
    if frameDir == "Left":
        return (x + PICKUP_OFFSET, y)
    if frameDir == "Right":
        return (x - PICKUP_OFFSET, y)
    if frameDir == "Down":
        return (x, y-PICKUP_OFFSET)
    if frameDir == "Up":
        return (x, y+PICKUP_OFFSET)

    return (x,y)


CLOSE_OFFSET = 50
def getCloseOffset(ball, frameDir):
    x,y = ball
    if frameDir == "Left":
        return (x + CLOSE_OFFSET, y)
    if frameDir == "Right":
        return (x - CLOSE_OFFSET, y)
    if frameDir == "Down":
        return (x, y-CLOSE_OFFSET)
    if frameDir == "Up":
        return (x, y+CLOSE_OFFSET)

    return (x,y)