import re

from ..atom_base import AtomGroup


def parse_from_res(filename: str, multilayer=(False, False, False), remove_extra=True):
    """解析res文件中的晶胞信息"""
    name = filename.split('/')[-1]
    cell = AtomGroup(name, multilayer)
    syms = []
    atom_dict = {}

    res = open(filename, 'r')
    res_lines = res.readlines()
    res.close()
    length = len(res_lines)
    index = 0
    #  读取shelxt求解评分
    for i in range(length):
        line = res_lines[i].rstrip('\n')
        if line.startswith('REM SHELXT'):
            line = line.rstrip('\n')
            pattern = re.compile('R1 (\\d+\\.\\d+), Rweak (\\d+\\.\\d+), Alpha (\\d+\\.\\d+)')
            match = re.search(pattern, line)
            if match:
                r1, rweak, al = map(float, match.groups())
                cell.set_shelxt_score(r1, rweak, al)
                index = i + 1
                break

    #  读取晶胞参数
    for i in range(index, length):
        line = res_lines[i].rstrip('\n')
        if line.startswith('CELL'):
            line = line.rstrip('\n')
            s = line.split()
            a, b, c, alpha, beta, gamma = map(float, s[2:])
            cell.set_parameter(a, b, c, alpha, beta, gamma)
            index = i + 1
            break

    #  读取对称性信息
    for i in range(index, length):
        line = res_lines[i].rstrip('\n')
        if line.startswith('SYMM'):
            line = line.replace('SYMM', '').replace(' ', '')
            sym = tuple(line.split(','))
            syms.append(sym)
    cell.set_symmetry(syms)

    #  读取元素信息
    for i in range(index, length):
        line = res_lines[i].rstrip('\n')
        if line.startswith('SFAC'):
            s = line.split()
            for e in range(1, len(s)):
                atom_dict[e] = s[e].capitalize()  # 统一大写
            index = i + 1
            break

    #  读取元素坐标信息
    for i in range(index, length):
        line = res_lines[i].rstrip('\n')
        s = line.split()
        if len(s) <= 6 or not s[5].startswith('11.0000'):
            continue
        else:
            label = s[0]
            x, y, z = map(float, s[2:5])
            intensity = -1
            if len(s) == 8:
                intensity = s[7]
            element = atom_dict[int(s[1])]
            cell.add_atom(element, label, x, y, z, intensity)
    cell.calc_neighbors()
    if remove_extra:
        # 有时RES文件中CNO判断不准，不能按照元素移除多余的键
        cell.remove_extra_connection()
    return cell
