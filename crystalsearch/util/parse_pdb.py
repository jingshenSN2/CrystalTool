from crystalsearch.atom_base import AtomGroup


def parseFromPDB(filename: str):
    """解析pdb文件中的晶胞信息"""
    name = filename.split('/')[-1]
    cell = AtomGroup(name)
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.rstrip('\n')
            tmp = line.split()
            if len(tmp) < 8:
                continue
            if line.startswith('CONECT'):
                break
            element = tmp[-1].capitalize()
            if element == 'H':
                continue
            index = tmp[1]
            x, y, z = map(float, tmp[-6:-3])
            cell.add_atom(element, element + index, x, y, z, 100)
    cell.calc_neighbors()
    cell.remove_extra_connection()
    return cell
