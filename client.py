from socket import *
import os 
import GUI

class fileClient:
    
    def __init__(self):
        self._port = 821 
        self.segmentLength = 1024

        self.mainSocket = socket(AF_INET,SOCK_STREAM)
        print("Socket Connected")

        self.mainSocket.bind = (("", self._port))#bind isn't set
        print("Socket Bound")

        self.mainSocket.connect(("192.168.0.100", self._port))
        print("Connection Succesful")

        self.interface = GUI(self)#mainWindow
        

     
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


    def decodeFile(self, segmentList):
        
        #first entry in segmentList is the filename, returns and removes it from the list, decodes
        #it, and splits on : to remove the header label
        fileName = segmentList.pop(0).decode().split(':')[1]
        
        file = open(fileName, 'w')
        
        for segment in segmentList:
            file.write(segment.decode())
            
        file = open(fileName, 'r')
            
        return file


    # request the list of files available on the serve and prints them
    def listFile(self):
        self.mainSocket("list\n".encode())
        data = self.mainSocket(1024).decode()
        print("\n Files available on server:")
        return(data)


    def uploadFile(self, filePath):
        file = open(filePath, 'r')#maybe move to try/catch block?
        
        #gets filename from file path and adds header flag
        fileName = 'fn:' + filePath.split('/')[-1]
        
        headerList = [fileName.encode()]
        
        segmentList = headerList + self.encodeFile(file)
        #send each item of segmentList

        for item in segmentList:
            self.mainSocket.sendall(item)
        return(filePath + " Upload Confirmed")


    def downloadFile(self, fileName):
        self.mainSocket.sendall('dwn\n' + fileName)
        
        data = self.mainSocket.recv(1024).decode
        if (data == "Error 404: File not found"):
            print("file not found on server")
        else:
            with open(f"Downloaded_{fileName}", "w") as download:
                while True:
                    fileSize = self.mainSocket.recv(self.segmentLength)
                    if not fileSize:
                        break
                    download.write(fileSize.decode())
        
        
   
    def deleteFile(self,fileName):
        request = f"del\n{fileName}"
        self.mainSocket.sendall(request.encode())
        response = self.mainSocket.recv(1024).decode() 
        return  response