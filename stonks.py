import yfinance as yf
import mplfinance as mpf
import pandas as pd
import tkinter as tk
from tkinter import ttk
import numpy as np
import pytz

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import matplotlib.pyplot as plt

# TODO if After hours show whole day 
# TODO click on frame goes enlarged view 

global backgroundColor, textColor, font, fontSize
backgroundColor = '#17202e'
textColor = 'lightgrey'
fontName = 'Courier'
fontSizeBig = '15'
fontSizeSmall = '12'



class stockWindow(tk.Tk):
    def  __init__(self, tickerList):
        tk.Tk.__init__(self)
        self.configure(background=backgroundColor)
        self.tickers = tickerList
        self.frameList = [stockFrame(self, ticker) for ticker in tickerList]
        
        gridSize = int(np.ceil(np.sqrt(len(self.frameList))))
        
        counter=0
        for i in range(gridSize):
            for j in range(gridSize):
                counter+=1
                if  counter > len(self.frameList):
                    break
                self.frameList[counter-1].grid(row=i, column=j)
            else:
                continue
            break
    
    
    def startClocks(self):
        for frame in self.frameList: frame.clock()
        
        

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
        self.lbl_title = tk.Label(self, text = str(ticker) + ' - ' + self.tickerData.info['shortName'], bg=backgroundColor, fg='white')
        self.lbl_title.config(font=(fontName, fontSizeSmall, 'bold'))
        
        #price
        self.lbl_priceTitle = tk.Label(self, text = 'Price', bg=backgroundColor, fg=textColor)
        self.lbl_priceTitle.config(font=(fontName, fontSizeSmall, 'bold'))        
        
        self.price = tk.StringVar()
        self.lbl_price = tk.Label(self, textvariable=self.price, bg=backgroundColor)
        self.lbl_price.config(font=(fontName, fontSizeBig, 'bold'))
        
        self.gainsLosses = tk.StringVar()
        self.lbl_gainsLosses = tk.Label(self, textvariable=self.gainsLosses, bg=backgroundColor)
        self.lbl_gainsLosses.config(font=(fontName, fontSizeBig, 'bold'))  
        
        #gains/losses
        self.lbl_gainsLossesTitle = tk.Label(self, text = 'Net Gain', bg=backgroundColor, fg=textColor)
        self.lbl_gainsLossesTitle.config(font=(fontName, fontSizeSmall, 'bold'))        
        
        self.gainsLosses = tk.StringVar()
        self.gainsLosses.set('$ 102.23')
        self.lbl_gainsLosses = tk.Label(self, textvariable=self.gainsLosses, bg=backgroundColor)
        self.lbl_gainsLosses.config(font=(fontName, fontSizeBig, 'bold'))
        
        #quantity
        self.lbl_quantityTitle = tk.Label(self, text = 'Quantity', bg=backgroundColor, fg=textColor)
        self.lbl_quantityTitle.config(font=(fontName, fontSizeSmall, 'bold'))        
        
        self.quantity = tk.StringVar()
        self.quantity.set('6')
        self.lbl_quantity = tk.Label(self, textvariable=self.quantity, bg=backgroundColor, fg=textColor)
        self.lbl_quantity.config(font=(fontName, fontSizeBig, 'bold'))
        
        #plot parameters
        self.timeFrame = [0,5,30] #days, hours, minutes - default is 1 hour
        self.interval = '1m'
        self.intervalDict = {'1m':60000, '5m':5*60000}
        
        #plot style
        mc = mpf.make_marketcolors(base_mpf_style='yahoo', wick='inherit')
        style1 = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=mc, figcolor=backgroundColor, facecolor=backgroundColor, gridcolor='slategray', gridstyle='--')
        
        #create figure and axes
        self.fig = mpf.figure(figsize=(3,3), style=style1, tight_layout=True)
        self.fig.subplots_adjust(hspace=0)
        
        self.axCandles, self.axVolume = self.fig.subplots(2,1, sharex=True, gridspec_kw={'hspace': 0,'height_ratios':[2,1]})
        
        self.axCandles.spines['bottom'].set_visible(False)
        self.axCandles.tick_params(axis='x', colors=backgroundColor)
        
        #create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        
        self.setLayout()
        
    
    def setLayout(self):
        self.lbl_title.grid(column=0, columnspan=2, row=6)
        self.canvas.get_tk_widget().grid(column=0, row=0, rowspan=6)
        
        self.lbl_priceTitle.grid(column=1, row=0)
        self.lbl_price.grid(column=1, row=1)        
        
        self.lbl_gainsLossesTitle.grid(column=1, row=2)
        self.lbl_gainsLosses.grid(column=1, row=3)
        
        self.lbl_quantityTitle.grid(column=1, row=4)
        self.lbl_quantity.grid(column=1, row=5)
        
    
    def update(self): 
        #set start time of plot
        self.timeStart = datetime.now(pytz.utc) - pd.DateOffset(days=self.timeFrame[0], hours=self.timeFrame[1], minutes=self.timeFrame[2])
        
        #retrieve data from start point to present
        df = self.tickerData.history(interval=self.interval, start=self.timeStart.strftime("%Y-%m-%d"))
        dfView = df.loc[self.timeStart:,:]
        
        currentPrice = df.iloc[-1]['Open']
        startPrice = df.iloc[0]['Open']
        diffPrice = currentPrice-startPrice
        
        
        if currentPrice >= startPrice:
            self.lbl_price.config(fg='spring green')
            updown=u'\u23F6'
        elif currentPrice < startPrice:
            self.lbl_price.config(fg='firebrick1')
            updown=u'\u23F7'
            
        self.price.set('$' + str(round(currentPrice,2)) + '\n' + updown + '$' + str(round(diffPrice,2)))
        
        
        #clear axes
        self.axCandles.clear()
        self.axVolume.clear()
        
        #plot on axes and show
        mpf.plot(dfView, ax=self.axCandles, volume=self.axVolume, type='candle', tight_layout=True)
        
        self.axVolume.ticklabel_format(axis='y',style='sci',scilimits=(0,0))
        self.canvas.draw()
        
        
    def clock(self):
        #update with the given interval
        print('updating ticker ' + self.ticker)
        self.update()
        wait = self.intervalDict[self.interval]
        self.after(wait, self.clock) #run itself after 1 minute    
 
        
 
#https://tradingview.com/chart/?symbol=BB

    
def main():
    root=stockWindow(['ENB.TO','ARKK','SU.TO','AAPL','QQQ','WCP.TO','FTNT', 'VCE.TO'])
    root.startClocks()
    root.mainloop()

if __name__ == '__main__':
    main()

