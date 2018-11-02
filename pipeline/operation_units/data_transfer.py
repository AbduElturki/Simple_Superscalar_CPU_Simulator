class data_transfer(object):
    def __init__(self):
        self.buf = 0
        self.addr = 0
    def execute(self, decode, reg, memory):
        if decode[0] is 0x0:
            self.addr = decode[2]
            self.buf = memory[self.addr]
        elif decode[0] is 0x1:
            self.buf = decode[2]
        elif decode[0] is 0x2:
            self.addr = decode[2]
            self.buf = reg[decode[1]]
            memory[self.addr] = reg[decode[1]]
