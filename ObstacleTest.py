import unittest

import numpy as np

from math import *

class MyTestCase(unittest.TestCase):

    def test_something(self):

        self.assertEqual(True, True)  # add assertion here

    def test_angle(self):

        self.green = (400, 300)
        self.blue = (292, 279)
        self.front = (293,284)
        closestBall = (260, 220)
        robotVector = (self.blue[0] - self.green[0], (self.blue[1] - self.green[1]))
        ballVector = (closestBall[0] - self.blue[0]  , (closestBall[1] - self.blue[1]))
        scalarProduct = robotVector[0] * ballVector[0] + robotVector[1] * ballVector[1]
        lengthMultiple = sqrt(robotVector[0] ** 2 + robotVector[1] ** 2) * sqrt(ballVector[0] ** 2 + ballVector[1] ** 2)
        vinkel = acos(scalarProduct / lengthMultiple) * 57.2958
        print(vinkel)


if __name__ == '__main__':
    unittest.main()
