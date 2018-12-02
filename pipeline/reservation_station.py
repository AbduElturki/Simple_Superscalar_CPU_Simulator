import pandas as pd

class reservation_station(object):
    def __init__(self, size=16):
        self.size = size
        self.reservation = pd.DataFrame({'busy' : [False] * size,
                                         'unit' : [None] * size,
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

    def is_full(self):
        return all(self.reservation['busy'].tolist())

    def issue(self):
        for row in range(self.size):
            if self.reservation['busy'].iloc[row]:
                rs = self.reservation.iloc[row]
                if rs['valid_1'] and rs['valid_2']:
                    decode = self.rs_to_decode(rs)
                    self.reservation = self.reservation.drop(row).reset_index(
                        drop=True)
                    self.reservation = self.reservation.append(
                        pd.DataFrame({'busy' : [False],
                                      'unit' : [None],
                                      'opcode' : [0x00],
                                      'dest' : [0x00],
                                      'op_1' : [0x00],
                                      'valid_1' : [False],
                                      'op_2' : [0x00],
                                      'valid_2' : [False],
                                      'offset' : [0x00]
                                    }))
                    return decode
            else:
                raise Exception("Stall should have occured here")

    #Not Secure
    def add_instruction(self, decode, cpu):
        if not self.is_free_space():
            raise Exception("Tried to add to instruction to RS when it is not\
                            free")
        for row in range(self.size):
            if not self.reservation['busy'].iloc[row]:
                self.reservation.iloc[row] = decode_to_rs(decode, cpu)
                break

    def add_instruction_test(self):
        if not self.is_free_space():
            raise Exception("Tried to add to instruction to RS when it is not\
                            free")
        for row in range(self.size):
            if not self.reservation['busy'].iloc[row]:
                self.reservation['busy'].iloc[row] = True
                break

    def decode_to_rs(decode, cpu):
        if decode[0] is "ALU":
            if type(decode[4]) is int:
                return [True, "ALU", decode[1], decode[2], decode[3],
                        cpu.sb[decode[3]], decode[4], True, 0]
            else:
                return [True, "ALU", decode[1], decode[2], decode[3],
                        cpu.sb[decode[3]], decode[4], cpu.sb[decode[4]], 0]
        elif decode[0] is "DT":
            if decode[1] in [0x0, 0x1]:
                return [True, "DT", decode[1], decode[2], decode[3],
                        cpu.sb[decode[3]], 0, True, 0]
            elif decode[1] is 0x2:
                return [True, "DT", decode[1], decode[2], decode[3], True, 0,
                        True, 0]
            else:
                return [True, "DT", decode[1], decode[2], decode[4],
                        cpu.sb[decode[4]], 0, True, decode[4]]
        elif decode[0] is "CF":
            if decode[1] in [0x0, 0x2, 0x3]:
                return [True, "CF", decode[1], 0, decode[2], cpu.sb[decode[2]],
                        0, True, 0]
            elif decode[1] is 0x1:
                return [True, "CF", decode[1], 0, decode[2], True, 0, True, 0]
            else:
                return [True, "CF", decode[1], 0, decode[2], cpu.sb[decode[2]],
                        decode[3], cpu.sb[decode[3]], 0]

    def rs_to_decode(rs):
        if rs['unit'] is "ALU":
            return ["ALU", rs['opcode'], rs['dest'], rs['op_1'], rs['op_2']]
        elif rs['unit'] is "DT":
            if rs['opcode'] <= 0x2:
                return ["DT", rs['opcode'], rs['dest'], rs['op_1']]
            else:
                return ["DT", rs['opcode'], rs['dest'], rs['offset'],
                        rs['op_1']]
        elif rs['unit'] is "CF":
            if rs['opcode'] <= 0x3:
                return ["CF", rs['opcode'], rs['op_1']]
            else:
                return ["CF", rs['opcode'], rs['op_1'], rs['op_2']]

    def sb_update(self, cpu):
        self.reservation['valid_1'] = self.reservation['op_1'].apply(
            lambda x: cpu.sb[x] if isinstance(x, str) else True)
        self.reservation['valid_2'] = self.reservation['op_2'].apply(
            lambda x: cpu.sb[x] if isinstance(x, str) else True)
