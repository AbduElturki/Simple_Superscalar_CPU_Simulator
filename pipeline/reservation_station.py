import pandas as pd

class reservation_station(object):
    def __init__(self, size):
        self.size = size
        self.reservation = pd.DataFrame({'busy' : [False] * size,
                                         'opcode' : [0x00] * size,
                                         'dest' : [0x00] * size,
                                         'op_1' : [0x00] * size,
                                         'valid_1' : [False] * size,
                                         'op_2' : [0x00] * size,
                                         'valid_2' : [False] * size,
                                         'offset' : [0x00] * size
                                        })

    def is_free_space(self):
        return (self.reservation['busy'] == False).any()

    def add_instruction(self, decode):
        if not self.is_free_space():
            raise Exception("Tried to add to instruction to RS when it is not\
                            free")
        for row in range(self.size):
            if not self.reservation['busy'].iloc[row]:
                #Add instruction here
                break

    def decode_to_rs(decode, cpu):
        if decode[0] is "ALU":
            if type(decode[4]) is int:
                return [True, decode[1], decode[2], decode[3],
                        cpu.sb[decode[3]], decode[4], True, 0]
            else:
                return [True, decode[1], decode[2], decode[3],
                        cpu.sb[decode[3]], decode[4], cpu.sb[decode[4]], 0]
        elif decode[0] is "DT":
            pass
