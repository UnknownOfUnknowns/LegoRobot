from core.sender import Sender
import time
sender = Sender()

while True:
    sender.turn(0.1)
    time.sleep(0.1)
    sender.drive(1)
