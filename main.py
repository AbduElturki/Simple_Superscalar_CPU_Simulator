from pipeline import *
from cpu import * 
#from assembler.assembler import assembler 


instructions = ["11010020", "1102002f", "01030102"]
fetch = fetch.fetch_unit()
decode = decode.decode_unit()
execute = execute.execute_unit()
write_back = write_back.write_back()
cpu = cpu.cpu(instructions, fetch, decode, execute, write_back)
print(cpu.mem[:10])
cpu.limited_run()
