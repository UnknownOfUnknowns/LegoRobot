from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('192.168.0.239', serverPort))
serverSocket.listen(1)
print('The server is ready to receive')
while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024)
    capitalizedSentence = ""

    s = sentence.decode()
    if s == "bdf":
        print("Ready to adhere to your orders")
        capitalizedSentence = input()
    connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()
