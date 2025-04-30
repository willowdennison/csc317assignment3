from tkinter import *
from tkinter import ttk


class mainWindow:

    def __init__(self, root):
        root.geometry("700x500") #sets default size to 700pxw 500pxh
        root.title("File Sharing Client")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.msgQueue=[]
        self.getFileName = StringVar()
        self.pushFileName = StringVar()
        self.deleteFileName = StringVar()

        self.commandFrame = ttk.Frame(root, padding="3 3 12 12")
        self.commandFrame.grid(column=0, row=0, sticky=(N, W, E, S))

        ttk.Button(self.commandFrame, text="List All Files", command=self.listFiles).grid(column=0,columnspan=2, row=0, sticky=W)

        ttk.Button(self.commandFrame, text="Get", command=self.getFile).grid(column=0, row=1, sticky=W)
        ttk.Label(self.commandFrame, text="Get File From").grid(column=1, row=1, sticky=(W, E))
        getFileEntry = ttk.Entry(self.commandFrame, width=30, textvariable=self.getFileName)
        getFileEntry.grid(column=2, row=1, sticky=(W, E))

        ttk.Button(self.commandFrame, text="Push", command=self.pushFile).grid(column=0, row=2, sticky=W)
        ttk.Label(self.commandFrame,  text="Get File From").grid(column=1, row=2, sticky=(W, E))
        getFileEntry = ttk.Entry(self.commandFrame, width=30, textvariable=self.pushFileName)
        getFileEntry.grid(column=2, row=2, sticky=(W, E))

        ttk.Button(self.commandFrame, text="Delete", command=self.deleteFile).grid(column=0, row=3, sticky=W)
        ttk.Label(self.commandFrame,  text="Delete File At").grid(column=1, row=3, sticky=(W, E))
        getFileEntry = ttk.Entry(self.commandFrame, width=30, textvariable=self.deleteFileName)
        getFileEntry.grid(column=2, row=3, sticky=(W, E))

        self.consoleLabel=ttk.Label(self.commandFrame, text="console square", font=("Consolas",10))
        self.consoleLabel.grid(column=3, columnspan=2, row=0, rowspan=4, sticky=(S))

    
    def listFiles(self):
        self.consoleLog("list here")
        print("list here")


    def getFile(self):
        self.consoleLog("got file from: " + self.getFileName.get())
        print("got file from: " + self.getFileName.get())


    def pushFile(self):
        self.consoleLog("pushed file from: " + self.pushFileName.get() + " to server")
        print("pushed file from: " + self.pushFileName.get() + " to server")


    def deleteFile(self):
        self.consoleLog("deleted file at: " + self.deleteFileName.get())
        print("deleted file at: " + self.deleteFileName.get())


    def consoleLog(self,newMsg):
        self.msgQueue.append(newMsg)
        if(len(self.msgQueue)>5):
            self.msgQueue.pop(0)
        txt=""
        for msg in self.msgQueue:
            txt=  txt + "\n" + msg
        self.consoleLabel.config(text=txt)


if __name__ == "__main__":
    root=Tk()
    main=mainWindow(root)
    root.mainloop()