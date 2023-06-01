from socket import *


def connect():
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('172.20.10.3', serverPort))

    serverSocket.listen(1)
    print('The server is ready to receive')

    connectionSocket, addr = serverSocket.accept()
    print("Robot connected")
    return connectionSocket


connectionSocket = connect()


def drive(distance):
    direction = 'f'
    if distance < 0:
        direction = 'b'
    sentence = 'd' + " " + direction + " " + distance
    connectionSocket.send(sentence.encode())


def turn(angle):
    direction = 'l'
    if angle < 0:
        angle = -angle
        direction = 'r'
    sentence = 't' + " " + direction + " " + str(angle)
    connectionSocket.send(sentence.encode())
    connectionSocket.recv(1024)


def closeClaw():
    connectionSocket.send('c')


def openClaw():
    connectionSocket.send('oc')


def deploy():
    connectionSocket.send('deploy')


def undeploy():
    connectionSocket.send('undeploy')
