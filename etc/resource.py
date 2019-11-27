#encoding: utf-8

import os

if __name__ == '__main__':
    fhandler = os.popen('top -n 1 -b')
    lines = fhandler.readlines()
    cpu_line = lines[2]

    cpu_line = cpu_line.split()[1]

    cpu = float(cpu_line[:cpu_line.find('%')])

    mem_line = lines[3]
    mem = mem_line.split()
    
    # mem = 100 * float(mem[3][:-1]) / float(mem[1][:-1])
    mem = round(100*(float(mem[7])/float(mem[3])),2)
    print(cpu)
    print(mem)

    fhandler.close()