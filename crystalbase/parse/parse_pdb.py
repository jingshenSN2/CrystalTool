from ..atom_base import AtomGroup


def parse_from_pdb(filename: str):
    """解析pdb文件中的晶胞信息"""
    name = filename.split('/')[-1]
    cell = AtomGroup(name)
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.rstrip('\n')
            tmp = line.split()
            if len(tmp) < 8:
                # 跳过标题等信息
                continue
            if line.startswith('CONECT'):
                # 读取完分数坐标，之后的键联关系不需要读取，自己计算
                break
            # 读取原子信息、分数坐标行
            element = tmp[-1].capitalize()
            if element == 'H':
                # 忽略氢
                continue
            index = tmp[1]  # 晶胞中的原子编号
            x, y, z = map(float, tmp[-6:-3])  # 分数坐标
            cell.add_atom(element, element + index, x, y, z, 100)
    # 计算键联关系
    cell.calc_neighbors()
    cell.remove_extra_connection()
    return cell
