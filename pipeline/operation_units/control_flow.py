class control_flow(object):
    def __init__(self):
        self.is_loaded =False
        self.decode = None
        self.is_busy = False
        self.clock = 0

    def execute(self, decode, cpu):
        if decode[1] is 0x0:
            cpu.pc = cpu.get_value(decode[2])
        elif decode[1] is 0x1:
            cpu.pc = decode[2]
        elif decode[1] is 0x2:
            cpu.pc += decode[1]
        elif decode[1] is 0x3:
            cpu.WBR['R14'] = cpu.pc
            cpu.pc = decode[2]

        elif decode[1] >= 0x4:
            r1 = cpu.get_value(decode[2])
            r2 = decode[3]
            if decode[1] is 0x4:
                if r1 >= 0:
                    cpu.pc = r2
                else:
                    pass
            elif decode[1] is 0x5:
                if r1 < 0:
                    cpu.pc = r2
                else:
                    pass
            elif decode[1] is 0x6:
                if r1 != 0:
                    cpu.pc = r2
                else:
                    pass
            elif decode[1] is 0x7:
                if r1 > 0:
                    cpu.pc = r2
                else:
                    pass
            else:
                raise Exception("In conditional branch section of control_flow\
                                , decode[1] is larger than 0x7")
