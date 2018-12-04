class alu_logic(object):
    def __init__(self):
        self.is_loaded =False
        self.decode = None
        self.is_busy = False
        self.clock = 0

    def load_decode(self, decode):
        self.decode = decode
        self.is_busy = True
        self.is_loaded = True

    def execute(self, cpu, decode):
        dest = decode[2]
        r2 = cpu.get_value(decode[3])
        r3 = cpu.get_value(decode[4])
        if decode[1] is 0x00: #ADD
           cpu.WBR[dest] = r2 + r3 % 0xFFFFFFFF 
        elif decode[1] is 0x01: #SUB
           cpu.WBR[dest] = r2 - r3 % 0xFFFFFFFF 
        elif decode[1] is 0x02: #MUL
           cpu.WBR[dest] = r2 * r3 % 0xFFFFFFFF 
        elif decode[1] is 0x03: #DIV
           cpu.WBR[dest] = int(r2 / r3) % 0xFFFFFFFF 
        elif decode[1] is 0x04: #XOR
           cpu.WBR[dest] = r2 ^ r3 % 0xFFFFFFFF 
        elif decode[1] is 0x05: #SHL
           cpu.WBR[dest] = r2 << r3 % 0xFFFFFFFF 
        elif decode[1] is 0x06: #SHR
           cpu.WBR[dest] = r2 >> r3 % 0xFFFFFFFF 
        elif decode[1] is 0x07: #CMP
           cpu.WBR[dest] = int('1'*31+'0', 2) if r2 < r3 else 0 if r2 == r3 else 1
