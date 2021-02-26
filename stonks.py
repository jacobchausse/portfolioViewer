import yfinance as yf
import mplfinance as mpf
import pandas as pd
import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from datetime import date


class stockWindow(tk.Tk):
    def  __init__(self):
        tk.Tk.__init__(self)


class stockFrame(tk.Frame):
    def  __init__(self, root, ticker):
        tk.Frame.__init__(self, root)   
        
        self.root=root
        self.ticker = ticker
        self.tickerData = yf.Ticker(ticker)
        
        self.timeFrame = [0,1,0] #days, hours, minutes - default is 1 hour
        self.interval = '1m'
        
        
        mc = mpf.make_marketcolors(base_mpf_style='yahoo', wick='inherit')
        style1 = mpf.make_mpf_style(marketcolors=mc, facecolor='darkslategrey', gridcolor='slategray', gridstyle='--')
        
        self.fig = mpf.figure(figsize=(5,5))
        self.fig.subplots_adjust(hspace=0)
        self.axCandles = self.fig.add_subplot(3,1,(1,2), style=style1)
        self.axVolume = self.fig.add_subplot(3,1,3, style=style1)
        self.axCandles.spines['bottom'].set_visible(False)
        
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(expand=1)
    
    
    def update(self): 
        self.timeStart = datetime.now() - pd.DateOffset(days=self.timeFrame[0], hours=self.timeFrame[1], minutes=self.timeFrame[2])
        df = self.tickerData.history(interval=self.interval, start=self.timeStart.strftime("%Y-%m-%d"))
        dfView = df.loc[self.timeStart:,:]
        self.axCandles.clear()
        self.axVolume.clear()
        
        mpf.plot(dfView, ax=self.axCandles, volume=self.axVolume, type='candle')
        self.canvas.draw()
        
    def clock(self):
        print('updating!')
        self.update()
        self.after(60000, self.clock) #run itself after 1 minute
        
    
root=tk.Tk()
frame = stockFrame(root, 'AAPL')
frame.pack()
frame.clock()

root.mainloop()



