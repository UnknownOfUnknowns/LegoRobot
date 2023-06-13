import mouse
import time
from imageFilesReader import *
import matplotlib.pyplot as plt
# 928,787
def getImageNameFromPhone():
    time.sleep(0.5)
    mouse.move(928, 787)
    oldImage = getNewestImageName()
    mouse.click('left')
    image = getNewestImageName()
    while image == oldImage:
        image = getNewestImageName()
    return image
