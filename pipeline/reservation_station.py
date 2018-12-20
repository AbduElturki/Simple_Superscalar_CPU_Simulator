import pandas as pd
pd.options.mode.chained_assignment = None 

class reservation_station(object):
    def __init__(self, op_unit=[], size=16):
        self.size = size
        self.op_unit = op_unit
        self.reservation = pd.DataFrame({'busy' : [False] * size,
                                         'unit' : [None] * size,
                                         'opcode' : [0x00] * size,
                                         'dest' : [0x00] * size,
                                         'op_1' : [None] * size,
                                         'valid_1' : [False] * size,
                                         'op_2' : [None] * size,
                                         'valid_2' : [False] * size,
                                         'offset' : [0x00] * size,
                                         'spec' : [False] * size
                                        })

    def is_free_space(self):
        f = lambda x: not x
        return any(map(f,self.reservation['busy'].tolist()))

    def is_empty(self):
        return (self.reservation['busy'] == False).all()

    def is_full(self):
        return all(self.reservation['busy'].tolist())

    def is_any_slot_ready(self):
        return any(self.reservation['valid_1'].tolist() and \
                   self.reservation['valid_2'].tolist())

    def is_free_op_unit(self):
        return any([(not op.is_busy) for op in self.op_unit])

    def is_issuable(self):
        return self.is_any_slot_ready() or self.is_free_space()

    def is_all_op_unit_busy(self):
        return all([op.is_busy for op in self.op_unit])

    def can_bypass(self, decode, cpu):
        rs = self.decode_to_rs(decode, cpu)
        valid = rs[5] and rs[7]
        return self.is_empty() and self.is_free_op_unit() and valid

    def bypass(self, decode, cpu, spec):
        for i in range(len(self.op_unit)):
            if not self.op_unit[i].is_busy:
                self.op_unit[i].load_decode(decode, spec)
                self.op_unit[i].execute(cpu)
                break

    def free_slots(self):
        f = lambda x: not x
        busy_list = self.reservation['busy'].tolist()
        return sum(map(f, busy_list))

    def issue_to_op(self, decode, spec):
        for i in range(len(self.op_unit)):
            if not self.op_unit[i].is_busy:
                self.op_unit[i].load_decode(decode, spec)
                break

    def execute(self, cpu):
            for i in range(len(self.op_unit)):
                if self.op_unit[i].is_loaded:
                    self.op_unit[i].execute(cpu)

    def retire_update(self, old, new):
            for i in range(len(self.op_unit)):
                if self.op_unit[i].is_loaded:
                    self.op_unit[i].retire_update(old, new)

    def flush(self):
        for row in range(self.size):
            if self.reservation['spec'].iloc[row]:
                self.reservation = self.reservation.drop(row).reset_index(
                    drop=True)
                self.reservation = self.reservation.append(
                    pd.DataFrame({'busy' : [False],
                                  'unit' : [None],
                                  'opcode' : [0x00],
                                  'dest' : [0x00],
                                  'op_1' : [None],
                                  'valid_1' : [False],
                                  'op_2' : [None],
                                  'valid_2' : [False],
                                  'offset' : [0x00],
                                  'spec' : False
                                }))
                self.reservation = self.reservation.reset_index(drop=True)
        for i in range(len(self.op_unit)):
            if self.op_unit[i].is_loaded and self.op_unit[i].is_speculative():
                self.op_unit[i].flush()

    def merge(self):
        self.reservation['spec'] = [False] * self.size
        for i in range(len(self.op_unit)):
            if self.op_unit[i].is_loaded and self.op_unit[i].is_speculative():
                self.op_unit[i].merge()
      
    def issue(self):
        for row in range(self.size):
            if self.is_all_op_unit_busy():
                break
            if self.reservation['busy'].iloc[row]:
                rs = self.reservation.iloc[row]
                if rs['valid_1'] and rs['valid_2']:
                    decode = self.rs_to_decode(rs)
                    spec = rs['spec']
                    self.reservation = self.reservation.drop(row).reset_index(
                        drop=True)
                    self.reservation = self.reservation.append(
                        pd.DataFrame({'busy' : [False],
                                      'unit' : [None],
                                      'opcode' : [0x00],
                                      'dest' : [0x00],
                                      'op_1' : [None],
                                      'valid_1' : [False],
                                      'op_2' : [None],
                                      'valid_2' : [False],
                                      'offset' : [0x00],
                                      'spec' : [False]
                                    }))
                    self.reservation = self.reservation.reset_index(drop=True)
                    self.issue_to_op(decode, spec)
                    break

    def add_instruction(self, decode, cpu, spec):
        if not self.is_free_space():
            raise Exception("Tried to add to instruction to RS when it is not\
                            free")
        for row in range(self.size):
            if not self.reservation['busy'].iloc[row]:
                self.reservation.iloc[row] = (self.decode_to_rs(decode, cpu) +
                                              [spec])
                break

    def add_instruction_test(self):
        if not self.is_free_space():
            raise Exception("Tried to add to instruction to RS when it is not\
                            free")
        for row in range(self.size):
            if not self.reservation['busy'].iloc[row]:
                self.reservation['busy'].iloc[row] = True
                break

    def decode_to_rs(self, decode, cpu):
        if decode[0] is "ALU":
            if type(decode[4]) is int:
                return [True, "ALU", decode[1], decode[2], decode[3],
                        cpu.get_valid(decode[3]), decode[4], True, 0]
            else:
                return [True, "ALU", decode[1], decode[2], decode[3],
                        cpu.get_valid(decode[3]), decode[4],
                        cpu.get_valid(decode[4]), 0]
        elif decode[0] is "DT":
            if decode[1] == 0 or decode[1] == 5 :
                return [True, "DT", decode[1], decode[2], decode[3],
                        cpu.get_valid(decode[3]), 0, True, 0]
            elif decode[1] == 0x1:
                return [True, "DT", decode[1], decode[2], decode[3],
                        True, 0, True, 0]
            elif decode[1] == 0x2 or decode[1] == 0x6:
                return [True, "DT", decode[1], 0, decode[2],
                        cpu.get_valid(decode[2]), decode[3],
                        cpu.get_valid(decode[3]), 0]
            elif decode[1] == 0x3:
                return [True, "DT", decode[1], 0, decode[2],
                        cpu.get_valid(decode[2]), decode[4],
                        cpu.get_valid(decode[4]), decode[3]]
            else:
                return [True, "DT", decode[1], decode[2], decode[4],
                        cpu.get_valid(decode[4]), 0, True, decode[3]]
        elif decode[0] == "CF":
            if decode[1] in range(0x4):
                return [True, "CF", decode[1], 0, decode[2], True, 0, True, 0]
            else:
                return [True, "CF", decode[1], 0, decode[2],
                        cpu.get_valid(decode[2]), decode[3], True, 0]

    def rs_to_decode(self, rs):
        if rs['unit'] is "ALU":
            return ["ALU", rs['opcode'], rs['dest'], rs['op_1'], rs['op_2']]
        elif rs['unit'] is "DT":
            if rs['opcode'] < 0x2 or rs['opcode'] == 5:
                return ["DT", rs['opcode'], rs['dest'], rs['op_1']]
            elif rs['opcode'] == 0x2 or rs['opcode'] == 0x6:
                return ["DT", rs['opcode'], rs['op_1'], rs['op_2']]
            elif rs['opcode'] == 0x3:
                return ["DT", rs['opcode'], rs['op_1'], rs['offset'], rs['op_2']]
            else:
                return ["DT", rs['opcode'], rs['dest'], rs['offset'], rs['op_1']]
        elif rs['unit'] is "CF":
            if rs['opcode'] in range(0x4):
                return ["CF", rs['opcode'], rs['op_1']]
            else:
                return ["CF", rs['opcode'], rs['op_1'], rs['op_2']]

    def sb_update(self, cpu):
        self.reservation['valid_1'] =  self.reservation['op_1'].apply(
            lambda x: cpu.get_valid(x) if str(x)[0] is "R" else False if x is
            None else True)
        self.reservation['valid_2'] = self.reservation['op_2'].apply(
            lambda x: cpu.get_valid(x) if str(x)[0] is "R" else False if x is
            None else True)

    def update_op(self, rob, reg):
        for row in range(self.size):
            if not self.reservation['busy'].iloc[row]:
                break
            if self.reservation['op_1'].iloc[row] == rob:
                self.reservation['op_1'].iloc[row] = reg
            if self.reservation['op_2'].iloc[row] == rob:
                self.reservation['op_2'].iloc[row] = reg
