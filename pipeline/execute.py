from .operation_units import *

class execute_unit(object):
    def __init__(self):
        self.busy = False
        self.alu_unit = alu.alu_logic()
        self.data_transfer_unit = data_transfer.data_transfer()
        self.control_flow_unit = control_flow.control_flow()
        self.buf = 0
        self.decode = None 
        self.link = False

    def execute(self, cpu):
        self.decode = cpu.decode_unit.decode
        if self.decode[0] is "ALU":
            self.alu_unit.execute(cpu, self.decode)
        elif self.decode[0] is "DT":
            self.data_transfer_unit.execute(self.decode, cpu)
        elif self.decode[0] is "CF": 
            self.control_flow_unit.execute(self.decode, cpu)
