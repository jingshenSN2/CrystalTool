from ..matcher import Result


def saveToRes(output_file: str, match_result: Result, match_pair: dict):
    """
    根据匹配映射另存新的RES文件
    :param output_file: 输出文件名
    :param match_result: 匹配结果，用于读取RES结构
    :param match_pair: 匹配映射，用于修改RES的原子类型
    :return:
    """
    elements = set()
    # 读取所有的元素类型
    for q_atom in match_pair.values():
        elements.add(q_atom.element)
    elements = list(elements)
    elements.append('H')  # 加上氢
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
                # 匹配上的原子，将元素类型改为PDB中的类型
                a_ele = match_pair[atom].element
            else:
                # 未匹配上原子，改成氢
                a_ele = 'H'
            ele_count[a_ele] += 1
            ele_index = ele_dict[a_ele]
            name = '%s%d' % (a_ele, ele_count[a_ele])
            f.write('%s %d %.4f %.4f %.4f 11.00000 0.0\n' % (name, ele_index, atom.x / 10, atom.y / 10, atom.z / 10))
        f.write('HKLF 4\n')
        f.write('END\n')
