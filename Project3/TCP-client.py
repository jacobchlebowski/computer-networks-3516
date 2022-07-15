#TCP-client.py
#Jacob Chlebowski 3/31/22

from socket import *
HOST = "127.0.0.1"
PORT = 8080;
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((HOST,PORT))

#send HTTP requesrt to SEVER
input = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % HOST
clientSocket.send(input.encode() )

#receive data
response = clientSocket.recv(8192)

#display the response
print(response)

clientSocket.close()