from pipeline import *
from cpu import * 
#from assembler.assembler import assembler 

with open('assembler/alu_test_1.hex') as f:
    instructions = f.read().splitlines()
fetch = fetch.fetch_unit()
decode = decode.decode_unit()
execute = execute.execute_unit()
write_back = write_back.write_back()
branch_predictor = branch_prediction.branch_predictor()
cpu = cpu.cpu(instructions, branch_predictor, fetch, decode, execute, write_back)
cpu.run()
