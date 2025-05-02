from socket import *
import threading
import time
import os


class FileServer:


    def __init__(self):
        
        self._port = 821

        self.mainSocket = socket(AF_INET, SOCK_STREAM)
        print('Socket Connected')
        
        #use 127.0.0.1 in the first argument to connect with your own pc
        self.mainSocket.bind(('', self._port)) 
        print('Socket Bound')

        #set connection buffer size to 5
        self.mainSocket.listen(5)
        
        self.segmentLength = 1024
        
        connectThread = threading.Thread(target = self.connect)
        connectThread.start()


    #accepts connections and opens a thread for each user when they connect
    def connect(self): 
        
        while True:
            
            conn, clientAddress = self.mainSocket.accept()
            print('Connected to:', clientAddress)
            
            self.createUserThread(conn)


    #receives messages from client for requests and file uploads
    def receive(self, conn): 
        
        data = conn.recv(1024).decode()
        return data
    

    #open file, check if file exists or create file if permissions == 'wb'
    def openFile(self, fileName, permissions):
        
        path = os.getcwd() 
        
        #check for file separator character and use the proper one
        if '/' in path: 
            char = '/'
        else: 
            char = '\\'
            
        path = path + char + 'files' + char + fileName 

        if permissions == 'wb':
            return open(path, permissions)
        
        elif os.path.exists(path):
            return open(path, permissions)
        
        else: 
            raise(FileNotFoundError)


    #sends a file, fileName, to the client, in max length 1024 byte segments
    def sendFile(self, fileName, conn, doPrint = True):
        
        try:
            file = self.openFile(fileName, 'rb')
        
        except FileNotFoundError:
            conn.send('Error 404: File not found'.encode())
            return
        
        segmentList = self.encodeFile(file)
        
        for item in segmentList:
            conn.send(item)
            
            if doPrint:
                print(item)

    
    #deletes the file at fileName
    def delete(self, fileName):
        
        path = os.getcwd() 
        
        #check for file separator character and use the proper one
        if '/' in path: 
            char = '/'
        else: 
            char = '\\'
            
        fileName = path + char + 'files' + char + fileName
        
        if os.path.exists(fileName):
            os.remove(fileName)
            print(f'{fileName} deleted')
        else:
            print('File does not Exist') 


    #lists all files in the /files/ directory and formats them for display
    def listDir(self):
        
        dir = os.listdir('files')
        
        formattedDir = ''
        
        for f in dir:
            formattedDir = formattedDir + f + '\n'
        
        return formattedDir


    #takes connection object, recieves a file over socket conn, and saves file to directory
    def recieveFile(self, conn, fileName, doPrint = True):
        
        segmentList = []
            
        while True: 
            data = self.receive(conn)
            
            if print: 
                print(data)
                
            segmentList.append(data)   
                 
            #if this is the end of the file
            if len(data) < 1024:
                
                self.decodeFile(segmentList, fileName)
                
                if doPrint:
                    print(f'{fileName} received')

                return


    #takes a file object, transforms the file into a list of maximum length 1024 byte data segments, encoded to be sent over a socket
    #does not add header with filename,<= means that the last segment will always be an empty string, showing that the file has been fully sent
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
    
    
    
    #takes a list of encoded data segments from an incoming file transmission,stores the file at the filename in the first segment,  returns a file object, #first entry in segmentList is the filename, returns and removes it from the list, decodes
        #it, and splits on : to remove the header label
    def decodeFile(self, segmentList, fileName):
         
        file = self.openFile(fileName, 'wb')
        
        for segment in segmentList:
            file.write(segment)
            
        file = self.openFile(fileName, 'rb')
            
        return file
         

    #take a client request and an active connection, call the appropriate functions, and send the server response
    #handles download, delete, and list requests
    def processRequest(self, request, conn):
        
        request = request.split(sep = '\n')
        requestType = request[0].strip()
        
        match requestType:
            
            case 'dwn':
                fileName = request[1].strip()
                print('Downloading ' + fileName)
                self.sendFile(fileName, conn)
                
            case 'del':
                fileName = request[1].strip()
                print('Deleting '+ fileName)
                self.delete(fileName) 
                   
            case 'list':
                print('listing')
                dir = self.listDir()
                print(dir)
                conn.send(dir.encode())
                
            case _:
                conn.send('Invalid command'.encode())
                
                
    #creates a thread for the connection at conn using userThread()
    def createUserThread(self, conn):
        
        thread = threading.Thread(target = self.userThread, args = (conn,))
        thread.start()
        
    
    #thread created for each connection to monitor and handle client requests
    def userThread(self, conn):
        
        timeStart = time.time()
        
        while True:
            
            if time.time() > timeStart + 300:
                conn.close()
                return
            
            data = self.receive(conn)
            
            fileName = data.split(':')
            if fileName[0] == 'fn':
                self.recieveFile(conn, fileName[1])
                
            else:
                self.processRequest(data, conn)
            
            timeStart = time.time()



if __name__ == '__main__':
    main = FileServer()