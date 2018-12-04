from .op_unit import op_unit

class data_transfer(object):
    def execute(self, cpu):
        decode = self.decode
        if decode[1] is 0x0: #LD
            dest = cpu.get_dest(decode[2])
            self.store = False
            self.MAR = cpu.reg[decode[2]]
            cpu.WBR[dest] = cpu.mem[self.MAR]
        elif decode[1] is 0x1: #LDI
            dest = cpu.get_dest(decode[2])
            self.store = False
            cpu.WBR[dest] = decode[3]
        elif decode[1] is 0x2: #ST
            self.store = True
            self.MAR = cpu.reg[decode[3]]
            cpu.mem[self.addr] = cpu.reg[decode[1]]
        elif decode[1] is 0x3: #STO
            self.store = True
            self.offset = decode[3]
            self.MAR = cpu.reg[decode[4]]
            cpu.mem[self.offset + self.MAR] = cpu.reg[decode[1]]
        elif decode[1] is 0x4:
            dest = cpu.get_dest(decode[2])
            self.store = False
            self.offset = decode[3]
            self.MAR = offset + cpu.reg[decode[4]]
            self.WBR[dest] = cpu.mem[self.MAR]
