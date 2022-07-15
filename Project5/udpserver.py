#Jacob Chlebowski (jachlebowski)
#Project 5
import socket
import random
import time
import argparse
import sys
import os
timeout=5

flag1=0
flag2=0
flag3=0
flag4=0

#LOSSPROB MUST BE BETWEEN 0 AND 1
#min/max DELAY IN MILISECONDS

for i in range(len(sys.argv)):
    if sys.argv[i] == "--lossprob":
     try:
         lossProb= float(sys.argv[i+1])
         if((lossProb >=0) and (lossProb <= 1)):
             flag1=flag1+1
         else:
             print("MUST BE VALID INTEGER BETWEEN 0 AND 1\n")
     except ValueError:
         print("MUST BE VALID INTEGER BETWEEN 0 AND 1\n")

    if sys.argv[i] == "--mindelay":
       minDelay = int(sys.argv[i+1])
       flag2=flag2+1
    if sys.argv[i] == "--maxdelay":
       maxDelay = int(sys.argv[i+1])
       flag3=flag3+1
    if sys.argv[i] == "--port":
        serverPort = int(sys.argv[i+1])
        flag4=flag4+1


       #ELSE IF VARIABLES AREN'T CHANGED
    if flag1==0:
       lossProb = 0
    if flag2==0:
       minDelay = 0
    if flag3==0:
       maxDelay = 0
    if flag4==0:
       serverPort=12000


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,0)
serverSocket.bind(('127.0.0.1',serverPort))
print("The server is ready to receive")
if (minDelay > maxDelay) or (maxDelay < minDelay):
   print("MIN DELAY MUST BE LESS THAN MAX DELAY")
   serverSocket.close()
   
try:
   while True:
     message,clientAddress = serverSocket.recvfrom(4096)
     serverSocket.settimeout(timeout)

     try:
        modifiedMessage = message.decode()
        #DELAYs
        delay = random.randint(minDelay,maxDelay)/1000 #convert?
        #Delay in miliseconds
        time.sleep(delay)

        #IF PROB=TRUE, PACKET IS DROPPED
        #Request timed out for packet
        if(random.random() < lossProb):
           modifiedMessage = "Request timed out"
           serverSocket.sendto(modifiedMessage.encode(), clientAddress)
        else:
          #send message back
          serverSocket.sendto(modifiedMessage.encode(), clientAddress)


     except socket.timeout:
          print("Error: socket recv timed out")
          serverSocket.close()
          break

   
except:
    print("Error: unexpected end of input")
    serverSocket.close()
    print('\nserver closed \n')





