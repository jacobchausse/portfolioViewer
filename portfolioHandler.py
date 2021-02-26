# Get stock symbol name
# Get stock quantity
# Get stock purchase price
# Determine if either Portfolio or watchlist

class portfolio():
    def __init__(self, name):
        self.tickerList = [] # List stock objects
        self.name = name
        
    def newStock(self):
        # Check if stock is in tickerlist already if it
        # is call stock.updateStock else create new stock object and to its list
        # updates portfolio file

    def loadPortfolio(self, dir):
        # populate portfolio list with stock objects

    def deleteStock(self, ticker, quanitity, price):
        # 

class stock():

    def __init__(self, ticker, quantity=None,price=None):
        self.ticker = ticker
        self.quantity = quantity
        self.price = price

    def addStock(self, newQuantity, newPrice):
        # Determine average price
        # update self quanitity and price with the average price
        # ingest prior data 
        totalQuantity = self.quantity + newQuantity
        averagePrice = ( self.quantity * self.price + newQuantity * newPrice ) / totalQuantity
        self.quantity = totalQuantity
        self.price = averagePrice

    def removeStock(self):
        #check if this transaction can go through

