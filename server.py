from socket import *
import threading
import time
import os
import queue

class FileServer:

    def __init__(self):
        self._port = 821

        self.mainSocket = socket(AF_INET, SOCK_STREAM)
        print("Socket Connected")
        # Binds socket to port 
        self.mainSocket.bind(('', self._port))
        print("Socket Bound")

        #set connection buffer size to 5
        self.mainSocket.listen(5)
        
        self._threads = []
        
        self.segmentLength = 1024
        
        self.downloadQueue = queue.Queue()


    #creates a thread for each client
    def connect(self): 
        connSocket, clientAddress = socket.accept()
        print("Connected to:", clientAddress)
        
        self.createUserThread(connSocket)


    #receives messages from client for debugging and handshakes
    def receive(self, connSocket): 
        data = connSocket.recv(1024).decode()
        return data
    
    
    #sends message to client, only sends encrypted strings
    def send(self, connSocket, message, print = True):
        
        connSocket.send(message.encode())
        
        if print: 
            print("Message sent:" + message)


    def sendFile(self, filePath, connSocket): #only works for text files
        file = open(filePath, "r")
        segmentList = self.encodeFile(file)
        for item in segmentList:
            self.send(connSocket, item)
        connSocket.sendall("File done sending".encode())


    #takes a file object, transforms the file into a list of maximum length 1024 byte data segments, encoded to be sent over a socket
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
  
         
    #should this be made part of user thread?
    def downloadThread(self, connSocket):
        while True:
            data = connSocket.recv(1024).decode()
            self.downloadQueue.put(data)

    #should we include another thing at the start of the segments with the filename? like a custom header
    #takes a list of encoded data segments from an incoming file transmission, returns a file object
    def decodeFile(self, segmentList):
        
        fileName = 'temp.txt'
        
        file = open(fileName, 'w')
        
        for segment in segmentList:
            file.write(segment.decode())
            
        file = open(fileName, 'r')
            
        return file
            
    #would it be better to return the thread?
    #creates a thread, calls userThread, adds the thread the self._threads list
    def createUserThread(self, connSocket):
        thread = threading.Thread(target = self.userThread, args=(connSocket, len(self._threads)))
        thread.start()
        self._threads.append(thread)
        
    
    #
    def userThread(self, conn, index):
        timeStart = time.time()
        while True:
            if time.time > timeStart + 300:
                conn.close()
                self._threads.pop(index)
                return
            self.receive(conn)
            tiStart = time.time()
   
            

main = FileServer()

print(main.readEncodeFile('test.txt'))