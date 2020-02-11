from checker.backtest import Backtest
from checker.strategy import Strategy
from checker.candles import Candles
import pandas as pd
import datetime

import numpy as np

now = datetime.datetime.now()

k=0.582
long_ma_period = 36000
candleLength = 1440

c = Candles("res_1_2018_2020.csv")
c["yH"] = pd.DataFrame(np.repeat(c["H"].rolling(candleLength).max().shift()[::candleLength],candleLength)).set_index(c.index, drop=True)
c["yL"] = pd.DataFrame(np.repeat(c["L"].rolling(candleLength).min().shift()[::candleLength],candleLength)).set_index(c.index, drop=True)
c["delta"] = c["yH"] - c['yL']
c["tO"] = pd.DataFrame(np.repeat(c["O"][::candleLength],candleLength)).set_index(c.index,drop=True)
c["tC"] = pd.DataFrame(np.repeat(c["C"][candleLength-1::candleLength],candleLength)).set_index(c.index,drop=True)
c["BV"] = c["tO"] + k*c["delta"]
c["SV"] = c["tO"] - k*c["delta"]

s = Strategy("VB")
s.long_entry = lambda x : x["C"] >= x["BV"]
s.long_exit = lambda x : x["C"] < x["SV"]
s.short_entry = lambda x : x["C"] <= x["SV"]
s.short_exit = lambda x : x["C"] > x["BV"]
s.long_entry_price = s.short_exit_price = lambda x : x["BV"]
s.long_exit_price = s.short_entry_price = lambda x : x["SV"]

bt = Backtest()
bt.bind_strategy(s)
bt.bind_candles(c)
bt.set_fee(entry_fee=0.001, exit_fee=0.001)
bt.run()
bt.plot()
bt.trade_history()

print("took",datetime.datetime.now() - now)