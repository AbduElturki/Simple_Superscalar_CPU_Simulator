import re
import sys

from .table import opcode, register_aliases
from collections import defaultdict

def comment_sanitizer(asm):
    '''
    input: list of assembly code
    return: list of assembly code

    removes comments and white space in the list of assembly code
    '''
    asm = [line[0:line.find(';')].strip() for line in asm]
    return asm

def parse_operand(operand, labels):
    if operand.startswith("%"):
        label = operand.replace(",","")[1:]
        if label in labels:
           return labels[label]
        else:
            raise Exception("Nonexistent label: " + operand)
    elif operand.startswith("R") or operand.startswith("V"):
        if operand.replace(",","") in register_aliases:
            operand = register_aliases[operand]
            print(operand)
        print(operand)
        return int(re.search(r'\d+',operand).group()) #extract int from string
    elif operand.startswith("0x"):
        return int(operand, 16)
    else:
        return int(operand)
            
def asm_to_machine(asm):
    labels = defaultdict(int)
    machine_code = []
    addr = 0

    # First pass - labels
    for line in asm:
        if line.strip().startswith(";") or (len(line.strip()) == 0):
            continue
        if line.strip().endswith(":"):
            target_line = line.strip()
            label_name = target_line[:len(target_line)-1]
            location = addr
            labels[label_name] = location
            continue
        addr += 1

    # Second pass - opcodes
    for line in asm:
        if line.strip().startswith(";") or line.strip().endswith(':') or (len(line.strip()) is 0):
            continue
        instruct = line.replace(',','').split()
        if instruct[0] not in opcode:
            raise Exception("Line " + asm.index(line) + ", operation doesn't exist")

        op = [opcode[instruct[0]]] + [parse_operand(operand,labels) for operand in instruct[1:]]
        if len(op) is 2:
            output = format(op[0],'02x') + format(op[1],'06x')

        elif len(op) is 3:
            output = format(op[0],'02x') + format(op[1],'02x') + format(op[2],'04x')
        elif len(op) is 4:
            output = (format(op[0],'02x') + format(op[1],'02x') +
                      format(op[2],'02x') + format(op[3],'02x'))
        else:
            raise Exception("Error parsing line: " + line)
        machine_code.append(output)
    return machine_code

def assembler(assembly):
    with open(assembly) as f:
        assembly  = f.readlines()
        f.close()
    return asm_to_machine(assembly)

