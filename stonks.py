import yfinance as yf
import mplfinance as mpf
import pandas as pd
import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime


class stockWindow(tk.Tk):
    def  __init__(self, tickerList):
        tk.Tk.__init__(self)
        self.configure(background='darkslategrey')
        self.tickers = tickerList
        self.frameList = [stockFrame(self, ticker) for ticker in tickerList]
        for frame in self.frameList: frame.pack()
    
    
    def startClocks(self):
        for frame in self.frameList: frame.clock()
        
        

class stockFrame(tk.Frame):
    def  __init__(self, root, ticker):
        tk.Frame.__init__(self, root)   
        
        #define root
        self.root=root
        self.configure(background='darkslategrey')
        
        #ticker info
        self.ticker = ticker
        self.tickerData = yf.Ticker(ticker)
        
        #Frame label
        self.lbl_title = tk.Label(self, text = str(ticker) + ' - ' + self.tickerData.info['shortName'], bg='darkslategrey', fg='white')
        self.lbl_title.grid(column=0, row=1)
        self.lbl_title.config(font=("Courier", 15, 'bold'))
        
        #plot parameters
        self.timeFrame = [0,1,0] #days, hours, minutes - default is 1 hour
        self.interval = '1m'
        self.intervalDict = {'1m':60000, '5m':5*60000}
        
        #plot style
        mc = mpf.make_marketcolors(base_mpf_style='yahoo', wick='inherit')
        style1 = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=mc, figcolor='darkslategrey', facecolor='darkslategrey', gridcolor='slategray', gridstyle='--')
        
        #create figure and axes
        self.fig = mpf.figure(figsize=(5,4), style=style1)
        self.fig.subplots_adjust(hspace=0)
        self.axCandles = self.fig.add_subplot(3,1,(1,2), style=style1)
        self.axVolume = self.fig.add_subplot(3,1,3, style=style1)
        self.axCandles.spines['bottom'].set_visible(False)
        
        #create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().grid(column=0, row=0)
        
    
    def update(self): 
        #set start time of plot
        self.timeStart = datetime.now() - pd.DateOffset(days=self.timeFrame[0], hours=self.timeFrame[1], minutes=self.timeFrame[2])
        
        #retrieve data from start point to present
        df = self.tickerData.history(interval=self.interval, start=self.timeStart.strftime("%Y-%m-%d"), prepost = True)
        dfView = df.loc[self.timeStart:,:]
        
        #clear axes
        self.axCandles.clear()
        self.axVolume.clear()
        
        #plot on axes and show
        mpf.plot(dfView, ax=self.axCandles, volume=self.axVolume, type='candle')
        self.canvas.draw()
        
        
    def clock(self):
        #update with the given interval
        print('updating!')
        self.update()
        wait = self.intervalDict[self.interval]
        self.after(wait, self.clock) #run itself after 1 minute    
        

    
def main():
    root=stockWindow(['ENB.TO','ARKK'])
    root.startClocks()
    root.mainloop()

if __name__ == '__main__':
    main()

