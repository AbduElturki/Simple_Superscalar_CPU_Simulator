class data_transfer(object):
    def __init__(self):
        self.MBR = 0
        self.MAR = 0
        self.offset = 0
        self.store = False
    def execute(self, decode, cpu):
        if decode[0] is 0x0: #LD
            self.store = False
            self.MAR = decode[2]
            self.MBR = cpu.mem[self.MAR]
        elif decode[0] is 0x1: #LDI
            self.store = False
            self.MBR = decode[2]
        elif decode[0] is 0x2: #ST
            self.store = True
            self.MAR = decode[2]
            cpu.mem[self.addr] = cpu.reg[decode[1]]
        elif decode[0] is 0x3: #STO
            self.store = True
            self.offset = decode[2]
            self.MAR = decode[3]
            cpu.mem[self.offset + self.MAR] = cpu.reg[decode[1]]
