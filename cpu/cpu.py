from .memory import reg, rat, score_board
from .reorder_buffer import reorder_buffer
from pprint import pprint

class cpu(object):
    def __init__(self, instruct, fetch_unit, decode_unit, execute_unit, write_back_unit):
        self.pc = 0x00

        self.reg = reg
        self.sb = score_board 
        self.rat = rat
        self.rob = reorder_buffer(64)
        self.instruct_reg = '00000000'
        self.MDR = 0x00
        self.MAR = 0x00
        self.WBR = 0x00
        
        self.mem = ['00000000'] * 1024
        self.mem[:len(instruct)] = instruct

        self.fetch_unit = fetch_unit
        self.decode_unit = decode_unit
        self.execute_unit = execute_unit
        self.write_back_unit = write_back_unit

        self.running = False

    def get_dest(self, reg):
        if reg not in self.reg:
            raise Exception("get_dist: Register doesn't exist")
        return self.rat[reg]

    def new_dest(self, reg):
        self.rob.issue(reg, 00, False)
        self.rat[reg] = 'ROB' + str(self.rob.tail - 1).zfill(2)

    def update_reg(self, dest, update):
        #if update is not int:
        #    raise Exception("Update isn't int")
        if dest in self.reg:
            self.reg[dest] = update
        elif test[:3] is "ROB":
            self.rob.rob['reg'].iloc[0]
        else:
            raise Exception("")

    def update_pc(self, dest):
        self.pc = dest

    def store(self, location, update):
       self.mem[location] = format(update, "x08") 

    def pc_increment(self):
        self.pc += 1

    def update_instruct_reg(self):
        self.instruct_reg = self.mem[self.pc]

    def fetch(self):
        self.fetch_unit.fetch(self)

    def decode(self):
        self.decode_unit.decoder(self)

    def execute(self):
        self.execute_unit.execute(self)

    def write_back(self):
        self.write_back_unit.write_back(self, self.execute_unit.link)

    def limited_run(self, cycles=2):
        print("Limited run of " + str(cycles) + " cycles")
        for i in range(cycles):
            print("***********************")
            print("cycle: " + str(i))
            print("prior cycle")
            self.fetch()
            self.decode()
            pprint(self.sb)
            self.execute()
            self.write_back()
            print("------------\nAfter cycle:")
            #reg_next = dict(self.write_back.reg)
            pprint(self.reg)
            #self.reg = dict(reg_next)

