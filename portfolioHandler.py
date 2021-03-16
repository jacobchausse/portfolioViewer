# Get stock symbol name
# Get stock quantity
# Get stock purchase price
# Determine if either Portfolio or watchlist
import tkinter as tk
import os.path


class portfolio():
    def __init__(self, name,dataObject, fileDescript='All files', fileExt='.xlsx',
                 cmd=None, monthVar = 0, closeConditionVar = 0):
        self.tickerList = [] # List stock objects
        self.name = name
        self.filePath = '' #default file path
        
    def newStock(self):
        #check if stock is in tickerlist already if it
        #is call stock.updateStock else create new stock object and to its list
        #updates portfolio file (use savePortfolio)
        pass

    def loadPortfolio(self, directory):
        tk.Frame.__init__(self, parent)
        self.file     = tk.StringVar()
        self.fileName = tk.StringVar()
        self.fileName.set('Default File Path')
        self.file.set(filePath)
        self.fileDescript = fileDescript
        self.fileExt      = fileExt
        self.cmd          = cmd
        self.monthVar     = tk.IntVar()
        self.monthVar.set(2)
        self.closeConditionVar = tk.IntVar()
        self.closeConditionVar.set(0)
        self.parent = parent

        self.data = stock() #initializes stock object

        tk.Button(self, text='Change File', command=self.load).grid(row=5, column=2, padx=5, pady=3)

        tk.Label(self, textvariable=self.fileName).grid(row=5, column=1, ipadx=0, pady=10)
        #populate portfolio list with stock objects from file

        self.okayButton = tk.Button(self, text="START",
                                    command=lambda: self.parent.stepOne())

        self.okayButton.grid(row=6, column=1, padx=5, pady=3,sticky='w'+'e'+'n'+'s')

        self.CancelButton = tk.Button(self, text="CANCEL",
                                      command=lambda: exit("cancelling automation"))
        self.CancelButton.grid(row=6, column=2, padx=5, pady=3,sticky='w'+'e'+'n'+'s')
        pass

    def load(self):
        self.filePath = tkfile.askopenfilename(filetypes=[(self.fileDescript, '*'+self.fileExt)])
        self.data.filePath = self.filePath
        if self.filePath != '':
            self.file.set(os.path.basename(self.filePath))
            if self.cmd != None:
                self.cmd(self.filePath)
        self.fileName.set('file path: ' + self.file.get().split('\\')[-1])

    def removeStock(self):
        #check if this transaction can go through
        #if it can, either remove correct amount by calling stock.subtractStock
        #or delete the stock all together if the removed quantity = total quantity
        #updates portfolio file (use savePortfolio)
        pass
    
    def savePortfolio(self):
        #saves the object to file, use the portfolio name
        pass

    def checkFile(self):
        if os.path.isfile(self.filePath):
            return True
        else:
            False
        # Check to see if a portfolio file exists already 
        # if not query user to select file or create new one
        pass

class stock():

    def __init__(self, ticker, quantity=None,price=None):
        self.ticker = ticker
        self.quantity = quantity
        self.price = price

    def addStock(self, buyQuantity, buyPrice):
        #weighted average to update
        totalQuantity = self.quantity + buyQuantity
        averagePrice = ( self.quantity * self.price + buyQuantity * buyPrice ) / totalQuantity
        self.quantity = totalQuantity
        self.price = averagePrice

    def subtractStock(self, sellQuantity):
        #feasibility checks not handled here
        self.quantity = self.quantity - sellQuantity
        
        

