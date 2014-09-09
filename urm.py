#!/usr/bin/env python3

from sys import argv

class SyntaxError(Exception): pass

class VerboseDict(dict):
    def __init__(self):
        super().__init__()
    def __setitem__(self, *args, **kwargs):
        super().__setitem__(*args, **kwargs)
        for k, v in self.items():
            print('%s: %s' % (k, v))
        print()

memory = VerboseDict()
source_filename = argv[1]
line_n = 0

# memory = VerboseDict()
# memory[1] = 'a'
# memory[2] = 'b'

def die(msg, code=0):
    print(msg)
    try:
        ret = memory[0]
        print(ret)
        exit(ret)
    except KeyError:
        exit(-1)

with open(source_filename, 'r') as source_file:
    for line in (l.strip() for l in source_file):
        if line == '.code':
            break
        if line == '.init':
            print('=== Initialization ===')
            line = source_file.readline().strip()
            while line and not line.startswith('#') and line != '.code':
                register, value = [int(w) for w in line.split()]
                print('%s <- %s' % (register, value))
                memory[register] = value
                line = source_file.readline().strip()

    print('=== Main program ===')
    source = [line for line in source_file.readlines()
                if line.strip() and not line.startswith('#') ]
    while line_n < len(source):
        expression = source[line_n].lstrip()
        command = expression[0].lower()
        print(' - %s - ' % line_n)
        try:
            if command == 'z':
                register = int(expression[2:])
                memory[register] = 0
                line_n += 1
            elif command == 's':
                register = int(expression[2:])
                memory[register] = memory[register] + 1 if register in memory else 1
                line_n += 1
            elif command == 't':
                r1, r2 = [int(r) for r in expression[2:].split()]
                # print('<%s> = %s -> <%s> = %s' % (r1, memory[r1], r2, memory[r2]))
                memory[r2] = memory[r1]
                line_n += 1
            elif command == 'j':
                r1, r2, n = [int(r) for r in expression[2:].split()]
                if memory[r1] == memory[r2]:
                    line_n = n
                else:
                    line_n += 1
            else:
                raise SyntaxError('unknown command %s, line %s' % (command, line_n))
        except KeyError:
            die('an uninitialized register has been referenced with %s' % expression)
    die('eof')
