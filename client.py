from socket import *
import os 

class ClientServer:
    
    def __init__(self):
        self._port = 821 

        self.mainSocket = socket(AF_INET,SOCK_STREAM)
        print("Socket Connected")

        self.mainSocket.bind = (("", self._port))
        print("Socket Bound")


        
    def encodeFile(self, file):

        file.seek(0, os.SEEK_END)
        fileLength = file.tell()
        
        file.seek(0)
        
        nSegments = int(fileLength / self.segmentLength) + (fileLength % self.segmentLength > 0)
        
        segments = []
        currentSegment = 0
        
        while currentSegment <= nSegments:
            
            segments.append(file.read(self.segmentLength).encode())
            currentSegment += 1
            
        return segments

    # request the list of files available on the serve and prints them
    def listFile(self):
        self.mainSocket("list \n".encode())
        data = self.mainSocket(1024).decode()
        print("\n Files available on server:")
        print(data)


    def uploadFile(self):
        filePath = input("Enter File Path: ")
        file = open(filePath, 'r')
        segmentList = self.encodeFile(file)
        #send each item of segmentList




    def downloadFile(self):
        fileName = input("File to Download: ")
        self.mainSocket.sendall('dwn\n\n' + fileName)
        
        data = self.mainSocket.recv(1024).decode 

        if data == "Error: File not found":
            print("file not found on server")
        else:
            with open("Downloaded_"):
                pass
        


   
    def deleteFile(self):
        file = input("Delete a File: ")
        self.mainSocket.sendall('del\n' + file)
            
