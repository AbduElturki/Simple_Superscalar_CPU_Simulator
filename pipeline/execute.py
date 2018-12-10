from .operation_units import *
from reservation_station import reservation_station

class execute_unit(object):
    def __init__(self):
        self.busy = False
        self.rs = {"ALU" : reservation_station([alu()] * 4, 16),
                   "DT"  : reservation_station([data_transfer()] * 2, 6),
                   "CT"  : reservation_station([control_flow()] * 2, 6)
                  }

    def is_free_space(self, unit):
        return self.rs[unit].is_free_space()

    def sb_update(self, cpu):
        self.rs['ALU'].sb_update(cpu)
        self.rs['DT'].sb_update(cpu)
        self.rs['CT'].sb_update(cpu)

    def load(self, decode, cpu):
        if self.rs[decode[0]].can_bypass():
            self.rs[decode[0]].bypass(decode, cpu)
        else:
            self.rs[decode[0]].add_instruction(decode, cpu)

    def execute(self, cpu):
        for unit in self.rs:
            if self.rs[unit].is_issuable():
                self.rs[unit].issue()
            self.rs[unit].execute(cpu)
