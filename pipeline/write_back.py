class write_back(object):
    def __init__(self):
        self.busy = False
        self.decode = None 
        self.buf = None 
        self.reg = None
    
    def write_back(self, cpu):
        for dest in cpu.WBR:
            cpu.update_reg(dest, cpu.WBR[dest])
            cpu.set_valid(dest)
        cpu.WBR = {}
        cpu.rob_retire()
    
