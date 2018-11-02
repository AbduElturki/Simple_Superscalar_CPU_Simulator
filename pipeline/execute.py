#from operation_units import *
#import operation_units.alu as alu
#import operation_units.data_transfer as data_transfer

class execute_unit(object):
    def __init__(self):
        self.alu_unit = alu.alu_logic()
        self.data_transfer_unit = data_transfer.data_transfer()
        self.buf = 0
        self.mode = "ALU"
        self.decode = None 

    def execute(self, mode, decode, reg, memory):
        self.decode = decode
        if self.mode is "ALU":
            self.alu_unit.execute(self.decode)
            self.buf = self.alu_unit.buf
        elif self.mode is "DT":
            self.data_transfer.execute(self.decode, reg, memory)
            self.buf = self.data_transfer_unit.buf



