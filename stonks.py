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

# TODO if After hours show whole day 
# TODO click on frame goes enlarged view 

global backgroundColor, textColor, font, fontSize, highlightColor, frameHeight,  frameWidth

frameSize = 400

widthToHeightRatio = 5/4
frameHeight = frameSize
frameWidth = int(frameSize * widthToHeightRatio)
graphSize = round(frameSize/160,1)


backgroundColor = '#17202e'
textColor = 'lightgrey'
fontName = '3ds'
fontSizeBig = str(int(frameSize / 20))
fontSizeSmall = str(int(frameSize / 30))
highlightColor = 'lightslategrey'




class stockWindow(tk.Tk):
    def  __init__(self):
        tk.Tk.__init__(self)
        self.eval('tk::PlaceWindow . center')
        
        self.title('Portfolio Viewer')
        self.configure(background=backgroundColor)
        self.stocksContainer = stocksContainer(self)
        self.btn_addStock = tk.Button(self, text='Add', command = self.addStockWindow, bg=backgroundColor, fg=textColor)
        self.btn_addStock.config(font=(fontName, fontSizeSmall, 'bold'), bg=backgroundColor, fg=textColor)
        
        self.btn_addStock.grid(row=0, column=0, sticky='e')
        self.stocksContainer.grid(row=1,column=0,columnspan=2)
        
        self.bind('<Control_L>a', self.addStockWindow)
        
        self.iconbitmap('portfolioviewer.ico')
    
    
    def addStockWindow(self, event=None):
        win = addStockWindow(self)
        self.eval(f'tk::PlaceWindow {str(win)} center')
        
        

 
class addStockWindow(tk.Toplevel):
    def __init__(self, root):
        tk.Toplevel.__init__(self, root)
        
        self.root = root
        self.configure(background=backgroundColor)
        
        self.title('Add Stock')
        
        self.ent_ticker = simpleEntryFrame(self, 'Ticker') 
        
        
        self.btn_OK = tk.Button(self, text='OK', command = self.OK , bg=backgroundColor, fg=textColor)
        self.btn_cancel = tk.Button(self, text='Cancel', command = self.destroy, bg=backgroundColor, fg=textColor)
        
        self.btn_OK.config(font=(fontName, fontSizeSmall, 'bold'), bg=backgroundColor, fg=textColor)
        self.btn_cancel.config(font=(fontName, fontSizeSmall, 'bold'), bg=backgroundColor, fg=textColor)
        
        self.ent_ticker.grid(row=0,column=0,columnspan=2)
        self.btn_OK.grid(row=1,column=0)
        self.btn_cancel.grid(row=1,column=1)
        
        self.bind('<Return>', self.OK)
        self.bind('<Escape>', lambda event: self.destroy())
        
        self.transient(self.root)
        self.grab_set()
        self.ent_ticker.ent.focus_set()
        
    
    def OK(self, event=None):
        output = self.root.stocksContainer.addStockFrame(self.ent_ticker.ent.get().upper())
        
        if output == True:
            self.destroy()
        else:
            messagebox.showerror('Error', output)
            self.ent_ticker.replaceText('')




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
        self.configure(background=backgroundColor)        
        self.stockFrameList = []
        self.tickerList = []
        
        
    def addStockFrame(self, ticker):
        validate = self.validateAddStock(ticker)
        if validate == True:
            self.stockFrameList.append(stockFrame(self, ticker))
            self.tickerList.append(ticker)
            self.stockFrameList[-1].clock()
            self.updateLayout()

        return validate
        
        
    def removeStockFrame(self, ticker):
        validate = self.validateRemoveStock(ticker)
        if validate == True:
            index = self.tickerList.index(ticker)
            self.tickerList.pop(index)
            self.stockFrameList.pop(index)
            self.updateLayout()
        
        return validate
        
    
    def validateRemoveStock(self, ticker):
        try:
            self.tickerList.index(ticker)
        except:
            return 'Ticker is Not in the List'
        else:
            return True
        
    
    def validateAddStock(self, ticker):
        try:
            yf.Ticker(ticker).info
        except: 
            return 'Ticker Does Not Exist'
        
        try:
            self.tickerList.index(ticker)
        except:
            return True
        else:
            return 'Ticker is Already in the List'
        
            
    def updateLayout(self):
        gridSize = int(np.ceil(np.sqrt(len(self.stockFrameList))))
        
        counter=0
        for i in range(gridSize):
            for j in range(gridSize):
                counter+=1
                if  counter > len(self.stockFrameList):
                    break
                self.stockFrameList[counter-1].grid(row=i, column=j)
            else:
                continue
            break
 
    
 

