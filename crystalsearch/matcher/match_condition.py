def node_match_old(atom1, atom2):
    """旧节点匹配函数，原子质量之比0.7~1.4内为匹配"""
    ratio = atom1['mass'] / atom2['mass']
    return 0.7 < ratio < 1.4


def node_match(atom1, atom2):
    """节点匹配，原子质量之比0.7~1.4内为匹配"""
    ratio = atom1.mass / atom2.mass
    return 0.7 < ratio < 1.4


def edge_match(edge1, edge2):
    """默认edge无条件匹配"""
    return True if edge1 == edge2 else True
