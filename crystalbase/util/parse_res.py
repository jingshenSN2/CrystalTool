from ..atom_base import AtomGroup


def parseFromRES(filename: str, remove_extra=True):
    """解析res文件中的晶胞信息"""
    name = filename.split('/')[-1]
    cell = AtomGroup(name)
    with open(filename, 'r') as f:
        atom_dict = {}
        for line in f.readlines():
            line = line.rstrip('\n')
            s = line.split()
            if len(s) == 0:
                # 跳过空行
                continue
            if s[0] == 'CELL':
                # 晶胞参数所在行
                a, b, c, alpha, beta, gamma = map(float, s[2:])
                cell.set_parameter(a, b, c, alpha, beta, gamma)
            elif s[0] == 'SFAC':
                # 元素-编号所在行，例如SFAC C N O，之后的原子坐标中第2列就是用1,2,3来表示C,N,O
                for i in range(1, len(s)):
                    atom_dict[i] = s[i].capitalize()
            if len(s) <= 6 or not s[5].startswith('11.0000'):
                # 跳过无用信息
                continue
            else:
                # 读取原子信息、分数坐标行
                label = s[0]  # 晶胞中的原子编号
                x, y, z = map(float, s[2:5])  # 分数坐标
                intensity = -1  # 强度（可能没有）
                if len(s) == 8:
                    intensity = s[7]
                element = atom_dict[int(s[1])]  # 元素符号
                # print('add atom_base:', element, index, x, y, z, intensity)
                cell.add_atom(element, label, x, y, z, intensity)
    # 计算键联关系
    cell.calc_neighbors()
    if remove_extra:
        # 有时RES文件中CNO判断不准，不能按照元素移除多余的键
        cell.remove_extra_connection()
    return cell
