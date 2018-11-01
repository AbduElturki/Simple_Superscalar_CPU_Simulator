#ALU
#0x00 ADD | 0x04 XOR | 
#0x01 SUB | 0x05 SHL | 
#0x02 MUL | 0x06 SHR |
#0x03 DIV | 0x07 CMP |

class alu_logic(object):
    def __init__(self):
        self.buf = 0
    def execute(self, decode):
        if decode[0] is 0x00: #ADD
           self.buf = decode[2] + decode[3] % 0xFFFFFFFF 
        elif decode[0] is 0x01: #SUB
           self.buf = decode[2] - decode[3] % 0xFFFFFFFF 
        elif decode[0] is 0x02: #MUL
           self.buf = decode[2] * decode[3] % 0xFFFFFFFF 
        elif decode[0] is 0x03: #DIV
           self.buf = int(decode[2] / decode[3]) % 0xFFFFFFFF 
        elif decode[0] is 0x04: #XOR
           self.buf = decode[2] ^ decode[3] % 0xFFFFFFFF 
        elif decode[0] is 0x05: #SHL
           self.buf = decode[2] << decode[3] % 0xFFFFFFFF 
        elif decode[0] is 0x06: #SHR
           self.buf = decode[2] >> decode[3] % 0xFFFFFFFF 
        elif decode[0] is 0x07: #CMP
           self.buf = int('1'*31+'0', 2) if decode[2] < decode[3] else 0 if decode[2] == decode[3] else 1
