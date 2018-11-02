from .memory import reg
from pprint import pprint

class cpu(object):
    def __init__(self, instruct, fetch_unit, decode_unit, execute_unit, write_back_unit):
        self.pc_next = 0x00
        self.reg = reg
        self.running = False
        self.mem = ['00000000'] * 1024
        self.mem[:len(instruct)] = instruct
        self.fetch = fetch_unit
        self.decode = decode_unit
        self.execute = execute_unit
        self.write_back = write_back_unit

    def limited_run(self, cycles=2):
        print("Limited run of " + str(cycles) + " cycles")
        for i in range(cycles):
            print("***********************")
            print("cycle: " + str(i))
            print("prior cycle")
            pprint(self.reg)
            self.fetch.fetch()
            cntr =  self.fetch.pc
            self.decode.decoder(self.mem[i], self.reg)
            print(self.decode.decode)
            self.execute.execute(self.decode.mode, self.decode.decode, self.reg, self.mem)
            self.write_back.write_back(self.decode.mode, self.decode.decode, self.execute.buf, self.reg)
            print("------------\nAfter cycle:")
            reg_next = dict(self.write_back.reg)
            pprint(reg_next)
            self.reg = dict(reg_next)

