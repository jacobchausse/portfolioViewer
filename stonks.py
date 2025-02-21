
#external libraries
import yfinance as yf
import mplfinance as mpf
import pandas as pd
import tkinter as tk
from tkinter import ttk
import numpy as np
import pytz
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import os
from forex_python.converter import CurrencyRates


#local files
from portfolioHandler import portfolio


#global parameters
global timeZone, backgroundColor, textColor, font, fontSize, highlightColor, frameHeight,  frameWidth, currentDir

currentDir = os.path.dirname(os.path.realpath(__file__))

timeZone = pytz.timezone('US/Eastern')
frameSize = 500

widthToHeightRatio = 5/4
frameHeight = frameSize
frameWidth = int(frameSize * widthToHeightRatio)
graphSize = round(frameSize/160,1)

backgroundColor = '#17202e'
textColor = 'lightgrey'
highlightColor = 'lightslategrey'

fontName = '3ds'
fontSizeBig = str(int(frameSize / 20))
fontSizeSmall = str(int(frameSize / 30))


#TODO "there are unsaved changes" flag set to True or False
#TODO config file with all startup settings
#TODO construct and update portfolio object
#TODO change currency
#TODO Lezajsk mode
#TODO add refresh button to each stock frame that restarts the clock if A.H. or B.H.


class portfolioViewerApp(tk.Tk):
    def  __init__(self):
        tk.Tk.__init__(self)

        #TODO if portfolio is loaded, display name

        self.iconbitmap(currentDir + '\\portfolioviewer.ico')
        self.eval('tk::PlaceWindow . center')
        
        self.title('Portfolio Viewer')
        self.configure(background=backgroundColor)
        
        self.portfolioCurrency = tk.StringVar() 
        self.portfolioCurrency.set('CAD')               #TODO make this changeable
        self.lbl_currency = tk.Label(self, textvariable=self.portfolioCurrency)
        self.lbl_currency.grid(row=0,column=0)
        self.lbl_currency.config(font=(fontName, fontSizeBig, 'bold'), bg=backgroundColor, fg=textColor)  

        self.stocksContainer = stocksContainer(self)
        self.stocksContainer.grid(row=1,column=0,columnspan=2)
        
        self.menuBar = tk.Menu(self)
        self.configure(menu=self.menuBar)
        self.mnu_portfolio = tk.Menu(self.menuBar, tearoff=0)
        self.mnu_portfolio.add_command(label="Open - Ctrl+O", command=self.loadPortfolioWindow)
        self.mnu_portfolio.add_command(label="New - Ctrl+N", command=self.addStockWindow) # TODO make it work correctly
        self.mnu_portfolio.add_command(label="Save - Ctrl+S", command=self.savePortfolioWindow)
        self.mnu_portfolio.add_separator()
        self.mnu_portfolio.add_command(label="Add Stock - Ctrl+A", command=self.addStockWindow) 
        self.mnu_portfolio.add_command(label="Remove Stock - Ctrl+R", command=self.addStockWindow) # TODO make it work correctly
        self.menuBar.add_cascade(label="Portfolio", menu=self.mnu_portfolio)
        
        self.bind('<Control_L>a', self.addStockWindow)
        self.bind('<Control_L>o', self.loadPortfolioWindow)
        self.bind('<Control_L>s', self.savePortfolioWindow)


    def savePortfolioWindow(self, event=None):
        win = savePortfolioWindow(self)
        self.eval(f'tk::PlaceWindow {str(win)} center')


    def loadPortfolioWindow(self, event=None):
        win = loadPortfolioWindow(self)
        self.eval(f'tk::PlaceWindow {str(win)} center')


    def addStockWindow(self, event=None):
        win = addStockWindow(self)
        self.eval(f'tk::PlaceWindow {str(win)} center')



