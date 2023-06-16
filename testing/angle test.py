from math import atan, pi

def angleBetweenPoints(p1, p2):
    xGrowth = p2[0] - p1[0]
    yGrowth= p2[1] - p1[1]
    if xGrowth > 0:
        return atan(yGrowth / xGrowth)
    if xGrowth == 0 and yGrowth > 0:
        return pi / 2
    if xGrowth < 0 and yGrowth >= 0:
        return atan(yGrowth / xGrowth)+pi
    if xGrowth == 0 and yGrowth < 0:
        return -pi/2
    if xGrowth < 0 and yGrowth < 0:
        return atan(yGrowth / xGrowth)-pi

