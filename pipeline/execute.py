from .operation_units import *
from reservation_station import reservation_station

class execute_unit(object):
    def __init__(self):
        self.busy = False
        self.rs = {"ALU" : reservation_station([alu()] * 4, 16),
                   "RS"  : reservation_station([data_transfer()] * 2, 6)
                  }

    def execute(self, cpu):
        pass
