#!/usr/bin/env pybricks-micropython
from socket import *
from time import *
from pybricks.hubs import EV3Brick
from pybricks.tools import wait
ev3 = EV3Brick()
serverName = '192.168.0.239'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
sentence = "bdf"

start = time()
clientSocket.send(sentence.encode('utf-8'))
modifiedSentence = clientSocket.recv(1024)
print(time() - start)

decoded = modifiedSentence.decode('utf-8')
if decoded == "who is the laziest?":
    ev3.screen.draw_text(10,10, "Seier for sure")
    wait(5000)
print(time() - start)
clientSocket.close()
