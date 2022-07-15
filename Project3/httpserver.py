
#TCP-server.py
#Jacob Chlebowski 3/31/22 I
import socket
import os
import argparse
import sys
import time
import threading
running_threads = []
lock = threading.Lock()
timeout=0


def main():
  try: 
    while True:
       connectionSocket, addr = serverSocket.accept()
       hostname = socket.gethostname()
       ip_address = socket.gethostbyname(hostname)
       print("Information: received new connection from <%s>, port <%s>\n" % (ip_address,serverPort))
       connectionSocket.settimeout(timeout)
     
      
       try:
          input = connectionSocket.recv(8192).decode()
       except socket.timeout:
          print("Error: socket recv timed out")
          connectionSocket.close()
          break
       except UnicodeDecodeError:
          print("Error: invalid input character")
          connectionSocket.close()
          break



      
       #check HTTP1.0 or HTTP1.1 for OK return (more splitting)
       http1 = "HTTP/1.0"
       http2 = "HTTP/1.1"
       if (http1 in input):
          OK = response10
          connectionSocket.send(OK.encode())
       elif (http2 in input):
          OK = response11
          connectionSocket.send(OK.encode())
       else:
          connectionSocket.send(errmsg.encode())
          print("Error: invalid request line")
          connectionSocket.close()
          break

       #heres what's being input and read:
       #   print("INPUT: \n")
       #   print(input)
   
   
       #check for X-additional wait
       substring1 = "X-additional-wait: "
       if(substring1 in input):
          list1 = input.split('X-additional-wait: ',1)
          wait = list1[1]
          try:
             list2 = wait.split(' ',1)
             #SLEEP/WAIT
             wait = list2[0]
             time.sleep(int (wait))
          except:
             print("Error: invalid headers")
             connectionSocket.close()
             break
       

      

        #parse to get correct file name before searching that file
       stringGET = "GET"
       if not (stringGET in input):
        print("Error: invalid request line")
        connectionSocket.close()
        break

       if(stringGET in input):
          firstList = input.split('GET ',1)
          fileName = firstList[1]
          secondList = fileName.split(' HTTP',1)
          fileName = secondList[0]
          fileName = fileName.replace("/","\\")
    

          #final directory to file
          fileDir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + fileName

    
  
          #IF invalid Path OR IF "../" is in path OR file doesn't exist at path
          substring2 = "..\\"
          #or (substring2 in fileDir) or (not os.path.isfile(fileDir)
          if (substring2 in fileDir):
             connectionSocket.send(errmsg.encode()) #404 NOT FOUND
          elif (not os.path.exists(fileDir)):
             connectionSocket.send(errmsg.encode()) #404 NOT FOUND
             print("Error: invalid path")


          #Valid path and file exists, now send it back to client


          #return HTTP file request
          lock.acquire()
          with open (fileDir, 'rb') as f:
             connectionSocket.sendfile(f,0)
          lock.release()

          #remove backslash and print success served file
          test1 = fileName.split('\\',1)
          fileName = test1[1]
          print("Success: served file <%s>\n" % (fileName))
          connectionSocket.close()
          print('\nserver closed \n')
  except:
     print("Error: unexpected end of input")
     connectionSocket.close()
     print('\nserver closed \n')







#import THREADING MODULE for MULTIPLE SOCKETS
#MAY USE argparse MODULE TO PERFORM command-line OPTION PARSING
#YOU MAY USE FUNCTIONALITY PROVIDED BY THE time,sys,os MODULES
errmsg = 'HTTP/1.1 404 NOT FOUND\r\n\r\n'
response10 = 'HTTP/1.0 200 OK\r\n\r\n'
response11 = 'HTTP/1.1 200 OK\r\n\r\n'
errmsg = 'HTTP/1.1 404 NOT FOUND\r\n\r\n'

flag1=0
flag2=0
flag3=0

for i in range(len(sys.argv)):
    if sys.argv[i] == "--port":
       serverPort= int(sys.argv[i+1])
       flag1=flag1+1
    if sys.argv[i] == "--maxrq":
       NUM_THREADS = int(sys.argv[i+1])
       flag2=flag2+1
    if sys.argv[i] == "--timeout":
       timeout = int(sys.argv[i+1])
       flag3=flag3+1


       #ELSE IF VARIABLES AREN'T CHANGED
    if flag1==0:
       serverPort=8080
    if flag2==0:
       NUM_THREADS = 10
    if flag3==0:
       timeout = 10

         

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('127.0.0.1',serverPort))
serverSocket.listen(NUM_THREADS)
print('The server is ready to receive \n')

#create number of threads (each request)
for i in range(NUM_THREADS):
   t = threading.Thread(target=main, name=i)
   t.start()
   running_threads.append(t)

for t in running_threads:
   t.join()