class savePortfolioWindow(tk.Toplevel):
    def __init__(self, root):
        tk.Toplevel.__init__(self, root)
        self.root = root
        self.iconbitmap(currentDir + '\\portfolioviewer.ico')
        
        self.ent_name = simpleEntryFrame(self, 'Portfolio Name') 
        self.btn_OK = tk.Button(self, text='OK', command = self.OK, bg=backgroundColor, fg=textColor)
        self.btn_cancel = tk.Button(self, text='Cancel', command = self.destroy, bg=backgroundColor, fg=textColor)
        
        self.configureWindow()
        self.setLayout()
        self.transient(self.root) 
        self.grab_set()
        self.ent_name.ent.focus_set()
        
        
    def configureWindow(self):
        self.configure(background=backgroundColor)
        self.title('Add Stock')
        
        self.btn_OK.config(font=(fontName, fontSizeSmall, 'bold'), bg=backgroundColor, fg=textColor)
        self.btn_cancel.config(font=(fontName, fontSizeSmall, 'bold'), bg=backgroundColor, fg=textColor)        
 
        self.bind('<Return>', self.OK)
        self.bind('<Escape>', lambda event: self.destroy()) 
        
    
    def setLayout(self):
        self.ent_name.grid(row=0,column=0,columnspan=2)
        self.btn_OK.grid(row=1,column=0)
        self.btn_cancel.grid(row=1,column=1)

    
    def OK(self, event=None):  
        #TODO check if the name is good, only letters numbers - _  
        #TODO catch os error
        #TODO check if there is at least 1 stock
        #TODO add functionality

        fileName = self.ent_name.ent.get()

        with open(currentDir + '\\saves\\' + fileName + '.portfolio', "w") as portfolio:
            # Get all stock objects
            portfolio.write(self.root.portfolioCurrency.get() + "\n")
            for stock in self.root.stocksContainer.stockList[:-1]:
                portfolio.write(stock.ticker + "," + str(stock.quantity) + "," + str(stock.buyPrice) +"\n")
            
            stock = self.root.stocksContainer.stockList[-1]
            portfolio.write((stock.ticker + "," + str(stock.quantity) + "," + str(stock.buyPrice)))

        self.destroy()

        
class loadPortfolioWindow(tk.Toplevel):
    def __init__(self, root):
        tk.Toplevel.__init__(self, root)
        self.root = root
        self.iconbitmap(currentDir + '\\portfolioviewer.ico')

        self.portfolios = None
        self.var_portfolio = tk.StringVar()

        self.findPortfolios()
        self.opt_portfolios = tk.OptionMenu(self, self.var_portfolio, *self.portfolios)

        self.btn_OK = tk.Button(self, text='OK', command = self.OK, bg=backgroundColor, fg=textColor)
        self.btn_cancel = tk.Button(self, text='Cancel', command = self.destroy, bg=backgroundColor, fg=textColor)
        
        self.configureWindow()
        self.setLayout()
        self.transient(self.root)
        self.grab_set()


    def findPortfolios(self):
        pathList = os.listdir(currentDir + '\\saves\\')
        if len(pathList) == 0:
            #TODO throw error
            pass
        else:
            self.portfolios = [os.path.splitext(path)[0] for path in pathList]

        
    def configureWindow(self):
        self.configure(background=backgroundColor)
        self.title('Load Portfolio')
        
        self.opt_portfolios.config(font=(fontName, fontSizeSmall, 'bold'), bg=backgroundColor, fg=textColor)
        self.btn_OK.config(font=(fontName, fontSizeSmall, 'bold'), bg=backgroundColor, fg=textColor)
        self.btn_cancel.config(font=(fontName, fontSizeSmall, 'bold'), bg=backgroundColor, fg=textColor)        
 
        self.bind('<Return>', self.OK)
        self.bind('<Escape>', lambda event: self.destroy()) 
        
    
    def setLayout(self):
        self.opt_portfolios.grid(row=0,column=0, columnspan=2)
        self.btn_OK.grid(row=1,column=0)
        self.btn_cancel.grid(row=1,column=1)
 
    
    def OK(self, event=None):
        #TODO flush current portfolio
        
        for stock in self.root.stocksContainer.stockList:
            stock.destroy()
        self.root.stocksContainer.stockList=[]    

        path = currentDir + '\\saves\\' + self.var_portfolio.get() + '.portfolio'
        allLines = []

        with open(path, 'r') as portfolio:
            for line in portfolio:
                allLines.append(line)

        self.root.portfolioCurrency.set(allLines[0].rstrip())
        for line in allLines[1:]:        
            ticker, quantity, price = (line.split(","))
            output = self.root.stocksContainer.addstock(ticker.upper(), int(quantity), float(price), doValidate=False)

            if output != True:
                print("ur big stinky")
                #TODO think about mistakes in life
                break
                
        self.destroy()




