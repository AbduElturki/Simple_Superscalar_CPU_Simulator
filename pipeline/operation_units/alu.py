#ALU
#0x00 ADD | 0x04 XOR | 
#0x01 SUB | 0x05 SHL | 
#0x02 MUL | 0x06 SHR |
#0x03 DIV | 0x07 CMP |

class alu_logic(object):
    def __init__(self):
        self.buf = 0
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
