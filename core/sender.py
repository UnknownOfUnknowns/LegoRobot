from socket import *


class Sender:
    def __init__(self):

        self.connectionSocket = self.connect()

    def connect(self):
        serverPort = 12001
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind(('192.168.94.92', serverPort))

        serverSocket.listen(1)
        print('The server is ready to receive')

        connectionSocket, addr = serverSocket.accept()
        print("Robot connected")
        return connectionSocket

    def send(self, command):
        try:
            self.connectionSocket.send(command.encode())
            self.connectionSocket.recv(1024)

        except ConnectionError as e:
            print(e)
            print("con err")
            self.connectionSocket = self.connect()
    def drive(self, distance):
        direction = 'f'
        if distance < 0:
            direction = 'b'

        sentence = 'd' + " " + direction + " " + str(distance)
        print(sentence)
        self.send(sentence)

    def turn(self, angle):
        direction = 'l'
        if angle < 0:
            angle = -angle
            direction = 'r'
        sentence = 't' + " " + direction + " " + str(angle)
        self.send(sentence)

    def closeClaw(self):
        self.send("c")

    def openClaw(self):
        self.send("oc")

    def deploy(self):
        self.send("deploy")

    def undeploy(self):
        self.send("undeploy")
