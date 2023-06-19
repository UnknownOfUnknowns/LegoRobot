from socket import *

serverName = '192.168.0.211'
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
sentence = "bdf"

clientSocket.send(sentence.encode())
while True:
    try:
        modifiedSentence = clientSocket.recv(1024)

        print(modifiedSentence)
        clientSocket.send(sentence.encode())
    except ConnectionError:
        print("error detected")
        try:
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect((serverName, serverPort))
            clientSocket.send(sentence.encode())
        except:
            pass
