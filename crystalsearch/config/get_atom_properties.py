import itertools
import json
import os


def get_atom_properties():
    """获取原子信息配置文件"""
    current_path = os.path.dirname(__file__)
    filename = current_path + '/atom_properties.json'
    atom_mass = {}
    atom_dist = {}
    atom_connect = {}
    max_distances = {}
    with open(filename, 'r') as f:
        data = json.load(f)
        for atom in data:
            info = data[atom]
            atom_mass[atom] = info['atom_mass']
            atom_dist[atom] = info['atom_radius']
            atom_connect[atom] = info['max_connection']
        for atom1, atom2 in itertools.combinations_with_replacement(atom_dist.keys(), 2):
            atom_pair = frozenset([atom1, atom2])
            max_distances[atom_pair] = round(1.2 * (atom_dist[atom1] + atom_dist[atom2]), 2)
    return atom_mass, max_distances, atom_connect
