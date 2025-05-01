from tkinter import *
from tkinter import ttk
from client import FileClient#debug? not sure if needed in final version


class MainWindow:

    def __init__(self, fileClient:FileClient):
        
        self.fileClient = fileClient
        self.maxQueueLength=5

        root=Tk()

        root.geometry('700x500') 
        root.title('File Sharing Client')
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        #sets default window size to 700w x 500h, with a name

        self.msgQueue=[]
        self.getFileName = StringVar()
        self.pushFileName = StringVar()
        self.deleteFileName = StringVar()
        #creating stringVar variables so they can be changed in GUI and then accessed in button methods

        self.commandFrame = ttk.Frame(root, padding='3 3 12 12')
        self.commandFrame.grid(column=0, row=0, sticky=(N))
        #creating the frame elements get added to

        ttk.Button(self.commandFrame, text='List All Files', command=self.listFiles).grid(column=0,columnspan=2, row=0, sticky=W)

        ttk.Button(self.commandFrame, text='Get', command=self.getFile).grid(column=0, row=1, sticky=W)
        ttk.Label(self.commandFrame, text='Get File From').grid(column=1, row=1, sticky=(W, E))
        getFileEntry = ttk.Entry(self.commandFrame, width=30, textvariable=self.getFileName)
        getFileEntry.grid(column=2, row=1, sticky=(W, E))

        ttk.Button(self.commandFrame, text='Push', command=self.pushFile).grid(column=0, row=2, sticky=W)
        ttk.Label(self.commandFrame,  text='Get File From').grid(column=1, row=2, sticky=(W, E))
        getFileEntry = ttk.Entry(self.commandFrame, width=30, textvariable=self.pushFileName)
        getFileEntry.grid(column=2, row=2, sticky=(W, E))

        ttk.Button(self.commandFrame, text='Delete', command=self.deleteFile).grid(column=0, row=3, sticky=W)
        ttk.Label(self.commandFrame,  text='Delete File At').grid(column=1, row=3, sticky=(W, E))
        getFileEntry = ttk.Entry(self.commandFrame, width=30, textvariable=self.deleteFileName)
        getFileEntry.grid(column=2, row=3, sticky=(W, E))
        #creating all onscreen elements

        self.consoleLabel=ttk.Label(self.commandFrame, text='console square', font=('Consolas',10))
        self.consoleLabel.grid(column=3, columnspan=2, row=0, rowspan=6, sticky=(S))

        root.mainloop()
        #internal loop so tk can hear inputs

    #calls client function to list all files in server's directory
    def listFiles(self):
        conf=self.fileClient.listFile()
        self.consoleLog(conf)


    #calls client function to get file from the specific path in server's directory
    def getFile(self):
        path=self.getFileName.get()
        if path is not "":
            conf=self.fileClient.downloadFile(path)
            self.consoleLog(conf)
        else:
            self.consoleLog("No file specified to download")


    #calls client function to push file from the specific path in client's directory
    def pushFile(self):
        path=self.pushFileName.get()
        if path is not "":
            conf=self.fileClient.uploadFile(path)
            self.consoleLog(conf)
        else:
            self.consoleLog("No file specified to upload")


    #calls client function to delete file from the specific path in server's directory
    def deleteFile(self):
        path=self.deleteFileName.get()
        if path is not "":
            conf=self.fileClient.deleteFile(path)
            self.consoleLog(conf)
        else:
            self.consoleLog("No file specified to delete")


    #displays messages to the GUI, basically a convenient print()
    #max length at 5 so console doesn't extend infinitely into window
    def consoleLog(self,newMsg):
        print(newMsg)
        self.msgQueue.append(newMsg)
        if len(self.msgQueue) > self.maxQueueLength :
            self.msgQueue.pop(0)
        txt = ''
        for msg in self.msgQueue:
            txt =  txt + '\n' + msg
        self.consoleLabel.config(text = txt)

