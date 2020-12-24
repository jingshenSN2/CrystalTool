import itertools
import math
import os
import string
from hashlib import md5

from src.config import get_atom_properties


class Atom:
    def __init__(self, element, label, mass, x, y, z, intensity):
        """初始化类成员"""
        tmp = element + label + str(mass) + str(x) + str(y) + str(z) + str(intensity)
        self.uid = md5(tmp.encode('utf-8')).hexdigest()
        self.element = element
        self.label = label
        self.mass = mass
        self.x = x
        self.y = y
        self.z = z
        self.intensity = intensity
        self.connections = dict()


def square_distance(a, b, c, alpha, beta, gamma, dx, dy, dz):
    """辅助函数，计算晶胞中两原子的距离"""
    return a ** 2 * dx ** 2 + b ** 2 * dy ** 2 + c ** 2 * dz ** 2 + 2 * b * c * dy * dz * math.cos(
        alpha * math.pi / 180.0) \
           + 2 * a * c * dx * dz * math.cos(beta * math.pi / 180.0) + 2 * a * b * dx * dy * math.cos(
        gamma * math.pi / 180.0)


class Cell:
    """
    这里是晶胞类
    Attributes:
        a,b,c,alpha,beta,gamma: float,晶胞参数
        atom_list: list(Atom),原子列表
        atom_mass: 原子质量表
        max_distances: 原子最大距离表
        atom_connect: 原子最大连接数表
    """

    def __init__(self):
        """初始化类成员"""
        current_path = os.path.dirname(__file__)
        self.a = 1
        self.b = 1
        self.c = 1
        self.alpha = 90
        self.beta = 90
        self.gamma = 90
        self.atom_dict = dict()
        self.atom_mass, self.max_distances, self.max_connect = get_atom_properties(
            current_path + '/atom_properties.json')

    def set_lat_para(self, a, b, c, alpha, beta, gamma):
        """设置晶胞参数"""
        self.a = a
        self.b = b
        self.c = c
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def add_atom(self, element, index, x, y, z, intensity):
        """添加新原子"""
        atom = Atom(element, index, self.atom_mass[element], x, y, z, intensity)
        if atom.uid not in self.atom_dict.keys():
            self.atom_dict[atom.uid] = atom

    def distance_judge(self, atom1, atom2):
        """辅助函数，判断两原子距离是否满足max_distances"""
        dx = atom2.x - atom1.x
        dy = atom2.y - atom1.y
        dz = atom2.z - atom1.z
        dist = math.sqrt(square_distance(self.a, self.b, self.c, self.alpha, self.beta, self.gamma, dx, dy, dz))
        atom_pair = frozenset([atom1.element, atom2.element])
        if dist <= self.max_distances[atom_pair]:
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
                atom1.connections[k2] = dist
                atom2.connections[k1] = dist

    def remove_extra_connection(self):
        """移除连接数超限的键"""
        for uid in self.atom_dict:
            atom = self.atom_dict[uid]
            d = atom.connections
            if len(d.keys()) > self.max_connect[atom.element]:
                out_ranges = sorted(d.items(), key=lambda s: s[1], reverse=False)[self.max_connect[atom.element]:]
                for other, dist in out_ranges:
                    atom.connections.pop(other)
                    self.atom_dict[other].connections.pop(uid)


def parse_res(filename, remove_extra=True):
    """解析res文件中的晶胞信息"""
    flag = False
    cell = Cell()
    with open(filename, 'r') as f:
        atom_dict = {}
        for line in f.readlines():
            line = line.rstrip('\n')
            s = line.split()
            if len(s) == 0:
                continue
            if s[0] == 'CELL':
                a, b, c, alpha, beta, gamma = map(float, s[2:])
                cell.set_lat_para(a, b, c, alpha, beta, gamma)
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


def parse_pdb(filename):
    """解析pdb文件中的晶胞信息"""
    cell = Cell()
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
            # print('add atom:', element, index, x, y, z)
            cell.add_atom(element, element+index, x, y, z, 100)
    cell.calc_neighbors()
    cell.remove_extra_connection()
    return cell


def to_res(input_filename, output_filename, match_result):
    """储存Cell类到res文件, 测试版"""
    element_map = {}
    for atom1, atom2 in match_result.items():
        elename = atom1.element + atom1.index
        element_map[elename] = atom2.element
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
                elename = tmp[0]
                if elename in element_map:
                    tmp[0] = element_map[elename]
                else:
                    tmp[0] = 'H'
                tmp[1] = str(index_map[tmp[0]])
                line = ' '.join(tmp) + '\n'
            output.write(line)