class stockFrame(tk.Frame):
    def  __init__(self, root, ticker):
        tk.Frame.__init__(self, root)   
        
        #define root
        self.root=root
        self.configure(background=backgroundColor, relief = 'ridge', bd = 4)
        
        #ticker info
        self.ticker = ticker
        self.tickerData = yf.Ticker(ticker)
        
        #Stock title
        self.lbl_title = tk.Label(self, text = str(ticker) , bg=backgroundColor, fg='white') #+ ' - ' + self.tickerData.info['shortName']
        self.lbl_title.config(font=(fontName, fontSizeBig, 'bold'))
        
        #Live indicator
        self.live = tk.StringVar()
        self.lbl_liveCircle = tk.Label(self, text = '      ' + u'\u2B24', bg=backgroundColor)
        self.lbl_live = tk.Label(self, textvariable = self.live, bg=backgroundColor, fg=highlightColor)
        self.lbl_liveCircle.config(font=(fontName, fontSizeSmall, 'bold'))
        self.lbl_live.config(font=(fontName, fontSizeSmall, 'bold'))
        
        #price
        self.lbl_priceTitle = tk.Label(self, text = 'Price', bg=backgroundColor, fg=textColor)
        self.lbl_priceTitle.config(font=(fontName, fontSizeSmall, 'bold'))        
        
        self.price = tk.StringVar()
        self.lbl_price = tk.Label(self, textvariable=self.price, bg=backgroundColor)
        self.lbl_price.config(font=(fontName, fontSizeBig, 'bold'))
        
        self.percentPrice = tk.StringVar()
        self.lbl_percentPrice = tk.Label(self, textvariable=self.percentPrice, bg=backgroundColor, width=15)
        self.lbl_percentPrice.config(font=(fontName, fontSizeSmall, 'bold'))  
        
        #gains/losses
        self.lbl_gainsLossesTitle = tk.Label(self, text = 'Net Gain', bg=backgroundColor, fg=textColor)
        self.lbl_gainsLossesTitle.config(font=(fontName, fontSizeSmall, 'bold'))        
        
        self.gainsLosses = tk.StringVar()
        self.gainsLosses.set('$ 102.23') #temp
        self.lbl_gainsLosses = tk.Label(self, textvariable=self.gainsLosses, bg=backgroundColor)
        self.lbl_gainsLosses.config(font=(fontName, fontSizeBig, 'bold'))        
        
        #quantity
        self.lbl_quantityTitle = tk.Label(self, text = 'Quantity', bg=backgroundColor, fg=textColor)
        self.lbl_quantityTitle.config(font=(fontName, fontSizeSmall, 'bold'))        
        
        self.quantity = tk.StringVar()
        self.quantity.set('6') #temp
        self.lbl_quantity = tk.Label(self, textvariable=self.quantity, bg=backgroundColor, fg=textColor)
        self.lbl_quantity.config(font=(fontName, fontSizeBig, 'bold'))
        
        #plot parameters
        self.timeFrame = [0,0,30] #days, hours, minutes - default is 1 hour
        self.interval = '1m'
        self.intervalDict = {'1m':60000, '5m':5*60000, '15m':15*60000 }
        
        #plot style
        mc = mpf.make_marketcolors(base_mpf_style='yahoo', wick='inherit')
        style1 = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=mc, figcolor=backgroundColor, facecolor=backgroundColor, gridcolor='slategray', gridstyle='--')
        
        #create figure and axes
        self.fig = mpf.figure(figsize=(4/5*graphSize,graphSize), style=style1, tight_layout=True)
        self.fig.subplots_adjust(hspace=0)
        
        self.axCandles, self.axVolume = self.fig.subplots(2,1, sharex=True, gridspec_kw={'hspace': 0,'height_ratios':[2,1]})
        
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
        
        
        #create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().bind("<Double-Button-1>", self.printhello)
        
        #dataFrame
        self.df = None
        
        #puts the widgets in the proper layout
        self.setLayout()
        
        #if set to True will not update the graph
        self.stopClock = False
     
        
    def printhello(self, event):
        print('hello')
    
    
    def setLayout(self):
        pady = 0
        
        self.lbl_title.grid(column=2, columnspan=2, row=6, sticky=tk.W, padx=(20,0))
        self.canvas.get_tk_widget().grid(column=0, columnspan=3, row=0, rowspan=6)
        
        self.lbl_liveCircle.grid(column=0, row=6)
        self.lbl_live.grid(column=1, row=6)
        
        #self.lbl_priceTitle.grid(column=3, row=0, pady=pady)
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
        
        df = self.tickerData.history(interval=self.interval, start=datetime.now().strftime('%Y-%m-%d'))
        
        if df.index[-1] < (datetime.now(pytz.utc) - pd.DateOffset(minutes=5)):
            self.stopClock = True
            dfView = df.iloc[::15,:] #takes every 15 minutes
            
            self.lbl_liveCircle.config(fg='grey')
            self.live.set('A.H.')
        
        else:
            #set start time of plot
            self.timeStart = datetime.now(pytz.utc) - pd.DateOffset(days=self.timeFrame[0], hours=self.timeFrame[1], minutes=self.timeFrame[2])
            
            #retrieve data from start point to present
            dfView = df.loc[self.timeStart:,:]
            
            self.lbl_liveCircle.config(fg='red')
            self.live.set('Live')
        
        currentPrice = df.iloc[-1]['Open']
        startPrice = df.iloc[0]['Open']
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
            
        self.price.set('$' + str(round(currentPrice,2)))
        self.percentPrice.set(updown + '$' + str(round(abs(diffPrice),2)) + '(' + str(round(abs(percentDiff),2)) + '%)')
        
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
    stockWindow()
    tk.mainloop()

if __name__ == '__main__':
    main()

