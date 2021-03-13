from crystalsearch import matcher


def to_res_old(input_filename, output_filename, match_result):
    """储存Cell类到res文件, 测试版"""
    element_map = {}
    for atom1, atom2 in match_result.items():
        element_name = atom1.element + atom1.index
        element_map[element_name] = atom2.element
    with open(input_filename, 'r') as inp, open(output_filename, 'w+') as output:
        counter = 0
        index_map = {}
        for line in inp.readlines():
            if line.startswith('SFAC'):
                tmp = line.split()
                for i in range(1, len(tmp)):
                    index_map[tmp[i]] = i
            if line.startswith('MOLE'):
                counter = counter + 1
            elif counter == 1:
                tmp = line.split()
                element_name = tmp[0]
                if element_name in element_map:
                    tmp[0] = element_map[element_name]
                else:
                    tmp[0] = 'H'
                tmp[1] = str(index_map[tmp[0]])
                line = ' '.join(tmp) + '\n'
            output.write(line)


def to_res(output_file: str, match_result: matcher.Result, match_pair: dict):
    elements = set()
    for q_atom in match_pair.values():
        elements.add(q_atom.element)
    elements = list(elements)
    elements.append('H')
    ele_dict = {elements[i]: i + 1 for i in range(len(elements))}
    ele_count = {elements[i]: 0 for i in range(len(elements))}
    with open(output_file, 'w') as f:
        # ATTENTION: 需要扩大晶胞边长为10埃，否则用Vesta打开时可能崩溃
        f.write('CELL 0 10.0000 10.0000 10.0000 90.000 90.000 90.000\n')
        f.write('LATT -1\n')
        f.write('SFAC %s\n' % ' '.join(elements))
        t_atoms = match_result.target.nodes()
        for atom in t_atoms:
            if atom in match_pair:
                a_ele = match_pair[atom].element
            else:
                a_ele = 'H'
            ele_count[a_ele] += 1
            ele_index = ele_dict[a_ele]
            name = '%s%d' % (a_ele, ele_count[a_ele])
            f.write('%s %d %.4f %.4f %.4f 11.00000 0.0\n' % (name, ele_index, atom.x / 10, atom.y / 10, atom.z / 10))
        f.write('HKLF 4\n')
        f.write('END\n')
