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
        print('Socket Connected')

        self.mainSocket.bind(('', self._port))
        print('Socket Bound')

        self.mainSocket.connect(('192.168.0.100', self._port))
        print('Connection Succesful')

        self.interface = GUI.MainWindow(self)
        

    #takes a file object, transforms the file into a list of maximum length 1024 byte data segments, encoded to be sent over a socket
    def encodeFile(self, file):
        
        file.seek(0, os.SEEK_END)
        fileLength = file.tell()
        
        file.seek(0)
        
        nSegments = int(fileLength / self.segmentLength) + (fileLength % self.segmentLength > 0)
        
        segments = []
        currentSegment = 0
        
        while currentSegment <= nSegments:
            
            segments.append(file.read(self.segmentLength))
            currentSegment += 1
            
        return segments
    #first entry in segmentList is the filename, returns and removes it from the list, decodes
    #it, and splits on : to remove the header label


    #decodes a segmentList from downloadFile() and saves it to fileName
    def decodeFile(self, segmentList, fileName):
        
        print(segmentList)
    
        filePath = os.getcwd()
        
        #check for file separator character and use the proper one
        if '\\' in filePath:
            char = '\\'
        else:
            char = '/'
        
        filePath = filePath + char + 'files' + char + fileName

        file = open(filePath, 'wb')
        
        for segment in segmentList:
            file.write(segment)
        
        file = open(filePath, 'rb')
        
        return file


    #requests the list of files available on the serve and prints them
    def listFile(self):
        
        self.mainSocket.send('list\n'.encode())
        
        data = self.mainSocket.recv(1024).decode()
       
        dirList = 'Files available on server: \n' + data

        return dirList


    #Sends file path and file contents, gets filename from file path and adds header flag
    def uploadFile(self, filePath):
        
        if os.path.exists(filePath): 
            file = open(filePath, 'rb')
            
        else:
            raise FileNotFoundError
        
        #check for file separator character and use the proper one
        if '/' in filePath:
            char = '/'
        else: 
            char = '\\'
        
        fileName = 'fn:' + filePath.split(char)[-1]
        
        self.mainSocket.send(fileName.encode())
        
        segmentList = self.encodeFile(file)
        
        time.sleep(0.01)

        for item in segmentList:
            self.mainSocket.send(item) 
            print(item)
    
        return filePath + ' uploaded'


    #Sends a request for server to send file contents, and then creates a duplicate file in client
    def downloadFile(self, fileName):
        
        self.mainSocket.send(f'dwn\n{fileName}'.encode())
        
        segmentList = []
        
        while True:
            
            segment = self.mainSocket.recv(1024)
            print(segment)
            
            segmentList.append(segment)
            
            print(segmentList)

            if len(segment.decode()) < 1024:
                self.decodeFile(segmentList, fileName) 
                return f'{fileName} downloaded'

        
    #sends a request to server to delete file (on server side), gets a response from the server
    def deleteFile(self,fileName):
        
        request = f'del\n{fileName}'
        
        self.mainSocket.send(request.encode())
       
        return (fileName + ' Deleted')



if __name__ == '__main__':
    fc = FileClient()