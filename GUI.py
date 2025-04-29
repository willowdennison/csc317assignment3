from tkinter import *
from tkinter import ttk


class mainWindow:
    def __init__(self):
        self.root = Tk()       
        self.root.geometry("700x500") #sets default size to 700pxw 500pxh
        self.root.title("File Sharing Client")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.getFileName = StringVar()
        
        commandFrame = ttk.Frame(self.root, padding="3 3 12 12")
        commandFrame.grid(column=0, row=0, sticky=(N, W, E, S))

        ttk.Button(commandFrame, text="List All Files", command=self.printList).grid(column=0,columnspan=2, row=0, sticky=W)
        

        ttk.Button(commandFrame, text="Get", command=self.printList).grid(column=0, row=1, sticky=W)
        ttk.Label(commandFrame, text="Get File From").grid(column=1, row=1, sticky=(W, E))
        getFileEntry = ttk.Entry(commandFrame, width=30, textvariable=self.getFileName)
        getFileEntry.grid(column=2, row=1, sticky=(W, E))

        ttk.Button(commandFrame, text="Push", command=self.printList).grid(column=0, row=2, sticky=W)
        ttk.Label(commandFrame,  text="Get File From").grid(column=1, row=2, sticky=(W, E))
        getFileEntry = ttk.Entry(commandFrame, width=30, textvariable=self.getFileName)
        getFileEntry.grid(column=2, row=2, sticky=(W, E))

        ttk.Button(commandFrame, text="Delete", command=self.printList).grid(column=0, row=3, sticky=W)
        ttk.Label(commandFrame,  text="Delete File At").grid(column=1, row=3, sticky=(W, E))
        getFileEntry = ttk.Entry(commandFrame, width=30, textvariable=self.getFileName)
        getFileEntry.grid(column=2, row=3, sticky=(W, E))

        self.consoleLabel=ttk.Label(commandFrame, text="console square", font=("Consolas",10)).grid(column=3, columnspan=2, row=0, rowspan=4)


        self.root.mainloop()
    
    def printList(self,*args):
            print("list here" + self.getFileName.get())

    def consoleLog(self,msg):
        self.consoleLabel.configure(text=msg)#this isnt updating console square
        self.consoleLabel.pack()

    def run(self):

        '''
        feet = StringVar()

        #makes a text input field
        feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
        feet_entry.grid(column=2, row=1, sticky=(W, E))

        meters = StringVar()
        ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))

        ttk.Button(mainframe, text="Calculate", command=mainWindow.calculate).grid(column=3, row=3, sticky=W)

        ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
        ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
        ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        feet_entry.focus()
        root.bind("<Return>", mainWindow.calculate)
        '''

if __name__ == "__main__":
    mw=mainWindow()