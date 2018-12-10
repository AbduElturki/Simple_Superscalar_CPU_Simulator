import time

from .memory import reg, rat, score_board
from .reorder_buffer import reorder_buffer
from collections import deque

class cpu(object):
    def __init__(self,  instruct, fetch_unit, decode_unit, execute_unit, write_back_unit):
        self.pc = 0x00

        self.reg = reg
        self.sb = score_board 
        self.rat = rat
        self.rob = reorder_buffer(64)
        self.WBR = {} 

        self.instruct_buffer = deque(maxlen=8)
        self.instruct_fork = {"sequential" : deque(maxlen=6),
                              "target"     : deque(maxlen=6)
                             }

        
        self.mem = ['00000000'] * 1024
        self.instruct_cache = deque(instruct)

        self.branch_predictor = branch_predictor
        self.fetch_unit = fetch_unit
        self.decode_unit = decode_unit
        self.execute_unit = execute_unit
        self.write_back_unit = write_back_unit

        self.running = False

    # Boolean

    def is_speculative(self):
        return self.branch_predictor.speculative
    
    # Memory access

    def get_dest(self, reg):
        if reg not in self.reg:
            raise Exception("get_dist: Register doesn't exist")
        return self.rat[reg]

    def new_dest(self, reg):
        self.rob.issue(reg, 00, False)
        self.rat[reg] = 'ROB' + str(self.rob.tail - 1).zfill(2)

    def set_valid(self, dest):
        if dest in self.reg:
            self.sb[dest] = True
        elif dest[:3] == "ROB":
            self.rob.rob['valid'].iloc[int(dest[-2:])] = True
        else:
            raise Exception("set_valid: dest doesn't exist")
        pass

    def get_valid(self, dest):
        if dest in self.reg:
            return self.sb[dest]
        elif dest[:3] == "ROB":
            location = int(dest[-2:])
            return self.rob.rob['valid'].iloc[location]
        else:
            raise Exception("get_valid: dest doesn't exist")
        pass

    def get_value(self, dest):
        if dest in self.reg:
            return self.reg[dest]
        elif dest[:3] == "ROB":
            return self.rob.rob['value'].iloc[int(dest[-2:])]
        else:
            raise Exception("get_value: dest doesn't exist " + dest[:3])

    # Memory update

    def update_reg(self, dest, update):
        if dest in self.reg:
            self.reg[dest] = update
        elif dest[:3] == "ROB":
            location = int(dest[-2:])
            self.rob.update_value(location, update)
        else:
            raise Exception("")

    def update_pc(self, dest):
        self.pc = dest

    def store(self, location, update):
       self.mem[location] = format(update, "x08") 

    def rob_retire(self):
        self.rob.retire(self)

    def pc_increment(self, step=1):
        self.pc += step

    # CPU stages

    def fetch(self):
        self.fetch_unit.fetch(self)

    def decode(self):
        self.decode_unit.decoder(self)

    def execute(self):
        self.execute_unit.execute(self)

    def update_rat(self, source, dest):
        self.rat[source] = dest

    def write_back(self):
        self.write_back_unit.write_back(self)

    def limited_run(self, cycles=2):
        print("Limited run of " + str(cycles) + " cycles")
        for i in range(cycles):
            self.fetch()
            self.decode()
            self.execute()
            self.write_back()
            time.sleep(1)
            print(self.reg, end='\n')

