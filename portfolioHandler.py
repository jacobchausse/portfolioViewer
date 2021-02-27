# Get stock symbol name
# Get stock quantity
# Get stock purchase price
# Determine if either Portfolio or watchlist

class portfolio():
    def __init__(self, name):
        self.tickerList = [] # List stock objects
        self.name = name
        
    def newStock(self):
        #check if stock is in tickerlist already if it
        #is call stock.updateStock else create new stock object and to its list
        #updates portfolio file (use savePortfolio)
        pass

    def loadPortfolio(self, directory):
        #populate portfolio list with stock objects from file
        pass

    def removeStock(self):
        #check if this transaction can go through
        #if it can, either remove correct amount by calling stock.subtractStock
        #or delete the stock all together if the removed quantity = total quantity
        #updates portfolio file (use savePortfolio)
        pass
    
    def savePortfolio(self):
        #saves the object to file, use the portfolio name
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
        
        

