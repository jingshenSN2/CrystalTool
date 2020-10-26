import itertools
import math
import os
import string


class Atom:
    def __init__(self, element, index, mass, x, y, z, intensity):
        self.element = element
        self.index = index
        self.mass = mass
        self.x = x
        self.y = y
        self.z = z
        self.intensity = intensity
        self.neighbors = {}

    def add_neighbor(self, atom, distance):
        self.neighbors[atom] = distance

    def remove_neighbor(self, atom):
        del self.neighbors[atom]


current_path = os.path.dirname(__file__)


def get_atom_properties(filename):
    atom_mass = {}
    atom_dist = {}
    atom_connect = {}
    max_distances = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue
            info_list = line.split(' ')
            element = info_list[0]
            atom_mass[element] = float(info_list[1])
            atom_dist[element] = float(info_list[2])
            atom_connect[element] = int(info_list[3])
        for atom1, atom2 in itertools.combinations_with_replacement(atom_dist.keys(), 2):
            atom_pair = frozenset([atom1, atom2])
            max_distances[atom_pair] = round(atom_dist[atom1] + atom_dist[atom2], 2)
    return atom_mass, max_distances, atom_connect


def square_distance(a, b, c, alpha, beta, gamma, dx, dy, dz):
    return a ** 2 * dx ** 2 + b ** 2 * dy ** 2 + c ** 2 * dz ** 2 + 2 * b * c * dy * dz * math.cos(
        alpha * math.pi / 180.0) \
           + 2 * a * c * dx * dz * math.cos(beta * math.pi / 180.0) + 2 * a * b * dx * dy * math.cos(
        gamma * math.pi / 180.0)


class Cell:
    def __init__(self):
        self.a = 0
        self.b = 0
        self.c = 0
        self.alpha = 0
        self.beta = 0
        self.gamma = 0
        self.atom_list = []
        self.atom_mass, self.max_distances, self.max_connect = get_atom_properties(
            current_path + '/atom_properties.txt')

    def set_lat_para(self, a, b, c, alpha, beta, gamma):
        self.a = a
        self.b = b
        self.c = c
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def add_atom(self, element, index, x, y, z, intensity):
        self.atom_list.append(Atom(element, index, self.atom_mass[element], x, y, z, intensity))

    def distance_judge(self, atom1, atom2):
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
        for atom1, atom2 in itertools.combinations(self.atom_list, 2):
            within, dist = self.distance_judge(atom1, atom2)
            if within:
                atom1.add_neighbor(atom2, dist)
                atom2.add_neighbor(atom1, dist)
        for atom in self.atom_list:
            dic = atom.neighbors
            if len(dic.keys()) > self.max_connect[atom.element]:
                outranges = sorted(dic.items(), key=lambda dic: dic[1], reverse=False)[self.max_connect[atom.element]:]
                for other, dist in outranges:
                    atom.remove_neighbor(other)
                    other.remove_neighbor(atom)


def parse_res(filename):
    flag = False
    cell = Cell()
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.rstrip('\n')
            if line.startswith('CELL'):  # 读取晶胞参数
                line = line.lstrip('CELL ')
                _, a, b, c, alpha, beta, gamma = map(float, line.split())
                # print('cell parameters:', a, b, c, alpha, beta, gamma)
                cell.set_lat_para(a, b, c, alpha, beta, gamma)
            if line.startswith('MOLE'):  # 准备读取分数坐标部分
                flag = not flag
                continue
            if flag:
                tmp = line.split()
                element = tmp[0].rstrip(string.digits)  # 元素符号和序号分离
                index = tmp[0].lstrip(string.ascii_letters)
                x, y, z = map(float, tmp[2:5])
                intensity = -1
                if len(tmp) == 8:
                    intensity = tmp[7]
                # print('add atom:', element, index, x, y, z, intensity)
                cell.add_atom(element, index, x, y, z, intensity)
    cell.calc_neighbors()
    return cell


def parse_pdb(filename):
    cell = Cell()
    cell.set_lat_para(1, 1, 1, 90, 90, 90)
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.rstrip('\n')
            tmp = line.split()
            if len(tmp) < 8:
                continue
            if line.startswith('CONECT'):
                break
            element = tmp[-1]
            if element == 'H':
                continue
            index = tmp[1]
            x, y, z = map(float, tmp[-6:-3])
            # print('add atom:', element, index, x, y, z)
            cell.add_atom(element, index, x, y, z, 100)
    cell.calc_neighbors()
    return cell


def to_res(input_filename, output_filename, match_result):
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





