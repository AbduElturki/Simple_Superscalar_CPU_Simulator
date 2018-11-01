from operation_logic import *

class execute_unit(object):
    def __init__(self, mode, decode):
        alu = alu.alu_logic()
        self.buf = 0
        self.mode = "ALU"
        self.decode = decode

    def execute(self):
        if self.mode is "ALU":
            self.alu.execute(self.decode)
            self.buf = alu.buf


