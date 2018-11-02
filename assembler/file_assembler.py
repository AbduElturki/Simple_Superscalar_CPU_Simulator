from assembler import asm_to_machine
import sys

def main():
    if len(sys.argv) != 2:
        print("Use: python main.py file.asm")
    else:
        filename = sys.argv[1].replace(".asm",".hex")
        with open(sys.argv[1]) as f:
            assembly  = f.readlines()
            f.close()
        machine_code = asm_to_machine(assembly)
        f = open(filename,"w+")
        for line in machine_code:
            f.write(line+"\n")
        f.close()

if __name__ == "__main__":
    main()

