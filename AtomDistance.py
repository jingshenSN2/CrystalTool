import itertools


class AtomDistanceHelper:
    def __init__(self, filename):
        self.atom_info = {}
        self.max_distances = {}
        with open(filename, 'r') as f:
            for line in f.readlines():
                info_list = line.split(' ')
                self.atom_info[info_list[0]] = info_list[1]
            for atom1, atom2 in itertools.combinations(self.atom_info.keys(), 2):
                atom_pair = frozenset([atom1, atom2])
                self.max_distances[atom_pair] = round(float(self.atom_info[atom1]) + float(self.atom_info[atom2]), 2)
