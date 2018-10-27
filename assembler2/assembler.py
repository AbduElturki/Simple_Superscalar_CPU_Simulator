"""
 MIPS Fields

 
 < R-type >
  31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0
 +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
 |    op(6bits)    |   rs(5bits)  |   rt(5bits)  |   rd(5bits)  | shamt(5bits) |   fucnt(6bits)  |
 +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
 
 
 < I-type >
  31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0
 +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
 |    op(6bits)    |   rs(5bits)  |   rt(5bits)  |         constant or address (16bits)          |
 +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
 
 < J-type >
  31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0
 +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
 |    op(6bits)    |                            address (30bits)                                 |
 +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
 
"""

import re

type_r = ['addu', 'and', 'jr', 'nor', 'or', 'sltu', 'sll', 'srl', 'subu']

type_r_fucnt = {'addu' : 33,
               'and'  : 36,
               'jr'   : 8,
               'nor'  : 39,
               'or'   : 37,
               'sltu' : 43,
               'sll'  : 0,
               'srl'  : 2,
               'subu' : 35
              }

type_i = ['addiu', 'andi', 'beq', 'bne', 'lui', "lb", "lw", "la", "ori", "sltiu", "sb", "sw"]

type_i_opcode = {'addiu' : 9,
                 'andi'  : 12,
                 'beq'   : 4,
                 'bne'   : 5,
                 'lui'   : 15,
                 'lb'    : 32,
                 'lw'    : 35,
                 'la'    : 15,
                 'ori'   : 13,
                 'sltiu' : 11,
                 'sw'    : 43,
                 'sb'    : 40
                }

type_j = ['jal', 'j']

type_j_opcode = {'jal' : 3,
                 'j'   : 2
                }

def get_bin(dec, lenght=32):
    return format(dec, 'b').zfill(lenght)

def make_r_type(op, rs, rt, rd, shamt, funct):
    return get_bin(((op << 26) | (rs << 21) | (rt << 16) | (rd << 11) | (shamt << 6) | funct))

def make_i_type(op, rs, rt, addr):
    return get_bin((op << 26) | (rs << 21) | (rt << 16) | (addr & 65535))

def make_j_type(op, addr):
    return get_bin((op << 26) | addr)

def reg_to_int(reg):
    reg = reg.lstrip('$')
    return int(reg.replace(',',''))

def imm_to_int(imm):
    return int(imm.replace(',',''),0)

def label_to_int_addr(labels, label_name):
    for label in labels:
        if label.name == label_name:
            return label.location
    raise Exception('Label' + label_name +'\'s location not found')

def assemble_line(line,instruct_index=0, labels=None):
    instruction = line.split()
    print(instruction) 
    #Type-R
    if instruction[0] in type_r:
        if instruction[0] is "jr":
            return make_r_type(0, reg_to_int(instruction[1]), 0, 0, 0, type_r_fucnt[instruction[0]])
        elif instruction[0] is "sll":
            return make_r_type(0,0, reg_to_int(instruction[2]), reg_to_int(instruction[1]), imm_to_int(instruction[3]), type_r_fucnt[instruction[0]])
        elif instruction[0] is 'srl':
            return make_r_type(0,0,reg_to_int(instruction[2]), reg_to_int(instruction[1]), imm_to_int(instruction[3]))
        elif instruction[0] in ["addu", "and", "nor", "or", "sltu", "subu"]:
            return make_r_type(0, reg_to_int(instruction[2]), reg_to_int(instruction[3]), reg_to_int(instruction[1]), 0, type_r_fucnt[instruction[0]])
        else:
            raise Exception('assemble_line tried to create machine code for "' + instruction[0] + '",but the instruction\'s make_r_type state doesn\'t exist')

    # Type-I
    elif instruction[0] in type_i:
        if instruction[0] in ['addiu', 'andi', 'ori', "sltiu"]:
            return make_i_type(type_i_opcode[instruction[0]], reg_to_int(instruction[2]), reg_to_int(instruction[1]), imm_to_int(instruction[3]))
        elif instruction[0] in ["beq", "bne"]:
            if labels == None:
                raise Exception(instruction[0] + " was called. No labels were loaded")
            relative_address = int( label_to_int_addr(labels,instruction[3]) - (0x400000 +(instruct_index*4) + 4))
            return make_i_type(type_i_opcode[instruction[0]], reg_to_int(instruction[1]), reg_to_int(instruction[2]), relative_address/4)
        elif instruction[0] is "lui":
            return make_i_type(type_i_opcode[instruction[0]], 0, reg_to_int(instruction[1]), imm_to_int(instruction[2]))
        elif instruction[0] in ["lw", "lb", "sw", "sb"]:
            instruct_2_split = re.split('\(|\)', instruction[2])
            offset = instruct_2_split[0]
            rs = instruct_2_split[1]
            return make_i_type(type_i_opcode[instruction[0]],reg_to_int(rs), reg_to_int(instruction[1]), imm_to_int(offset))
        elif instruction[0] is "la":
            if labels == None:
                raise Exception(instruction[0] + " was called. No labels were loaded")
            location = label_to_int_addr(labels,instruction[2])
            if ((location & 65535) == 0):
                return make_i_type(15,0,reg_to_int(instruction[1]),(location >> 16))
            else:
                return (make_i_type(15,0,reg_to_int(instruction[1]),(location >> 16))+ "\n" + make_i_type(13, reg_to_int(instruction(instruction[1]), reg_to_int(instruction[1]), (location & 65535))))
        else:
            raise Exception('assemble_line tried to create machine code for "' + instruction[0] + '",but the instruction\'s make_i_type state doesn\'t exist')

    # Type-J
    elif instruction[0] in type_j:
        if instruction[0] is "j":
            if labels == None:
                raise Exception(instruction[0] + " was called. No labels were loaded")
            return make_j_type(type_j_opcode[instruction[0]],(label_to_int_addr(instruction[1],labels) >> 2))
        elif instruction[0] == "jal":
            return make_j_type(type_j_opcode[instruction[0]], reg_to_int(instruction[1]))
        else:
            raise Exception('assemble_line tried to create machine code for "' + instruction[0] + '",but the instruction\'s make_j_type state doesn\'t exist')
    else:
        raise Exception(instruction[0] + " Doesn't exist")

                                                      
                                                      
