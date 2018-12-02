import pandas as pd

class reorder_buffer(object):
    def __init__(self, size=64):
        self.size = size
        self.rob = pd.DataFrame({'reg' : [None] * size,
                                 'value' : [0x00] * size,
                                 'valid' : [False] * size,
                                })
        self.head = 0
        self.tail = 0
    
    def retire(self):
        self.head = self.head + 1 % 64

    def issue(self, reg, value, valid):
        self.rob.iloc[self.tail] = [reg, value, valid]
        self.tail += self.tail + 1 % 64
    
    def get_valid(self, rob):
        self.rob['valid'].iloc[rob]

    def get_value(self, rob):
        self.rob['value'].iloc[rob]
