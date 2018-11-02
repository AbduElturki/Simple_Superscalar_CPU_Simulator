from pipeline import *
from cpu import cpu
from assembler import assembler 


def main():
    instructions = assembler()
    fetch = fetch.fetch_unit()
    decode = decode.decode_unit()
    execute = execute.execute_unit()
    write_back = write_back()


