import numpy as np

class CourtObject:
    def __init__(self, position):
        self.position = position


class Robot(CourtObject):
    def __init__(self, position, angle):
        super().__init__(position)
        self.angle = angle


class Ball(CourtObject):
    def __init__(self, position):
        super().__init__(position)


class Court:
    def __init__(self, w, h, balls, robot):
        self.coordinates = np.zeros(shape=(w, h))
        self.balls = balls
        self.robot = robot

    def registerObstructions(self, frame):
        self.coordinates = frame


