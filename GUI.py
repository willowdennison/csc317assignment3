from tkinter import *
from tkinter import ttk
from client import FileClient#debug? not sure if needed in final version


class MainWindow:

    def __init__(self, fileClient):
        
        self.fileClient = fileClient

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

        self.commandFrame = ttk.Frame(root, padding='3 3 12 12')
        self.commandFrame.grid(column=0, row=0, sticky=(N))

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

        self.consoleLabel=ttk.Label(self.commandFrame, text='console square', font=('Consolas',10))
        self.consoleLabel.grid(column=3, columnspan=2, row=0, rowspan=4, sticky=(S))

        root.mainloop()

    
    def listFiles(self):
        conf=self.fileClient.listFile()
        print(conf)
        self.consoleLog(conf)


    def getFile(self):
        conf=self.fileClient.downloadFile(self.getFileName.get())
        print(conf)
        self.consoleLog(conf)


    def pushFile(self):
        conf=self.fileClient.uploadFile(self.pushFileName.get())
        print(conf)
        self.consoleLog(conf)


    def deleteFile(self):
        conf=self.fileClient.deleteFile(self.deleteFileName.get())
        print(conf)
        self.consoleLog(conf)


    def consoleLog(self,newMsg):
        self.msgQueue.append(newMsg)
        if(len(self.msgQueue)>5):
            self.msgQueue.pop(0)
        txt=''
        for msg in self.msgQueue:
            txt=  txt + '\n' + msg
        self.consoleLabel.config(text=txt)

