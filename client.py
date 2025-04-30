from socket import *
import os 

class fileClient:
    
    def __init__(self):
        self._port = 821 
        self.segmentLength = 1024

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
        
        while currentSegment < nSegments:
            
            segments.append(file.read(self.segmentLength).encode())
            currentSegment += 1
            
        return segments


    # request the list of files available on the serve and prints them
    def listFile(self):
        self.mainSocket("list\n".encode())
        data = self.mainSocket(1024).decode()
        print("\n Files available on server:")
        print(data)


    def uploadFile(self):
        filePath = input('Enter path to the file to be uploaded: ')
        file = open(filePath, 'r')
        
        #gets filename from file path and adds header flag
        fileName = 'fn:' + filePath.split('/')[-1]
        
        headerList = [fileName.encode()]
        
        segmentList = headerList + self.encodeFile(file)
        #send each item of segmentList


    def downloadFile(self):
        fileName = input("File to Download: ")
        self.mainSocket.sendall('dwn\n' + fileName)
        
        data = self.mainSocket.recv(1024).decode
        if (data == "Error 404: File not found"):
            print("file not found on server")
        else:
            pass
        
   
    def deleteFile(self):
        file = input("Delete a File: ")
        self.mainSocket.sendall('del\n' + file)
        #add confirmation
            
