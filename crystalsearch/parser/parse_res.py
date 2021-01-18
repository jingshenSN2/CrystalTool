from crystalsearch.Atom import AtomGroup


def parse_res(filename, remove_extra=True):
    """解析res文件中的晶胞信息"""
    cell = AtomGroup()
    with open(filename, 'r') as f:
        atom_dict = {}
        for line in f.readlines():
            line = line.rstrip('\n')
            s = line.split()
            if len(s) == 0:
                continue
            if s[0] == 'CELL':
                a, b, c, alpha, beta, gamma = map(float, s[2:])
                cell.set_parameter(a, b, c, alpha, beta, gamma)
            elif s[0] == 'SFAC':
                for i in range(1, len(s)):
                    atom_dict[i] = s[i].capitalize()
            if len(s) <= 6 or not s[5].startswith('11.0000'):
                continue
            else:
                label = s[0]
                x, y, z = map(float, s[2:5])
                intensity = -1
                if len(s) == 8:
                    intensity = s[7]
                element = atom_dict[int(s[1])]
                # print('add atom:', element, index, x, y, z, intensity)
                cell.add_atom(element, label, x, y, z, intensity)
    cell.calc_neighbors()
    if remove_extra:
        cell.remove_extra_connection()
    return cell
