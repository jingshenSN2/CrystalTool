import string

from cell.Cell import Cell


def parse_res(filename):
    flag = False
    cell = Cell()
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.strip('\n')
            if line.startswith('CELL'):  # 读取晶胞参数
                line = line.strip('CELL ')
                _, a, b, c, alpha, beta, gamma = map(float, line.split())
                #print('cell parameters:', a, b, c, alpha, beta, gamma)
                cell.set_lat_para(a, b, c, alpha, beta, gamma)
            if line.startswith('MOLE'):  # 准备读取分数坐标部分
                flag = not flag
                continue
            if flag:
                tmp = line.split()
                element = tmp[0].strip(string.digits)  # 元素符号和序号分离
                index = tmp[0].strip(string.ascii_letters)
                x, y, z = map(float, tmp[2:5])
                intensity = -1
                if len(tmp) == 8:
                    intensity = tmp[7]
                #print('add atom:', element, index, x, y, z, intensity)
                cell.add_atom(element, index, x, y, z, intensity)
    return cell

def parse_pdb(filename):
    cell = Cell()
    with open(filename, 'r') as f:
        for line in f.readlines()[2:]:
            line = line.strip('\n')
            cell.set_lat_para(1, 1, 1, 90, 90, 90)
            tmp = line.split()
            if line.startswith('CONECT') or len(tmp) < 8:
                break
            element = tmp[-1]
            if element == 'H':
                continue
            index = tmp[1]
            x, y, z = map(float, tmp[-6:-3])
            #print('add atom:', element, index, x, y, z, intensity)
            cell.add_atom(element, index, x, y, z, 100)
    return cell