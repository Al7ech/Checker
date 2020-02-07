import numpy as np
import pandas as pd
import datetime

class Candles(pd.DataFrame):
    def __init__(self, filename : str):
        super().__init__()
        self.read_csv(filename)
        self.name = filename.split('.')[0]

    def read_csv(self, filename : str):
        self.__dict__ = pd.read_csv(filename, index_col = 0,
                                    parse_dates = ["S","E"],
                                    infer_datetime_format = True).__dict__
    
    @property
    def startTime(self):
        return self["S"].iloc[0]

    @property
    def endTime(self):
        return self["E"].iloc[-1]

    @property
    def resolution(self):
        return (self.endTime - self.startTime) / (len(self))

    
    def resize(self, ratio : int, how):
        # Snyc last candle to new resolution
        self.at[self.index[-1],"E"] = self["S"].iloc[-1] + self.resolution * ratio
        self = self.groupby(self.index // ratio).agg(how)
