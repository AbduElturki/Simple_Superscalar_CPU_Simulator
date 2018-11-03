import re
import sys

from .table import opcode, register_aliases

class label(object):
    def __init__(self, name, location):
        self.name = name
        self.location = location

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
        for label in labels:
            if operand.replace(",","") == label.name:
                return label.location
        raise Exception("Nonexistent label: " + operand)
    elif operand.startswith("R"):
        if operand.replace(",","") in register_aliases:
            operand = register_aliases[operand]
        return int(re.search(r'\d+',operand).group()) #extract int from string
    elif operand.startswith("0x"):
        return int(operand, 16)
    else:
        return int(operand)
            
def asm_to_machine(asm):
    label_list = []
    machine_code = []
    addr = 0

    #iasm = comment_sanitizer(asm)

    # First pass - labels
    for line in asm:
        if line.strip().startswith(";") or (len(line.strip()) == 0):
            continue
        if line.strip().endswith(":"):
            target_line = line.strip()
            label_name = target_line[:len(target_line)-1]
            location = addr
            print(addr)
            new_label = label(label_name, location)
            label_list.append(new_label)
            continue
        addr += 1

    # Second pass - opcodes
    for line in asm:
        op = []
        if line.strip().startswith(";") or line.strip().endswith(':') or (len(line.strip()) is 0):
            continue
        instruct = line.replace(',','').split()
        if instruct[0] not in opcode:
            raise Exception("Line " + asm.index(line) + ", operation doesn't exist")
        op.append(opcode[instruct[0]])

        for operand in instruct[1:]:
            op.append(parse_operand(operand,label_list))
        if len(op) > 4 or len(op) < 3:
            raise Exception("Error parsing line: " + line)

        if len(op) is 3:
            output = format(op[0],'02x') + format(op[1],'02x') + format(op[2],'04x')
        else:
            output = format(op[0],'02x') + format(op[1],'02x') + format(op[2],'02x') + format(op[3],'02x')
        machine_code.append(output)
    return machine_code

def assembler(assembly):
    with open(assembly) as f:
        assembly  = f.readlines()
        f.close()
    return asm_to_machine(assembly)

