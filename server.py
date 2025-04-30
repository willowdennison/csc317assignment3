from socket import *
import threading
import time
import os
import queue

class FileServer:

    def __init__(self):
        self._port = 821

        self.mainSocket = socket(AF_INET, SOCK_STREAM)
        print('Socket Connected')
        # Binds socket to port 
        self.mainSocket.bind(('', self._port))
        print('Socket Bound')

        #set connection buffer size to 5
        self.mainSocket.listen(5)
        
        self.segmentLength = 1024
        
        self.downloadQueue = queue.Queue()


    #creates a thread for each client
    def connect(self): 
        connSocket, clientAddress = socket.accept()
        print('Connected to:', clientAddress)
        
        self.createUserThread(connSocket)


    #receives messages from client for debugging and handshakes
    def receive(self, connSocket): 
        data = connSocket.recv(1024).decode()
        return data
    
    
    #sends message to client, only sends encrypted strings
    def send(self, connSocket, message, print = True):
        
        connSocket.send(message.encode())
        
        if print: 
            print('Message sent:' + message)


    def sendFile(self, filePath, connSocket, print = True): #only works for text files
        file = open(filePath, 'r')
        
        #gets the filename from path and prepares header to be sent first
        fileName = 'fn:' + filePath.split('/')[-1]
        headerList = [fileName]
        
        segmentList = headerList + self.encodeFile(file)
        
        for item in segmentList:
            self.send(connSocket, item, print)
            
        if print: 
            connSocket.sendall('File done sending'.encode())


    #takes a file object, transforms the file into a list of maximum length 1024 byte data segments, encoded to be sent over a socket
    def encodeFile(self, file):

        file.seek(0, os.SEEK_END)
        fileLength = file.tell()
        
        file.seek(0)
        
        nSegments = int(fileLength / self.segmentLength) + (fileLength % self.segmentLength > 0)
        
        segments = []
        currentSegment = 0
        
        #<= means that the last segment will always be an empty string, showing that the file has been fully sent
        while currentSegment <= nSegments:
            
            segments.append(file.read(self.segmentLength).encode())
            currentSegment += 1
            
        return segments
    
    
    #should we include another thing at the start of the segments with the filename? like a custom header
    #takes a list of encoded data segments from an incoming file transmission, returns a file object
    def decodeFile(self, segmentList):
        
        #first entry in segmentList is the filename, returns and removes it from the list, decodes
        #it, and splits on : to remove the header label
        fileName = segmentList.pop(0).decode().split(':')[1]
        
        file = open(fileName, 'w')
        
        for segment in segmentList:
            file.write(segment.decode())
            
        file = open(fileName, 'r')
            
        return file
         

    #take a client request and an active connection, call the appropriate functions, and send the server response
    def processRequest(self, request, conn):
        pass

    
    #this is just going to put a bunch of random strings in a queue, this does not work at all 
    #should this be made part of user thread?
    def downloadThread(self, connSocket):
        while True:
            data = connSocket.recv(1024).decode()
            self.downloadQueue.put(data)

            
    #would it be better to return the thread and get rid of the threads list entirely?
    #creates a thread, calls userThread, adds the thread the self._threads list
    def createUserThread(self, connSocket):
        thread = threading.Thread(target = self.userThread, args = (connSocket,))
        thread.start()
        
    
    #
    def userThread(self, conn):
        
        timeStart = time.time()
        
        while True:
            
            if time.time > timeStart + 300:
                conn.close()
                return
            
            data = self.receive(conn)
            
            segmentList = []
            
            #if sending a filename, signifying that a file transmission is starting
            if data.split(':')[0] == 'fn':
                segmentList.append(data)
                
                transmissionFinished = False
                
                while not transmissionFinished: 
                    data = self.receive(conn)
                    
                    #if this is the end of the file
                    if data == '':
                        transmissionFinished = True
                        self.decodeFile(segmentList)
                        break
                    
                    segmentList.append(data)
                
            else:
                self.processRequest(data, conn)
            
            timeStart = time.time()
   
            

main = FileServer()

print(main.readEncodeFile('test.txt'))