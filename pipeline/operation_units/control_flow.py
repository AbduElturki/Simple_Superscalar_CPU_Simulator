class control_flow(object):
    def __init__(self):
        self.buf = 0x00
        self.link = False
    def execute(self, decode, cpu):
        if decode[0] is 0x0:
            cpu.pc = int(decode[1] + cpu.reg[decode[2]])
        elif decode[0] is 0x1:
            cpu.pc = int(decode[1] + decode[2])
        elif decode[0] is 0x2:
            cpu.pc += int(decode[1])
        elif decode[0] is 0x3:
            self.link = True
            self.buf = cpu.pc #Might cause unwanted link.
            cpu.pc = int(decode[1] + cpu.reg[decode[2]])

        elif decode[0] is 0x4:
            r1 = cpu.reg[decode[2]]
            r2 = cpu.reg[decode[3]]
            if decode[1] is "EGZ":
                if r1 >= 0:
                    cpu.pc = r2
                else:
                    pass
            elif decode[1] is "LZ":
                if r1 < 0:
                    cpu.pc = r2
                else:
                    pass
            elif decode[1] is "Z":
                if r1 != 0:
                    cpu.pc = r2
                else:
                    pass
            elif decode[1] is "GZ":
                if r1 > 0:
                    cpu.pc = r2
                else:
                    pass
