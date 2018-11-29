class write_back(object):
    def __init__(self):
        self.busy = False
        self.decode = None 
        self.buf = None 
        self.reg = None
    
    def write_back(self, cpu, link):
        self.decode = cpu.decode_unit.decode
        self.reg = cpu.reg
        self.buf = cpu.execute_unit.buf
        if self.decode[0] is "ALU":
            dest = self.decode[2]
            cpu.update_reg(dest, self.buf)
            cpu.sb[dest] = True
        elif self.decode[0] is "DT":
            if cpu.execute_unit.data_transfer_unit.store:
                pass
            dest = self.decode[2]
            print(self.buf)
            cpu.update_reg(dest, self.buf)
            cpu.sb[dest] = True
        elif self.decode[0] is "CF" and link:
            dest = self.decode[2]
            cpu.update_reg(dest, self.buf)
            cpu.sb[dest] = True
        else:
            pass

