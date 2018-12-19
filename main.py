import sys

from pipeline import *
from cpu import * 
from assembler.assembler import assembler 

if len(sys.argv) != 2:
    print("Use: python main.py file.asm")
else:
    instructions = assembler(sys.argv[1]) 
    fetch = fetch.fetch_unit()
    decode = decode.decode_unit()
    execute = execute.execute_unit()
    write_back = write_back.write_back()
    branch_predictor = branch_prediction.branch_predictor()
    cpu = cpu.cpu(instructions, branch_predictor, fetch, decode, execute, write_back)
    cpu.run_cycle()
