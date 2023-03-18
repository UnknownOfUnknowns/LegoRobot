
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
