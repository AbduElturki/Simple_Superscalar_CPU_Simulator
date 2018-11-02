from memory import reg

class cpu(object):
    def __init__(self, instruct, fetch_unit, decode_unit, execute_unit, write_back_unit):
        self.pc = 0x00
        self.pc_next = 0x00
        self.reg = reg
        self.reg_next = reg
        self.running = False
        self.mem = ['00000000'] * 1024
        self.mem[:len(instruct)] = instruct
        self.fetch = fetch_unit
        self.decode = fetch_unit
        self.execute = execute_unit
        self.write_back = write_back_unit

