import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None 

class reorder_buffer(object):
    def __init__(self, size=64):
        self.size = size
        self.rob = pd.DataFrame({'reg' : [None] * size,
                                 'value' : [0x00] * size,
                                 'valid' : [False] * size,
                                 'spec'  : [False] * size
                                })
        self.head = 0
        self.tail = 0
    
    def retire(self, cpu):
        head_row = self.rob.iloc[self.head]
        while head_row['valid'] and not head_row['spec']:
            reg = self.rob['reg'].iloc[self.head]
            if reg is None:
                print(self.rob['value'].iloc[self.head])
                raise Exception("None type Register")
            value = self.rob['value'].iloc[self.head]
            if type(value) is str:
                value = cpu.string_2_array(value)
            rob = 'ROB' + str(self.head).zfill(2)
            cpu.reg[reg] = value
            cpu.sb[reg] = True
            cpu.update_rat(reg, reg)
            cpu.his_rat[reg] = reg
            print(reg)
            cpu.rs_update_dest(rob, reg)
            cpu.retire_update(rob, reg)
            cpu.retire_his[rob] = reg
            self.rob.iloc[self.head] = [None, 0x00, False, False]
            self.head = (self.head + 1) % self.size 
            head_row = self.rob.iloc[self.head]
            if cpu.is_stalling():
                cpu.stall_reset()

    def issue(self, reg, value, valid, spec, cpu):
        self.rob.iloc[self.tail] = [reg, value, valid, spec]
        self.tail = (self.tail + 1) % self.size 
        if self.tail + 1 % self.size is self.head:
            cpu.stall()

    def print_rob(self):
        print("ROB")
        print(self.rob)

    def is_empty(self):
        return self.tail == self.head
    
    def get_valid(self, rob):
        self.rob['valid'].iloc[rob]

    def get_value(self, rob):
        return self.rob['value'].iloc[rob]

    def get_reg(self, rob):
        return self.rob['reg'].iloc[rob]
    
    def update_value(self, rob, update):
        if self.rob['reg'] is None:
            raise Exception('')
        if type(update) is list or type(update) is np.ndarray:
            self.rob['value'].iloc[rob] = np.array2string(np.array(update)) 
        else:
            self.rob['value'].iloc[rob] = update 

    def merge(self):
        self.rob['spec'] = [False] * self.size

    def flush(self):
        while self.rob['spec'].iloc[self.tail - 1]:
            self.rob.iloc[self.tail - 1] = [None, 0x00, False, False]
            self.tail = self.tail - 1 if self.tail else self.size - 1
