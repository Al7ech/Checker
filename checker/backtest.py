from .strategy import Strategy
from .candles import Candles
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
import numpy as np
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

# TODO:
# 수수료
# 점화식 백테스팅
# quantity 설정
# leverage 설정
# 결과지표들 뽑기
# 거래결과 출력 유무
# 

class Backtest:
    def __init__(self):
        self._strategy = None
        self._candles = None
        self._balance_history = []


    def bind_strategy(self, s : Strategy):
        if not s.runable():
            raise NotImplementedError(f'Some properties of "{s.name}" is not implemented.')
        self._strategy = s

    def bind_candles(self, c : Candles):
        self._candles = c

    def run(self):
        N = len(self._candles)

        if not self._strategy.runable():
            raise NotImplementedError(f"Some properties of {self._strategy.name} is not implemented.")

        print("preprocessing strategy...")
        long_entry = self._strategy.long_entry(self._candles)
        long_entry = (long_entry & (~long_entry.shift().fillna(True))).to_numpy()
        long_exit = self._strategy.long_exit(self._candles)
        long_exit = (long_exit & (~long_exit.shift().fillna(True))).to_numpy()
        short_entry = self._strategy.short_entry(self._candles)
        short_entry = (short_entry & (~short_entry.shift().fillna(True))).to_numpy()
        short_exit = self._strategy.short_exit(self._candles)
        short_exit = (short_exit & (~short_exit.shift().fillna(True))).to_numpy()


        long_entry_price = self._strategy.long_entry_price(self._candles)
        long_exit_price = self._strategy.long_exit_price(self._candles)
        short_entry_price = self._strategy.short_entry_price(self._candles)
        short_exit_price = self._strategy.short_exit_price(self._candles)


        # Status : long -> buy_price > 0
        # Status : short -> buy_price < 0
        buy_price = 0
        balance = 1
        balance_pos = 0
        
        print("running backtest...")
        self._balance_history.append(balance)
        with open(self._strategy.name + "_" + self._candles.name + "_result.txt","w") as f:
            for i in range(1,N):
                if long_exit[i]:
                    if buy_price > 0:
                        sell_price = long_exit_price[i]
                        balance = balance_pos * (sell_price - 0.001 * (sell_price + buy_price)) / buy_price
                        balance_pos = 0
                        buy_price = 0
                        f.write(str(self._candles.index[i]) + " : long exit with price =  \t" + str(sell_price) + "\n")
                        f.write(str(self._candles.index[i]) + " : current balance = " + str(balance + balance_pos) + "\n")
                if short_exit[i]:
                    if buy_price < 0:
                        buy_price = -buy_price
                        sell_price = short_exit_price[i]
                        balance = balance_pos * (2*buy_price - sell_price - 0.001 * (sell_price + buy_price)) / buy_price
                        balance_pos = 0
                        buy_price = 0
                        f.write(str(self._candles.index[i]) + " : short exit with price = \t" + str(sell_price) + "\n")
                        f.write(str(self._candles.index[i]) + " : current balance = " + str(balance + balance_pos) + "\n")
                if long_entry[i]:
                    if buy_price == 0:
                        balance_pos = balance
                        balance = 0
                        buy_price = long_entry_price[i]
                        f.write(str(self._candles.index[i]) + " : long entry with price = \t" + str(buy_price) + "\n")
                if short_entry[i]:
                    if buy_price == 0:
                        balance_pos = balance
                        balance = 0
                        buy_price = -short_entry_price[i]
                        f.write(str(self._candles.index[i]) + " : short entry with price = \t" + str(-buy_price) + "\n")
                
                self._balance_history.append(balance + balance_pos)
    
    def plot(self, filename = ""):
        if filename == "":
            filename = self._strategy.name + "_" + self._candles.name + "_plot.png"

        print("drawing graphs...")

        register_matplotlib_converters()

        x = self._candles.index.tolist()
        y = self._balance_history
        

        fig,axes=plt.subplots(nrows=2)
        fig.set_figwidth(50)
        fig.set_figheight(20)
        fig.suptitle('BackTest Result', fontsize=40)
        axes[0].plot(x,y, label="Equity")
        axes[0].title.set_size(30)
        axes[0].set(xlabel="Time", ylabel="Equity Ratio")
        axes[0].xaxis.set_major_locator(mdates.MonthLocator(interval=1))    # xtick interval
        axes[0].tick_params(labelrotation=45)                               # xtick rotation
        axes[0].text(1.01,0.25, "final balance : " + str(round(self._balance_history[-1],3)), size=20, transform=axes[0].transAxes)
        axes[0].title.set_text('Equity Ratio')                              # Set title
        for tick in axes[0].xaxis.get_major_ticks():
                tick.label.set_fontsize(15)
        for tick in axes[0].yaxis.get_major_ticks():
                tick.label.set_fontsize(15)
        axes[0].grid(True)


        axes[1].plot(x,y, label="Equity")
        axes[1].title.set_size(30)
        axes[1].set(xlabel="Time", ylabel="Equity Ratio (Logarithm)")
        axes[1].xaxis.set_major_locator(mdates.MonthLocator(interval=1))    # xtick interval
        axes[1].tick_params(labelrotation=45)                               # xtick rotation
        axes[1].set_yscale("log")                                           # log scale of ER
        axes[1].set_yticks(np.logspace(-0.5, 1, num=4, base=10.0))          # ytick interval
        axes[1].title.set_text('Equity Ratio (Logarithm)')                  # Set title
        for tick in axes[1].xaxis.get_major_ticks():
                tick.label.set_fontsize(15)
        for tick in axes[1].yaxis.get_major_ticks():
                tick.label.set_fontsize(15)
        axes[1].grid(True)

        # # Buy and Sell Indicators
        # for i in range(len(self.short_trade)):
        #     if self.short_trade[i]>0:
        #         axes[0].axvline(x=self._start_datetime + self._delta_datetime*i, color='r', linestyle='-')
        #         axes[1].axvline(x=self._start_datetime + self._delta_datetime*i, color='r', linestyle='-')
        #     if self.short_trade[i]<0:
        #         axes[0].axvline(x=self._start_datetime + self._delta_datetime*i, color='r', linestyle=':')
        #         axes[1].axvline(x=self._start_datetime + self._delta_datetime*i, color='r', linestyle=':')
        #     if self.long_trade[i]>0:
        #         axes[0].axvline(x=self._start_datetime + self._delta_datetime*i, color='g', linestyle='-')
        #         axes[1].axvline(x=self._start_datetime + self._delta_datetime*i, color='g', linestyle='-')
        #     if self.long_trade[i]<0:
        #         axes[0].axvline(x=self._start_datetime + self._delta_datetime*i, color='g', linestyle=':')
        #         axes[1].axvline(x=self._start_datetime + self._delta_datetime*i, color='g', linestyle=':')

        axes[0].legend()
        axes[1].legend()
        
        plt.savefig(filename)
    