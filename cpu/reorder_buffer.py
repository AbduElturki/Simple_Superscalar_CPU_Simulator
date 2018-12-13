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
            value = self.rob['value'].iloc[self.head]
            rob = 'ROB' + str(self.head).zfill(2)
            cpu.reg[reg] = value
            cpu.sb[reg] = True
            cpu.update_rat(reg, reg)
            cpu.rs_update_dest(rob, reg)
            cpu.retire_his[rob] = reg
            self.rob.iloc[self.head] = [None, 0x00, False, False]
            self.head = self.head + 1 % self.size 
            head_row = self.rob.iloc[self.head]
            if cpu.is_stalling():
                cpu.stall_reset()

    def issue(self, reg, value, valid, spec):
        if self.tail + 1 % self.size is self.head:
            raise Exception("There should be stall here")
        else:
            self.rob.iloc[self.tail] = [reg, value, valid, spec]
            self.tail = self.tail + 1 % self.size 
            if self.tail + 1 % self.size is self.head:
                cpu.stall()

    def is_empty(self):
        return self.tail == self.head
    
    def get_valid(self, rob):
        self.rob['valid'].iloc[rob]

    def get_value(self, rob):
        return self.rob['value'].iloc[rob]
    
    def update_value(self, rob, update):
        self.rob['value'].iloc[rob] = update

    def merge(self):
        self.rob['spec'] = [False] * size

    def flush(self):
        for row in range(self.size):
            if self.rob['spec'].iloc[row]:
                self.rob = self.rob.drop(row).reset_index(drop=True)
                self.rob.append(pd.DataFrame({'reg' : [None] * size,
                                              'value' : [0x00],
                                              'valid' : [False],
                                              'spec'  : [False]
                                             }))
                self.tail = self.tail - 1 if self.tail else self.size - 1
