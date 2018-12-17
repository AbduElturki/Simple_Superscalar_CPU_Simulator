import time

from .memory import reg, rat, score_board
from .reorder_buffer import reorder_buffer
from collections import defaultdict, deque

class cpu(object):
    def __init__(self,  instruct, branch_predictor, fetch_unit, decode_unit, execute_unit, write_back_unit):
        self.pc = 0
        self.cycle = 0

        self.reg = reg
        self.sb = score_board 
        self.rat = rat.copy()
        self.his_rat = rat.copy()
        self.rob = reorder_buffer(64)
        self.retire_his = {}
        self.WBR = {} 
        self.WBR_spec = {}

        self.instruct_buffer = deque(maxlen=8)
        self.instruct_fork = {"sequential" : deque(maxlen=8),
                              "target"     : deque(maxlen=8)
                             }

        
        self.spec_mem = {} 
        self.mem = [0] * 1024
        self.mem[:8] = [102, 1, 4, 68, 6, 3, 9, 8]
        self.instruct_cache = instruct

        self.branch_predictor = branch_predictor
        self.fetch_unit = fetch_unit
        self.decode_unit = decode_unit
        self.execute_unit = execute_unit
        self.write_back_unit = write_back_unit
        
        self.stall_count = 0
        self.instruct_per_cycle = defaultdict(int)
        self.branching = 0
        self.correct_branching = 0

        self.is_seq = False
        self.stalling = False
        self.running = False

    # Boolean

    def is_unit_free(self, unit):
        return self.execute_unit.is_free_space(unit)

    def is_stalling(self):
        return self.stalling

    def is_speculative(self):
        return self.fetch_unit.speculative

    def is_spec_forward(self):
        return self.fetch_unit.is_forward

    def speculate(self, forward):
        self.is_seq = not self.branch_predictor.to_take(forward)
        #self.speculate_mode = True

    def stall(self):
        self.stalling = True
        self.stall_count += 1

    def stall_reset(self):
        self.stalling = False
    
    def speculate_mode(self):
        if self.is_seq:
            return "sequential"
        else:
            return "target"

    def update_branch_pred(self, taken, forward):
        self.branch_predictor.update(forward, taken)

    def commit_fork(self, spec):
        if spec in self.instruct_fork:
            self.instruct_buffer = self.instruct_fork[spec].copy()
        else:
            raise Exception(spec + "doesn't exist")
        self.instruct_fork = {"sequential" : deque(maxlen=8),
                              "target"     : deque(maxlen=8)
                             }

    def spec_merge(self):
        self.execute_unit.merge()
        self.rob.merge()
        self.fetch_unit.merge(self)
        self.fetch_unit.reset()
        self.his_rat = self.rat.copy()
        for addr in self.spec_mem:
            self.mem[addr] = self.spec_mem[addr]
        self.spec_mem = {} 
        

    def spec_flush(self):
        self.rat = self.his_rat.copy()
        self.execute_unit.flush()
        self.fetch_unit.flush(self)
        self.rob.flush()
        self.fetch_unit.reset()
        self.spec_mem = defaultdict(int)

    def load_to_rs(self, decode, spec):
        self.execute_unit.load(decode, self, spec)

    # Memory access

    def get_dest(self, reg):
        if reg not in self.reg:
            raise Exception("get_dist: " + reg + " Register doesn't exist")
        return self.rat[reg]

    def new_dest(self, reg, spec):
        if reg in self.reg:
            self.rob.issue(reg, 00, False, spec)
            location = self.rob.tail - 1 if self.rob.tail else self.rob.size - 1
            self.rat[reg] = 'ROB' + str(location).zfill(2)
        else:
            raise Exception(reg + ": is not a register")

    def set_valid(self, dest):
        if dest in self.reg:
            self.sb[dest] = True
        elif dest[:3] == "ROB":
            self.rob.rob['valid'].iloc[int(dest[-2:])] = True
        else:
            raise Exception("set_valid: dest doesn't exist")
        pass

    def get_valid(self, dest):
        if isinstance(dest, int):
            raise Exception("get_valid: " + str(dest) + "is int")
        elif dest in self.reg:
            return self.sb[dest]
        elif dest[:3] == "ROB":
            location = int(dest[-2:])
            if self.rob.rob['reg'].iloc[location]  is None:
                raise Exception(dest + ": doesn't exist")
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

    def store(self, location, update):
       self.mem[location] = format(update, "x08") 

    def rs_update_dest(self, rob, reg):
        self.execute_unit.update_rs_dest(rob, reg)

    def rob_retire(self):
        if not self.rob.is_empty():
            self.rob.retire(self)

    def retire_update(self, old, new):
        self.execute_unit.retire_update(old,new)

    def pc_increment(self, step=1):
        self.pc += step

    # CPU stages

    def fetch(self):
        if not (self.pc == len(self.instruct_cache)):
            self.fetch_unit.fetch(self)

    def decode(self):
        self.decode_unit.decoder(self)
        if not self.is_stalling() and len(self.instruct_buffer) == 8:
            self.stall()
        elif self.is_stalling() and not len(self.instruct_buffer) == 8:
            self.stall_reset()

    def execute(self):
        self.execute_unit.execute(self)

    def update_rat(self, source, dest):
        self.rat[source] = dest

    def write_back(self):
        self.write_back_unit.write_back(self)

    def is_running(self):
        if (self.pc == len(self.instruct_cache) and self.rob.is_empty() and 
            len(self.instruct_buffer) == 0):
            return False
        else:
            return True

    def print_status(self):
        sum_instruct = sum(self.instruct_per_cycle.values())
        ipc = sum_instruct/(self.cycle)
        percentage = (100 if not self.branching else
                      self.correct_branching/self.branching * 100.00)
        print("IPC: " + str(ipc))
        print("Prediction Accuracy: " + str(percentage) + "%")
    
    def print_reg(self):
        print("--------------------------")
        print("| REG |  Value   | SB    |")
        print("|-----+----------+-------|")
        for reg in self.reg:
            border = "  |" if self.sb[reg] else " |"
            seperator = "  | " if len(reg) == 2 else " | "
            print("| " + reg + seperator + str(self.reg[reg]).zfill(8) +
                  " | " + str(self.sb[reg]) + border)
        print("---------------------------\n")

    def run(self):
        while self.is_running():
            print("Cycle: " + str(self.cycle))
            print("PC: " + str(self.pc))
            print("Stalling: " + str(self.is_stalling()))
            print("Branching: " + str(self.is_speculative()))
            print("Spec mode: " + self.speculate_mode())
            print()
            self.write_back()
            self.execute()
            self.decode()
            self.fetch()
            self.cycle += 1
            self.print_reg()
            print()
            print(self.instruct_buffer)
            print(self.instruct_fork['sequential'])
            print(self.instruct_fork['target'])
            print("*******************************\n")
            print(self.mem[:10])
        #    time.sleep(2)
        self.print_status()
        print(self.mem[:10])

    def run_cycle(self):
        con = True
        while self.is_running() and con:
            print("Cycle: " + str(self.cycle))
            print("PC: " + str(self.pc))
            print("Stalling: " + str(self.is_stalling()))
            print("Branching: " + str(self.is_speculative()))
            print("Spec mode: " + self.speculate_mode())
            print()
            self.write_back()
            self.execute()
            self.decode()
            self.fetch()
            self.cycle += 1
            self.print_reg()
            print()
            print("Instruction Buffer")
            print(self.instruct_buffer)
            print("Instruction Fork Sequential")
            print(self.instruct_fork['sequential'])
            print("Instruction Fork Target")
            print(self.instruct_fork['target'])
            print()
            self.execute_unit.print_rs()
            self.rob.print_rob()
            print("*******************************\n")
            print(self.mem[:10])
            inp = input('Continue?')
            con = False if inp is "n" else True
        self.print_status()
        print(self.mem[:10])

    def limited_run(self, cycles=2):
        print("Limited run of " + str(cycles) + " cycles")
        for i in range(cycles):
            self.write_back()
            self.execute()
            self.decode()
            self.fetch()
            time.sleep(1)
            print(self.reg, end='\n')

