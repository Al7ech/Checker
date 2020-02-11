from checker.backtest import Backtest
from checker.strategy import Strategy
from checker.candles import Candles
import datetime

import numpy as np

c = Candles("res_1_2018_2020.csv")
c["sma"] = c["C"].rolling(10).mean()
c["lma"] = c["C"].rolling(2000).mean()
c["high"] = c["lma"] + 0.005 * c["C"] + 0.01
c["low"] = c["lma"] + 0.005 * c["C"] - 0.01

s = Strategy("ES")
s.long_entry = lambda x : x["sma"] >= x["high"]
s.long_exit = lambda x : x["sma"] < x["low"]
s.short_entry = lambda x : x["sma"] <= x["low"]
s.short_exit = lambda x : x["sma"] > x["high"]
s.long_entry_price = s.long_exit_price = s.short_entry_price = s.short_exit_price = lambda x : x["C"]

bt = Backtest()
bt.bind_strategy(s)
bt.bind_candles(c)
bt.set_fee(entry_fee=0.001, exit_fee=0.001)
bt.run()