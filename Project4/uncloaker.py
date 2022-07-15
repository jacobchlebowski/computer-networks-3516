#Project 4 - Jacob Chlebowski (jachlebowski)
#4/14/22

import sys
import time
import os
import multiprocessing
import argparse
from scapy.all import *

lock = multiprocessing.Lock()
queue = multiprocessing.Queue()


def processFile(fName,verbosity,flag5,folderName):
  #print("\nhere--------------")
  #NOT PCAP File
  try:
     packets = rdpcap(fName)
  except:
      if(verbosity==2 or verbosity==3):
          print("NOT VALID PCAP FILE")
          return


    
  #IS a PCAP file
  flag4=0
  for packet in packets:
     #TODO: complete
     summary = scapy.packet.Packet.summary(packet)  

     #VERBOSITY=1
     if(verbosity==1):
         if("DNS" in summary):
             if ("CNAME" in scapy.packet.Packet.sprintf(packet, "Type: {DNS:dest=%DNS.an%}")):
                 #correctly sets to 1
                 flag5 = 1
                 return flag5
 
     #VERBOSITY=2
     if(verbosity==2):
         if ("DNS" in summary):
              if ("CNAME" in scapy.packet.Packet.sprintf(packet, "Type: {DNS:dest=%DNS.an%}")) and (flag4==0):
                 print("CNAME cloaking detected")
                 flag4 = 1


     #VERBOSITY=3
     if(verbosity==3):
         if("DNS" in summary):
             if("CNAME" in scapy.packet.Packet.sprintf(packet, "Type: {DNS:dest=%DNS.an%}")):
                 if(flag4==0):
                     print("CNAME cloaking detected\n")
                     flag4 = 1
                 #PRINT LIST OF ALL SUSPICIOUS DOMAIN MAPPINGS
                 beforeCNAME = packet.an[0].rrname.decode("utf-8")
                 afterCNAME = packet.an[0].rdata.decode("utf-8")
                 print("%s: CNAME cloaking detected: (%s -> %s)" % (folderName,beforeCNAME,afterCNAME))


     pass

  if(flag4==0) and (verbosity==2):
     print("CNAME cloaking not detected")
  if(flag4==0) and (verbosity==3):
     print("CNAME cloaking not detected")


     return


def preProcess(folderName,fileDir,verbosity):
 #with folder name & DIRECTORY?, process EACH file in folder?
 flag5=0
 f = os.path.join(fileDir, folderName)
 #NOW what do you want to do w/ file?
 lock.acquire()
 print("File: <%s>" % folderName)
 flag5 = processFile(f,verbosity,flag5,folderName)
 if (verbosity==3 or verbosity==2):
     lock.release()
     return
 if(flag5==1):
     queue.put(1)
     lock.release()
     return
 elif(flag5==0):
     queue.put(0)
     lock.release()

 pass
 return





def main():
 #TODO: complete

 #COMMAND LINE OPTIONS
 #--verbosity
 #--processes
 #--folder (get file name and run processFile function)
 flag1=0
 flag2=0
 flag3=0

 for i in range(len(sys.argv)):
     if sys.argv[i] == "--verbosity":
         verbosity= float(sys.argv[i+1])
         #VALID PARAMETER?
         if not((verbosity==1)or(verbosity==2)or(verbosity==3)):
             print("INVALID PARAMETER FOR VERBOSITY. MUST BE '1' '2' or '3'....\n")
             return
         flag1=flag1+1  
     if sys.argv[i] == "--processes":
         #VALID PARAMETER?
         try:
             processes = int(sys.argv[i+1])
         except:
             print("INVALID PARAMETER FOR PROCESSES. MUST BE ANY INTEGER > 0....\n")
         flag2=flag2+1
     if sys.argv[i] == "--folder":
         folderName = sys.argv[i+1]
         #get directory
         fileDir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "/" + folderName
         #VALID PARAMETER?
         if not(os.path.exists(fileDir)):
             print("MUST BE VALID PATH and/or FILENAME....\n")
             return

         flag3=flag3+1

        #ELSE IF VARIABLES AREN'T CHANGED
     if flag1==0:
         verbosity = 2
     if flag2==0:
         processes = 2
     if flag3==0:
         folderName = "./" 
         #get directory (current in this case)
         fileDir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


 print("Number of Processes: %d" % processes)
 #LIST OF PCAP FILES
 pcaps = []
 for k in os.listdir(fileDir):
     pcaps.append(k)

 
 #Multiprocesses
 count = 0
 for y in range(len(pcaps)):
     for i in range(processes):
         if (count >= len(pcaps)):
             return
         folderName = pcaps[count]
         p = multiprocessing.Process(target=preProcess, args=(folderName,fileDir,verbosity), name = "process%d: " % i)
         if(verbosity==1 and queue.empty()==1):
             try:
                 packets = rdpcap(os.path.join(fileDir, folderName))
             except:
                 print("\nNOT PCAP FILE")
                 return
             print("CNAME cloaking detected")
             return
         if(verbosity==1 and queue.empty()==0):
             print("CNAME cloaking not detected")
             return

         p.start()
         count = count+1
     p.join()


 pass




if __name__ == '__main__':
    main()

