class write_back(object):
    def __init__(self):
        self.mode = None 
        self.decode = None 
        self.buf = None 
        self.reg = None
    
    def write_back(self, cpu):
        self.mode = cpu.decode_unit.mode
        self.decode = cpu.decode_unit.decode
        self.reg = cpu.reg
        self.buf = cpu.execute_unit.buf
        if self.mode is "ALU":
            dest = self.decode[1]
            cpu.update_reg(dest, self.buf)
        elif self.mode is "DT":
            dest = self.decode[1]
            cpu.update_reg(dest, self.buf)
        else:
            pass

