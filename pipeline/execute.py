from operation_logic import *

class execute_unit(object):
    def __init__(self):
        alu = alu.alu_logic()
        data_transfer = data_transfer.data_transfer()
        self.buf = 0
        self.mode = "ALU"
        self.decode = None 

    def execute(self, mode, decode, reg, memory):
        self.decode = decode
        if self.mode is "ALU":
            self.alu.execute(self.decode)
            self.buf = self.alu.buf
        elif self.mode is "DT":
            self.data_transfer.execute(self.decode, reg, memory)
            self.buf = self.data_transfer.buf



