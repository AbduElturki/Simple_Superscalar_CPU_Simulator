import sys
import numpy as np
import matplotlib.pyplot as plt

from misc.lena import lena
from pipeline import *
from cpu import * 
from assembler.assembler import assembler 

instructions = assembler("benchmark_codes/conv.asm") 
fetch = fetch.fetch_unit()
decode = decode.decode_unit()
execute = execute.execute_unit()
write_back = write_back.write_back()
branch_predictor = branch_prediction.branch_predictor()
cpu = cpu.cpu(instructions, branch_predictor, fetch, decode, execute, write_back)
cpu.mem = lena()
cpu.mem += [0] * (2*len(cpu.mem))
cpu.mem[16500:16509] = [-1, -1, -1, -1, 8, -1, -1, -1, -1]
cpu.run()
result = cpu.mem[17000:20844]
im = np.reshape(result, (62,62))
plt.imshow(im, cmap='gray')
plt.show()