class addStockWindow(tk.Toplevel):
    def __init__(self, root):
        tk.Toplevel.__init__(self, root)
        self.root = root
        self.iconbitmap(currentDir + '\\portfolioviewer.ico')
        
        self.ent_ticker = simpleEntryFrame(self, 'Ticker') 
        self.btn_OK = tk.Button(self, text='OK', command = self.OK, bg=backgroundColor, fg=textColor)
        self.btn_cancel = tk.Button(self, text='Cancel', command = self.destroy, bg=backgroundColor, fg=textColor)
        
        self.configureWindow()
        self.setLayout()
        self.transient(self.root)
        self.grab_set()
        self.ent_ticker.ent.focus_set()
        
        
    def configureWindow(self):
        self.configure(background=backgroundColor)
        self.title('Add Stock')
        
        self.btn_OK.config(font=(fontName, fontSizeSmall, 'bold'), bg=backgroundColor, fg=textColor)
        self.btn_cancel.config(font=(fontName, fontSizeSmall, 'bold'), bg=backgroundColor, fg=textColor)        
 
        self.bind('<Return>', self.OK)
        self.bind('<Escape>', lambda event: self.destroy()) 
        
    
    def setLayout(self):
        self.ent_ticker.grid(row=0,column=0,columnspan=2)
        self.btn_OK.grid(row=1,column=0)
        self.btn_cancel.grid(row=1,column=1)
 
    
    def OK(self, event=None):        
        output = self.root.stocksContainer.addstock(self.ent_ticker.ent.get().upper())
        
        if output == True:
            self.destroy()
        else:
            messagebox.showerror('Error', output)
            self.ent_ticker.replaceText('')




#taken as is from https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python
class ToolTip():

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      bg=backgroundColor, relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "10", "normal"), fg=textColor)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()





class simpleEntryFrame(tk.Frame):
    
    def __init__(self, root, title, width=15, default='', validate=str):
        tk.Frame.__init__(self, root)
        self.configure(background=backgroundColor)
        self.root=root
        self.validate = validate
        
        vcmd = (self.register(self.validateCmd))
        
        self.ent=tk.Entry(self, width=width, validate='all', validatecommand=(vcmd, '%P'))
        self.ent.insert(tk.END, str(default))
        self.lbl=tk.Label(self, text=title)
        
        self.ent.config(font=(fontName, fontSizeSmall, 'bold'), bg=backgroundColor, fg=textColor)
        self.lbl.config(font=(fontName, fontSizeSmall, 'bold'), bg=backgroundColor, fg=textColor)
        
        self.ent.grid(row=0, column=1, padx=(10,0))
        self.lbl.grid(row=0, column=0)
        
    
    def replaceText(self, text):
        self.ent.delete(0, 'end')
        self.ent.insert(tk.END, text)
    
           
    def validateCmd(self, P):
        if not P == '':
            try:
                self.validate(P)
            except:
                return False
        return True

        
    
        

