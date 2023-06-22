

def isCloseToEdge(ball, framePoints):
    edges = []
    for i in range(1, 50):
        try:

            if framePoints[int(ball[1]), int(ball[0]-i)] == 255:
                edges.append("Left")
            if framePoints[int(ball[1]),int(ball[0] + i)] == 255:
                edges.append("Right")
            if framePoints[int(ball[1]+i), int(ball[0])] == 255:
                edges.append("Down")
            if framePoints[int(ball[1]-i), int(ball[0])] == 255:
                edges.append("Up")
        except:
            pass
    if edges == []:
        return None
    return list(dict.fromkeys(edges))

PICKUP_OFFSET = 250
def getIntermediatePosition(ball, frameDir : list):
    x,y = ball
    if "Left" in frameDir:
        x,y =  (x + PICKUP_OFFSET, y)
    if "Right" in frameDir:
        x,y =  (x - PICKUP_OFFSET, y)
    if "Down" in frameDir:
        x, y = (x, y-PICKUP_OFFSET)
    if "Up" in frameDir:
        x,y =  (x, y+PICKUP_OFFSET)

    return (x,y)


CLOSE_OFFSET = 10
def getCloseOffset(ball, frameDir):
    x,y = ball
    if "Left" in frameDir:
        x, y = (x + CLOSE_OFFSET, y)
    if "Right" in frameDir:
        x,y =  (x - CLOSE_OFFSET, y)
    if "Down" in frameDir:
        x, y = (x, y-CLOSE_OFFSET)
    if "Up" in frameDir:
        x,y =  (x, y+CLOSE_OFFSET)

    return (x,y)