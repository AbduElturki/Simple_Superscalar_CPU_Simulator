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

    def free_spaces(self):
        spaces = 0
        for unit in self.rs:
            spaces += self.rs[unit].free_slots()
        return spaces

    def sb_update(self, cpu):
        self.rs['ALU'].sb_update(cpu)
        self.rs['DT'].sb_update(cpu)
        self.rs['CT'].sb_update(cpu)

    def load(self, decode, cpu):
        if self.rs[decode[0]].can_bypass():
            self.rs[decode[0]].bypass(decode, cpu)
        else:
            self.rs[decode[0]].add_instruction(decode, cpu)
        if not self.free_spaces():
            cpu.stall()

    def execute(self, cpu):
        for unit in self.rs:
            if self.rs[unit].is_issuable():
                self.rs[unit].issue()
            self.rs[unit].execute(cpu)
        if self.free_spaces() and cpu.is_stalling():
            cpu.stall_reset()
        cpu.decode()

    def merge(self):
        self.rs['ALU'].merge()
        self.rs['DT'].merge()
        self.rs['CT'].merge()

    def flush(self):
        self.rs['ALU'].flush()
        self.rs['DT'].flush()
        self.rs['CT'].flush()
        

