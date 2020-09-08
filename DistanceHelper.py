import itertools

def get_atom_properties(filename):
    atom_dist = {}
    atom_connect = {}
    max_distances = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            info_list = line.split(' ')
            atom_dist[info_list[0]] = float(info_list[1])
            atom_connect[info_list[0]] = int(info_list[2])
        for atom1, atom2 in itertools.combinations_with_replacement(atom_dist.keys(), 2):
            atom_pair = frozenset([atom1, atom2])
            max_distances[atom_pair] = round((atom_dist[atom1] + atom_dist[atom2]) / 2, 2)
    return max_distances, atom_connect
