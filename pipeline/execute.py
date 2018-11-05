from .operation_units import *

class execute_unit(object):
    def __init__(self):
        self.alu_unit = alu.alu_logic()
        self.data_transfer_unit = data_transfer.data_transfer()
        self.buf = 0
        self.mode = None 
        self.decode = None 

    def execute(self, cpu):
        self.decode = cpu.decode_unit.decode
        self.mode = cpu.decode_unit.mode
        if self.mode is "ALU":
            self.alu_unit.execute(self.decode)
            self.buf = self.alu_unit.buf
        elif self.mode is "DT":
            self.data_transfer_unit.execute(self.decode, cpu.reg, cpu.mem)
            self.buf = self.data_transfer_unit.buf



