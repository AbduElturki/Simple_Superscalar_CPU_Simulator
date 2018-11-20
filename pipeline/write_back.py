class write_back(object):
    def __init__(self):
        self.busy = False
        self.mode = None 
        self.decode = None 
        self.buf = None 
        self.reg = None
    
    def write_back(self, cpu, link):
        self.mode = cpu.decode_unit.mode
        self.decode = cpu.decode_unit.decode
        self.reg = cpu.reg
        self.buf = cpu.execute_unit.buf
        if self.mode is "ALU":
            dest = self.decode[1]
            cpu.update_reg(dest, self.buf)
            cpu.sb[dest] = True
        elif self.mode is "DT":
            if cpu.execute_unit.data_transfer_unit.store:
                pass
            dest = self.decode[1]
            cpu.update_reg(dest, self.buf)
            cpu.sb[dest] = True
        elif self.mode is "CF" and link:
            dest = self.decode[1]
            cpu.update_reg(dest, self.buf)
        else:
            pass