class stocksContainer(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root, height=frameHeight,  width=frameWidth)
        self.root = root
        self.configure(background=backgroundColor)        
        self.stockList = []
        
        
    def addstock(self, ticker, quantity=0, price=0, currency='CAD', doValidate=True):
        if doValidate:
            validate = self.validateAddStock(ticker)
        else:
            validate=True
        
        if validate == True:
            self.stockList.append(stock(self, ticker, quantity, price))
            self.stockList[-1].clock()
            self.updateLayout()

        return validate
        
        
    def removestock(self, ticker):
        validate = self.validateRemoveStock(ticker)
        if validate == True:
            index = self.tickerList.index(ticker)
            self.tickerList.pop(index)
            self.stockList.pop(index)
            self.updateLayout()
        
        return validate
        
    
    def validateRemoveStock(self, ticker):
        #TODO change validation when working with portfolio object
        try:
            self.tickerList.index(ticker)
        except:
            return 'Ticker is Not in the List'
        else:
            return True
        
    
    def validateAddStock(self, ticker):
        #TODO change validation when working with portfolio object
        try:
            yf.Ticker(ticker).financials #naive check
        except: 
            return 'Ticker Does Not Exist'
        
        try:
            self.tickerList.index(ticker)
        except:
            return True
        else:
            return 'Ticker is Already in the List'
        
            
    def updateLayout(self):
        gridSize = int(np.ceil(np.sqrt(len(self.stockList))))
        
        counter=0
        for i in range(gridSize):
            for j in range(gridSize):
                counter+=1
                if  counter > len(self.stockList):
                    break
                self.stockList[counter-1].grid(row=i, column=j)
            else:
                continue
            break

  

