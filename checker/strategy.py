import pandas as pd

class Strategy:
    def __init__(self, name : str, *,
                    long_entry = None,
                    long_exit = None,
                    short_entry = None,
                    short_exit = None):
        self.name = name
        self.long_entry = long_entry
        self.long_exit = long_exit
        self.short_entry = short_entry
        self.short_exit = short_exit
        self.long_entry_price = None
        self.long_exit_price = None
        self.short_entry_price = None
        self.short_exit_price = None


    def runable(self):
        return not (self.long_entry is None or
            self.long_exit is None or
            self.short_entry is None or
            self.short_exit is None)
