from .op_unit import op_unit

class data_transfer(object):
    def execute(self, cpu):
        decode = self.decode
        if decode[1] is 0x0: #LD
            if self.cycle == 1:
                dest = cpu.get_dest(decode[2])
                MAR = cpu.reg[decode[2]]
                if cpu.is_speculative() and MAR in cpu.spec_mem:
                    cpu.WBR[dest] = cpu.spec_mem[self.MAR]
                else:
                    cpu.WBR[dest] = cpu.mem[self.MAR]
            else:
                self.cycle += 1
        elif decode[1] is 0x1: #LDI
            dest = cpu.get_dest(decode[2])
            self.store = False
            cpu.WBR[dest] = decode[3]
        elif decode[1] is 0x2: #ST
            if self.cycle == 2:
                self.store = True
                self.MAR = cpu.reg[decode[3]]
                if cpu.is_speculative():
                    cpu.spec_mem[dest] = cpu.reg[decode[1]]
                else:
                    cpu.mem[self.addr] = cpu.reg[decode[1]]
            else:
                self.cycle += 1
        elif decode[1] is 0x3: #STO
            if self.cycle == 2:
                offset = decode[3]
                MAR = cpu.reg[decode[4]]
                if cpu.is_speculative():
                    cpu.spec_mem[self.offset + self.MAR] = cpu.reg[decode[1]]
                else:
                    cpu.mem[self.offset + self.MAR] = cpu.reg[decode[1]]
            else:
                self.cycle += 1
        elif decode[1] is 0x4:
            if self.cycle == 1:
                dest = cpu.get_dest(decode[2])
                offset = decode[3]
                MAR = offset + cpu.reg[decode[4]]
                if cpu.is_speculative() and MAR in cpu.spec_mem:
                    cpu.WBR[dest] = cpu.spec_mem[self.MAR]
                else:
                    cpu.WBR[dest] = cpu.mem[self.MAR]
            else:
                self.cycle += 1