class stock(tk.Frame):
    def  __init__(self, root, ticker, quantity, price):
        tk.Frame.__init__(self, root)   
        
        #TODO add BUY and SELL buttons

        #define root
        self.root=root
        
        #ticker info
        self.ticker = ticker
        self.quantity = quantity
        self.buyPrice = price

        self.tickerData = yf.Ticker(ticker)
        self.info = self.tickerData.info

        #Stock title
        self.lbl_title = tk.Label(self, text = str(ticker)) #+ ' - ' + self.tickerData.info['shortName']
        
        #Live indicator
        self.var_live = tk.StringVar()
        
        self.lbl_liveCircle = tk.Label(self, text = '      ' + u'\u2B24')
        self.lbl_live = tk.Label(self, textvariable = self.var_live)
        
        tiptext_live = 'A.H. (After Hours) or B.H. (Before Hours) displays data for the previous day \nLive displays updating data on a 30 min. interval'
        
        self.tip = ToolTip(self.lbl_live)
        self.lbl_live.bind('<Button-1>', lambda event: self.tip.showtip(tiptext_live))
        self.lbl_live.bind('<Leave>', lambda event: self.tip.hidetip())
        
        #price
        self.var_price = tk.StringVar()
        self.var_pricePercent = tk.StringVar()
        
        self.lbl_price = tk.Label(self, textvariable=self.var_price)
        self.lbl_percentPrice = tk.Label(self, textvariable=self.var_pricePercent, width=15)
        
        #gains/losses
        self.var_gainsLosses = tk.StringVar()
        
        self.lbl_gainsLossesTitle = tk.Label(self, text = 'Net Gain')
        self.lbl_gainsLosses = tk.Label(self, textvariable=self.var_gainsLosses)
        
        #quantity
        self.var_quantity = tk.StringVar()
        self.var_quantity.set(quantity)

        self.lbl_quantityTitle = tk.Label(self, text = 'Quantity')
        self.lbl_quantity = tk.Label(self, textvariable=self.var_quantity)
        
        #plot parameters
        self.timeFrame = [0,0,30] #days, hours, minutes - default is 30 mins
        self.interval = '1m'
        self.intervalDict = {'1m':60000}
        
        #plot style
        mc = mpf.make_marketcolors(base_mpf_style='yahoo', wick='inherit')
        style1 = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=mc, figcolor=backgroundColor, facecolor=backgroundColor, gridcolor='slategray', gridstyle='--')
        
        #create figure and axes
        self.fig = mpf.figure(figsize=(4/5*graphSize,graphSize), style=style1, tight_layout=True)
        self.fig.subplots_adjust(hspace=0)
        self.axCandles, self.axVolume = self.fig.subplots(2,1, sharex=True, gridspec_kw={'hspace': 0,'height_ratios':[2,1]})
        
        #create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().bind("<Double-Button-1>", self.printhello) #TODO link this with enlarged view
        
        #configure all widgets and set layout
        self.configureFrame()
        self.setLayout()
        
        #dataFrame
        self.df = None
        
        #puts the widgets in the proper layout
        self.setLayout()
        
        #if set to True will not update the graph
        self.stopClock = False
     
        
    def printhello(self, event):
        print('hello')
        # TODO click on frame goes enlarged view 
    
    
    def configureFrame(self):
        #configure frame
        self.configure(background=backgroundColor, relief = 'ridge', bd = 4)
        
        #configure label widgets
        #TODO explain after/before hours graph behaviour (shows whole day) when click on the A.H./B.H. https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python
        self.lbl_title.config(font=(fontName, fontSizeBig, 'bold'), bg=backgroundColor, fg=textColor)
        
        self.lbl_liveCircle.config(font=(fontName, fontSizeSmall, 'bold'), bg=backgroundColor)
        self.lbl_live.config(font=(fontName, fontSizeSmall, 'bold'), bg=backgroundColor, fg=textColor)
        
        self.lbl_price.config(font=(fontName, fontSizeBig, 'bold'), bg=backgroundColor, fg=textColor)
        self.lbl_percentPrice.config(font=(fontName, fontSizeSmall, 'bold'), bg=backgroundColor, fg=textColor)  
        
        self.lbl_gainsLossesTitle.config(font=(fontName, fontSizeSmall, 'bold'), bg=backgroundColor, fg=textColor)   
        self.lbl_gainsLosses.config(font=(fontName, fontSizeBig, 'bold'), bg=backgroundColor, fg=textColor)    
        
        self.lbl_quantityTitle.config(font=(fontName, fontSizeSmall, 'bold'), bg=backgroundColor, fg=textColor)  
        self.lbl_quantity.config(font=(fontName, fontSizeBig, 'bold'), bg=backgroundColor, fg=textColor)
        
        #configure plot widget
        self.axCandles.spines['bottom'].set_visible(False)
        self.axCandles.tick_params(axis='x', colors=backgroundColor)
        
        self.axCandles.axes.xaxis.set_visible(False)
        self.axCandles.axes.yaxis.set_visible(False)
        self.axVolume.axes.xaxis.set_visible(False)
        self.axVolume.axes.yaxis.set_visible(False)
        
        self.axCandles.spines['bottom'].set_color(highlightColor)
        self.axCandles.spines['top'].set_color(highlightColor)
        self.axCandles.spines['left'].set_color(highlightColor)
        self.axCandles.spines['right'].set_color(highlightColor)
        self.axVolume.spines['bottom'].set_color(highlightColor)
        self.axVolume.spines['top'].set_color(highlightColor)
        self.axVolume.spines['left'].set_color(highlightColor)
        self.axVolume.spines['right'].set_color(highlightColor)
        
        
    def setLayout(self):
        pady = 0
        
        self.lbl_title.grid(column=2, columnspan=2, row=6, sticky=tk.W, padx=(20,0))
        self.canvas.get_tk_widget().grid(column=0, columnspan=3, row=0, rowspan=6)
        
        self.lbl_liveCircle.grid(column=0, row=6)
        self.lbl_live.grid(column=1, row=6)
        
        self.lbl_price.grid(column=3, row=0, pady=(5,0)) 
        self.lbl_percentPrice.grid(column=3, row=1, pady=pady, sticky=tk.N) 
        
        self.lbl_gainsLossesTitle.grid(column=3, row=2, pady=pady)
        self.lbl_gainsLosses.grid(column=3, row=3, pady=pady, sticky=tk.N)
        
        self.lbl_quantityTitle.grid(column=3, row=4, pady=pady)
        self.lbl_quantity.grid(column=3, row=5, pady=pady, sticky=tk.N)
    
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        
    
    def update(self):

        if self.info['currency'] != self.root.root.portfolioCurrency.get():
            conversionFactor = CurrencyRates().get_rate(self.info['currency'],self.root.root.portfolioCurrency.get())
        else:
            conversionFactor=1


        weekday = datetime.today().weekday() #weekday index
        
        if weekday == 0: #if it is monday
            prevDay = (datetime.now(timeZone)- pd.DateOffset(days=3)).strftime('%Y-%m-%d')      
        elif weekday == 6: #if sunday
            prevDay = (datetime.now(timeZone)- pd.DateOffset(days=2)).strftime('%Y-%m-%d')
        else: #if any other day
            prevDay = (datetime.now(timeZone)- pd.DateOffset(days=1)).strftime('%Y-%m-%d') 
        
        today = datetime.now(timeZone).strftime('%Y-%m-%d')
        
        now = datetime.now(timeZone)
        startOfTheDay = now.replace(hour=0, minute=0,second=0, microsecond=0)
        
        df = self.tickerData.history(interval=self.interval, start=prevDay)
        priceEndPrevDay = df.loc[:prevDay,:].iloc[-1] #used to calculate % change
        
        if df.index[-1] < (now - pd.DateOffset(minutes=5)):
            self.stopClock = True
            
            if df.index[-1] < startOfTheDay: #before hours
                dfView = df.loc[:prevDay,:] 
                self.var_live.set('B.H.')
                
            else: #after hours
                dfView = df.loc[today:,:] 
                self.var_live.set('A.H.')
            
            dfView = dfView.iloc[::15,:] #takes every 15 minutes for clarity
            
            self.lbl_liveCircle.config(fg='grey')
            
        
        else:
            #set start time of plot
            self.timeStart = datetime.now(timeZone) - pd.DateOffset(days=self.timeFrame[0], hours=self.timeFrame[1], minutes=self.timeFrame[2])
            
            #retrieve data from start point to present
            dfView = df.loc[self.timeStart:,:]
            
            self.lbl_liveCircle.config(fg='red')
            self.var_live.set('Live')
        
        currentPrice = df.iloc[-1]['Open']
        startPrice = priceEndPrevDay['Open']
        diffPrice = currentPrice-startPrice
        percentDiff = diffPrice / currentPrice * 100
        
        if currentPrice >= startPrice:
            self.lbl_price.config(fg='spring green')
            self.lbl_percentPrice.config(fg='spring green')
            updown=u'\u23F6'
        elif currentPrice < startPrice:
            self.lbl_price.config(fg='firebrick1')
            self.lbl_percentPrice.config(fg='firebrick1')
            updown=u'\u23F7'
            
        self.var_price.set('$' + str(round(currentPrice * conversionFactor,2)))
        self.var_pricePercent.set(updown + '$' + str(round(abs(diffPrice * conversionFactor),2)) + '(' + str(round(abs(percentDiff),2)) + '%)')
        
        #set gainsLosses
        if self.quantity != 0:
            gainsLosses = round(self.quantity*(currentPrice * conversionFactor - self.buyPrice), 2)
            self.var_gainsLosses.set( str(gainsLosses) + '$' ) 

        #clear axes
        self.axCandles.clear()
        self.axVolume.clear()
        
        #plot on axes and show
        mpf.plot(dfView, ax=self.axCandles, volume=self.axVolume, type='candle', tight_layout=True)
        
        self.axVolume.margins(0)
        self.axCandles.margins(0)
        
        self.canvas.draw()
        
        
    def clock(self):
        #update with the given interval
        self.update()
        wait = self.intervalDict[self.interval]
        
        if not self.stopClock:    
            self.after(wait, self.clock) #run itself after 1 minute    
 
        

#https://tradingview.com/chart/?symbol=BB

    
def main():
    portfolioViewerApp()
    tk.mainloop()

if __name__ == '__main__':
    main()

