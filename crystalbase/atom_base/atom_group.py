import itertools
from collections import defaultdict

import numpy as np

from ..config import getAtomProperties


class Atom:
    def __init__(self, element, label, aindex, mass, x, y, z, intensity):
        """
        原子类
        :param element: 元素符号
        :param label: 晶体文件里的原子标签，如C001
        :param aindex: 原子序数，用于电子加权计算
        :param mass: 原子质量，用于质量加权计算
        :param x: 分数坐标
        :param y: 分数坐标
        :param z: 分数坐标
        :param intensity: RES中的强度
        """
        self.element = element
        self.label = label
        self.aindex = aindex
        self.mass = mass
        self.x = x
        self.y = y
        self.z = z
        self.intensity = intensity


class AtomGroup:
    class CellParameter:
        def __init__(self):
            """
            rotation_matrix: 用于换算分数坐标和绝对坐标的旋转矩阵
            """
            self.a = 1
            self.b = 1
            self.c = 1
            self.alpha = 90
            self.beta = 90
            self.gamma = 90
            self.rotation_matrix = None

        def coordinate_transform(self, x, y, z):
            """计算坐标转换结果"""
            if self.rotation_matrix is None:
                return x, y, z
            new_xyz = np.matmul(self.rotation_matrix, np.array([x, y, z]).T)
            new_xyz = new_xyz.T
            return np.round(new_xyz[0], 2), np.round(new_xyz[1], 2), np.round(new_xyz[2], 2)

        def set_parameter(self, a, b, c, alpha, beta, gamma):
            """设置晶胞参数"""
            self.a = a
            self.b = b
            self.c = c
            self.alpha = np.deg2rad(alpha)
            self.beta = np.deg2rad(beta)
            self.gamma = np.deg2rad(gamma)
            cosa = np.cos(self.alpha)
            cosb = np.cos(self.beta)
            cosg = np.cos(self.gamma)
            sing = np.sin(self.gamma)
            volume = 1 - cosa ** 2 - cosb ** 2 - cosg ** 2 + 2 * cosa * cosb * cosg
            # 计算旋转矩阵
            r = np.zeros((3, 3))
            r[0, 0] = a
            r[0, 1] = b * cosg
            r[0, 2] = c * cosb
            r[1, 1] = b * sing
            r[1, 2] = c * (cosa - cosb * cosg) / sing
            r[2, 2] = c * np.sqrt(volume) / sing
            self.rotation_matrix = r

    def __init__(self, name, multilayer=(False, False, False)):
        """初始化AtomGroup类成员"""
        self.name = name
        self.atom_index, self.atom_mass, self.max_distances, self.max_connect = getAtomProperties()
        self.cell_parameter = self.CellParameter()
        self.syms = []
        self.multilayer = multilayer
        self.atom_count = 0
        self.atom_dict = dict()
        self.connect_dict = defaultdict(int)
        self.bond_dict = dict()

    def set_parameter(self, a, b, c, alpha, beta, gamma):
        """设置晶胞参数"""
        self.cell_parameter.set_parameter(a, b, c, alpha, beta, gamma)

    def set_symmetry(self, syms):
        self.syms = syms

    def _syms_atom(self, x, y, z):
        """解析对称性，添加原子"""
        atoms = [(x, y, z)]
        if len(self.syms) == 0:
            return atoms
        for sym in self.syms:
            new_atoms = []
            for a in atoms:
                cord = {'X': a[0], 'Y': a[1], 'Z': a[2]}
                new_a = list(a)
                for i in range(3):
                    s = sym[i]
                    l_s = len(s)
                    if l_s == 1:  # 对称性类似X的情况
                        new_a[i] = cord[s]
                    elif l_s == 2:  # 对称性类似-X的情况
                        new_a[i] = -cord[s[-1]]
                    else:
                        for symbol in ['+', '-']:
                            if symbol in s:  # 对称性类似0.25+X的情况
                                scale, c = s.split(symbol)
                                try:
                                    scale = float(scale)
                                except ValueError:  # 对称性类似1/2+X的情况
                                    a, b = map(int, scale.split('/'))
                                    scale = a / b
                                new_a[i] = scale + (cord[c] if symbol == '+' else -cord[c])
                new_atoms.append(tuple(new_a))
            atoms.extend(new_atoms)
        return atoms

    def add_atom(self, element, index, x, y, z, intensity):
        """添加新原子"""
        xyz_list = self._syms_atom(x, y, z)
        for i in range(3):
            if self.multilayer[i]:
                temp_list = []
                for xyz in xyz_list:
                    new_xyz = list(xyz)
                    new_xyz[i] += 1
                    temp_list.append(tuple(new_xyz))
                xyz_list.extend(temp_list)

        for xyz in xyz_list:
            new_xyz = self.cell_parameter.coordinate_transform(*xyz)
            self.atom_dict[self.atom_count] = Atom(element, index, self.atom_index[element], self.atom_mass[element],
                                                   *new_xyz, intensity)
            self.atom_count += 1

    def distance_judge(self, atom1: Atom, atom2: Atom):
        """辅助函数，判断两原子距离是否满足max_distances"""
        dist = (atom2.x - atom1.x) ** 2 + (atom2.y - atom1.y) ** 2 + (atom2.z - atom1.z) ** 2
        atom_pair = frozenset([atom1.element, atom2.element])
        if dist <= self.max_distances[atom_pair] ** 2:
            return True, dist
        else:
            return False, dist

    def calc_neighbors(self):
        """计算原子键联关系"""
        for k1, k2 in itertools.combinations(self.atom_dict, 2):
            atom1 = self.atom_dict[k1]
            atom2 = self.atom_dict[k2]
            within, dist = self.distance_judge(atom1, atom2)
            if within:
                k = frozenset([k1, k2])
                self.bond_dict[k] = dist
                self.connect_dict[k1] += 1
                self.connect_dict[k2] += 1

    def remove_extra_connection(self):
        """移除连接数超限的键"""
        for k, atom in self.atom_dict.items():
            max_connect = self.max_connect[atom.element]
            if self.connect_dict[k] > max_connect:
                bonds = {b: d for b, d in self.bond_dict.items() if k in b}
                delete = sorted(bonds.items(), key=lambda s: s[1], reverse=False)[max_connect:]
                for b, d in delete:
                    self.bond_dict.pop(b)
            self.connect_dict[k] = max_connect
