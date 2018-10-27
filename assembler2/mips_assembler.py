import sys

from assembler import assemble_line

def usage():
    print 'Usage: '+sys.argv[0]+' -i <file1>'
    sys.exit(1)

def main(argv):
    files = argv

    if len(files) is not 1:
        usage()
    for filename in files:
        with open(filename) as f:
            asm = f.readlines()
        asm = [x.strip() for x in content]


