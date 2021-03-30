from crystalbase import Atom


def node_match(atom1: Atom, atom2: Atom):
    """节点匹配，原子质量之比0.7~1.4内为匹配"""
    ratio = atom1.mass / atom2.mass
    return 0.7 < ratio < 1.4


def edge_match(edge1, edge2):
    """默认edge无条件匹配"""
    return True if edge1 == edge2 else True
