from socket import *
import os 
import GUI
import time

class FileClient:
    
    #Constructor: Initializes connection and launches GUI
    def __init__(self):
        
        self._port = 821 
        self.segmentLength = 1024

        self.mainSocket = socket(AF_INET,SOCK_STREAM)
        print("Socket Connected")

        self.mainSocket.bind(("", self._port))
        print("Socket Bound")

        self.mainSocket.connect(("192.168.0.100", self._port))
        print("Connection Succesful")

        self.interface = GUI.mainWindow(self)
        

    #takes a file object, transforms the file into a list of maximum length 1024 byte data segments, encoded to be sent over a socket
    #does not add header with filename
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
        print(segmentList)
        
        #quick fix:
        try:
            fileName = segmentList.pop(0).decode().split(':')[1] #segment list is empty?? (Fix on thursday)
            self.mainSocket.sendall('File successfully sent')
            
        except IndexError:
            self.mainSocket.sendall('no segments to decode'.encode())
            return
        
        file = open(fileName, 'w')
        
        for segment in segmentList:
            file.write(segment.decode())
            
        file = open(fileName, 'r')
            
        return file


    # request the list of files available on the serve and prints them
    def listFile(self):
        
        self.mainSocket.sendall("list\n".encode())
        
        data = self.mainSocket.recv(1024).decode()
        
        dirList = "Files available on server: \n" + data
        
        return dirList


    # Sends file path and file contents
    def uploadFile(self, filePath):
        
        if os.path.exists(filePath): 
            file = open(filePath, 'r')
            
        else:
            raise FileNotFoundError
        
        #gets filename from file path and adds header flag
        fileName = 'fn:' + filePath.split('/')[-1] + ':'
        
        headerList = [fileName.encode()]
        
        segmentList = headerList + self.encodeFile(file)

        for item in segmentList:
            self.mainSocket.sendall(item)
        
        #ensures that packets don't get combined by tcp
        time.sleep(0.1)
        self.mainSocket.sendall('file sent'.encode())
        
        response = self.mainSocket.recv(1024).decode()
        
        return response


    #Sends a request for server to send file contents, and then creates a duplicate file in client
    def downloadFile(self, fileName):
        
        print("before send")
        self.mainSocket.sendall(f'dwn\n{fileName}'.encode())
        print("after send")
        
        segmentList = []
        
        receiving = True
        
        while receiving:
            segment = self.mainSocket.recv(1024)
            
            if  fileName + " Downloaded" in segment.decode():
                receiving = False 
            
            segmentList.append(segment)

            if segmentList[0].decode().startswith("Error 404"):
                return "Error 404: File not found"
            
        self.decodeFile(segmentList) 
        return f"{fileName} Downloaded says client"

        
    #sends a request to server to delete file (on server side), gets a response from the server
    def deleteFile(self,fileName):
        request = f"del\n{fileName}"
        self.mainSocket.sendall(request.encode())
       
        response = self.mainSocket.recv(1024).decode() 
        return response

if __name__ == "__main__":
    fc = FileClient()
