import itertools

def gen_max_distances(filename):
    atom_info = {}
    max_distances = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            info_list = line.split(' ')
            atom_info[info_list[0]] = info_list[1]
        for atom1, atom2 in itertools.combinations_with_replacement(atom_info.keys(), 2):
            atom_pair = frozenset([atom1, atom2])
            max_distances[atom_pair] = round((float(atom_info[atom1]) + float(atom_info[atom2])) / 2, 2)
    return max_distances
