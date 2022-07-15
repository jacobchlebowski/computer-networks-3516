#Jacob Chlebowski (jachlebowski)
#Project 5
from audioop import avg
import socket
import random
import time
import argparse
import sys
import os

flag1=0
flag2=0
flag3=0

for i in range(len(sys.argv)):
    if sys.argv[i] == "--timeout":
       timeout= int(sys.argv[i+1])
       flag1=flag1+1
    if sys.argv[i] == "--port":
       PORT = int(sys.argv[i+1])
       flag2=flag2+1
    if sys.argv[i] == "--server":
       HOST = int(sys.argv[i+1])
       flag3=flag3+1

       #ELSE IF VARIABLES AREN'T CHANGED
    if flag1==0:
       timeout=3
    if flag2==0:
       PORT = 12000
    if flag3==0:
       HOST = '127.0.0.1'


pingMinimum = 0
pingMaximum = 0
pingAverage = 0
packetLossRate = 0

clientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
#SET TIMEOUT
clientSocket.settimeout(timeout)

#Message
#message_bytes = 256
#message = bytearray([1] * message_bytes)
message=""
#start time RTT
#time_start = time.time()

elapsed = []
timedoutLength = 0
for i in range(10):
 try:
     #SEND MESSAGE, start time, end time for that specific packet
     start = time.time()
     clientSocket.sendto(message.encode(), (HOST,PORT))
     modifiedMessage, serverAddress = clientSocket.recvfrom(4096)
     end = time.time()
     if(modifiedMessage.decode() == "Request timed out"):
        print("Ping %d: Request timed out" % (i+1))
        timedoutLength = timedoutLength + 1
     else:
        elapsed.append(end-start)
        print("Ping %d: %dms" % (i+1,elapsed[i-timedoutLength]*1000))
   
 except socket.timeout as e:
    print("Ping %d: Packet lost in transmission" % (i+1))
    timedoutLength = timedoutLength + 1


if (timedoutLength == 10):
   print("RTT: minimum: N/A; maximum: N/A; average: N/A\n")
   print("Packet loss rate: 100%")
else:
   updated_elapsed = [element * 1000 for element in elapsed]
   average = sum(updated_elapsed)/len(updated_elapsed)
   min = min(updated_elapsed)
   max = max(updated_elapsed)

   print("RTT: minimum: %dms; maximum: %dms; average: %dms\n" % (min,max,average))
   timedoutLength = timedoutLength*10
   print("Packet loss rate: %d%%" % timedoutLength)

#close?
clientSocket.close()


