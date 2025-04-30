from socket import *
import threading
import time
import os

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
        
        connectThread = threading.Thread(target = self.connect)
        connectThread.start()


    #creates a thread for each client
    def connect(self): 
        
        while True:
            
            connSocket, clientAddress = self.mainSocket.accept()
            print('Connected to:', clientAddress)
            
            self.createUserThread(connSocket)


    #receives messages from client for debugging and handshakes
    def receive(self, connSocket): 
        data = connSocket.recv(1024).decode()
        return data
    

    #open file with checking for nonexistent files
    def openFile(self, path, permissions):
        if os.path.exists(path):
            return open(path, permissions)
        else: 
            raise(FileNotFoundError)


    #sends a file, filePath, to the client, sends a large amount of segments, client combines it into a txt file
    def sendFile(self, filePath, connSocket, doPrint = True): #only works for text files (currently)
        
        filePath = 'files/' + filePath
        
        try:
            file = self.openFile(filePath, 'r')
        
        except FileNotFoundError:
            connSocket.sendall('Error 404: File not found'.encode())
            return
        
        #gets the filename from path and prepares header to be sent first
        fileName = ('fn:' + filePath.split('/')[-1]).encode()
        headerList = [fileName]
        
        segmentList = headerList + self.encodeFile(file)
        
        for item in segmentList:
            connSocket.sendall(item)
            
            if doPrint:
                print(item)
            
            
        if doPrint:
            print(filePath + ' finished sending')

    
    #deletes the file with path fileName
    def delete(self, fileName):
        if os.path.exists(fileName):
            os.remove(fileName)
        else:
            print("File does not Exist") #Will be changed 


    #lists all files in the files/ directory and formats them for display
    def listDir(self):
        dir = os.listdir('files')
        
        formattedDir = ''
        
        for f in dir:
            formattedDir = formattedDir + f + '\n'
        
        return formattedDir


    #takes connection object, recieves, and saves file to directory
    def recieveFile(self, conn):
        
        segmentList = []
        
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
            
        conn.sendall('File recieved')

    #takes a file object, transforms the file into a list of maximum length 1024 byte data segments, encoded to be sent over a socket
    #does not add header with filename
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
            
        segments[-1] = 'end'.encode()
        
        return segments
    
    
    #should we include another thing at the start of the segments with the filename? like a custom header
    #takes a list of encoded data segments from an incoming file transmission, returns a file object
    def decodeFile(self, segmentList):
        
        #first entry in segmentList is the filename, returns and removes it from the list, decodes
        #it, and splits on : to remove the header label
        fileName = 'files/' + segmentList.pop(0).decode().split(':')[1]
        
        file = self.openFile(fileName, 'w')
        
        for segment in segmentList:
            file.write(segment.decode())
            
        file = self.openFile(fileName, 'r')
            
        return file
         

    #take a client request and an active connection, call the appropriate functions, and send the server response
    #handles download, delete, and list requests
    def processRequest(self, request, connSocket):
        
        request = request.split(sep = '\n')
        requestType = request[0].strip()
        
        match requestType:
            
            case 'dwn':
                fileName = request[1].strip()
                print("Downloading " + fileName)
                self.sendFile(fileName, connSocket)
                connSocket.sendall((fileName + ' Downloaded').encode())
                
            case 'del':
                fileName = request[1].strip()
                print("Deleting "+ fileName)
                self.delete(fileName) 
                connSocket.sendall((fileName + ' Deleted').encode())
                
            case 'list':
                print("listing")
                dir = self.listDir()
                print(dir)
                connSocket.sendall(dir.encode())
                connSocket.sendall('List Recieved'.encode())
                
            case _:
                connSocket.sendall('Invalid command'.encode())

            
    #would it be better to return the thread and get rid of the threads list entirely?
    #creates a thread, calls userThread, adds the thread the self._threads list
    def createUserThread(self, connSocket):
        thread = threading.Thread(target = self.userThread, args = (connSocket,))
        thread.start()
        
    
    #thread created for each connection to monitor requests, process them, and 
    def userThread(self, conn):
        
        timeStart = time.time()
        
        while True:
            
            if time.time() > timeStart + 300:
                conn.close()
                return
            
            data = self.receive(conn)
            
            #if sending a filename, signifying that a file transmission is starting
            if data.split(':')[0] == 'fn':
                self.recieveFile(conn)
                
            else:
                self.processRequest(data, conn)
            
            timeStart = time.time()

main = FileServer()