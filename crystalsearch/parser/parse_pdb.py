from crystalsearch.Atom import AtomGroup


def parse_pdb(filename):
    """解析pdb文件中的晶胞信息"""
    cell = AtomGroup()
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
            cell.add_atom(element, element+index, x, y, z, 100)
    cell.calc_neighbors()
    cell.remove_extra_connection()
    return cell
