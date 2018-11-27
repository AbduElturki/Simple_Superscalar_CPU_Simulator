#ALU
#0x00 ADD | 0x04 XOR | 
#0x01 SUB | 0x05 SHL | 
#0x02 MUL | 0x06 SHR |
#0x03 DIV | 0x07 CMP |

class alu_logic(object):
    def __init__(self):
        self.buf = 0
    def execute(self, cpu, decode):
        r2 = cpu.reg[decode[3]]
        r3 = cpu.reg[decode[4]]
        if decode[1] is 0x00: #ADD
           self.buf = r2 + r3 % 0xFFFFFFFF 
           print(self.buf)
        elif decode[1] is 0x01: #SUB
           self.buf = r2 - r3 % 0xFFFFFFFF 
        elif decode[1] is 0x02: #MUL
           self.buf = r2 * r3 % 0xFFFFFFFF 
        elif decode[1] is 0x03: #DIV
           self.buf = int(r2 / r3) % 0xFFFFFFFF 
        elif decode[1] is 0x04: #XOR
           self.buf = r2 ^ r3 % 0xFFFFFFFF 
        elif decode[1] is 0x05: #SHL
           self.buf = r2 << r3 % 0xFFFFFFFF 
        elif decode[1] is 0x06: #SHR
           self.buf = r2 >> r3 % 0xFFFFFFFF 
        elif decode[1] is 0x07: #CMP
           self.buf = int('1'*31+'0', 2) if r2 < r3 else 0 if r2 == r3 else 1
