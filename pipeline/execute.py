from .operation_units import *
from .reservation_station import reservation_station

class execute_unit(object):
    def __init__(self):
        self.busy = False
        self.rs = {"ALU" : reservation_station([alu.alu_logic()] * 4, 16),
                   "DT"  : reservation_station([data_transfer.data_transfer()] * 2, 6),
                   "CF"  : reservation_station([control_flow.control_flow()] * 2, 6)
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
        self.rs['CF'].sb_update(cpu)

    def load(self, decode, cpu, spec):
        if self.rs[decode[0]].can_bypass(decode, cpu):
            self.rs[decode[0]].bypass(decode, cpu, spec)
        else:
            self.rs[decode[0]].add_instruction(decode, cpu, spec)
        if not self.free_spaces():
            cpu.stall()

    def retire_update(self, old, new):
        self.rs['ALU'].retire_update(old, new)
        self.rs['DT'].retire_update(old, new)
        self.rs['CF'].retire_update(old, new)

    def update_rs_dest(self, rob, reg):
        self.rs['ALU'].update_op(rob, reg)
        self.rs['DT'].update_op(rob, reg)
        self.rs['CF'].update_op(rob, reg)

    def execute(self, cpu):
        self.sb_update(cpu)
        for unit in self.rs:
            if self.rs[unit].is_issuable():
                self.rs[unit].issue()
            self.rs[unit].execute(cpu)
        if self.free_spaces() and cpu.is_stalling():
            cpu.stall_reset()

    def merge(self):
        self.rs['ALU'].merge()
        self.rs['DT'].merge()
        self.rs['CF'].merge()

    def flush(self):
        self.rs['ALU'].flush()
        self.rs['DT'].flush()
        self.rs['CF'].flush()
        

