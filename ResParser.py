import string

import numpy as np

from Cell import Cell


def parse_res(filename):
    flag = False
    cell = Cell()
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.strip('\n')
            if line.startswith('CELL'):
                line = line.strip('CELL ')
                _, a, b, c, alpha, beta, gamma = map(float, line.split())
                print('cell parameters:', a, b, c, alpha, beta, gamma)
                cell.set_lat_para(a, b, c, alpha, beta, gamma)
            if line.startswith('MOLE'):
                flag = not flag
                continue
            if flag:
                tmp = line.split()
                elename = tmp[0].strip(string.digits)
                x, y, z = map(float, tmp[2:5])
                intensity = -1
                if len(tmp) == 8:
                    intensity = tmp[7]
                print('add atom:', elename, x, y, z, intensity)
                cell.add_atom(elename, np.array([x, y, z]), intensity)
    return cell


cell = parse_res('c21.res')

print(1)
