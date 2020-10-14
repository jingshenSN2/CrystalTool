import itertools
import random
import math
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher


def node_match(atom1, atom2):
    ratio = atom1['mass'] / atom2['mass']
    return 0.8 < ratio < 1.2


def edge_match(edge1, edge2):
    return True


def shrink_one(graph):
    newgraph = nx.Graph(graph)
    degree = newgraph.degree
    flag = False
    d1_nodes = [node for node in newgraph.nodes() if degree[node] == 1]
    if len(d1_nodes) > 0:
        remove_index = random.randint(0, len(d1_nodes)-1)
        newgraph.remove_node(d1_nodes[remove_index])
        flag = True
    return flag, newgraph


def gen_k(graph, k):
    subgraphs = set()
    newgraph = nx.Graph(graph)
    for atom_combine in itertools.combinations(newgraph.nodes, k):
        sub = newgraph.subgraph(atom_combine)
        subgraphs.add(sub)
    return subgraphs


def check_subgraph(target, sub):
    if not nx.is_connected(sub):
        return False
    gm = GraphMatcher(target, sub, node_match=node_match,
                      edge_match=edge_match)
    if gm.subgraph_is_isomorphic():
        return gm


def match_1(target, query, loss_atom):
    query_copy = query
    for i in range(min(loss_atom, len(query.nodes)) + 1):
        gm = GraphMatcher(target, query_copy, node_match=node_match,
                          edge_match=edge_match)
        if gm.subgraph_is_isomorphic():
            return gm.subgraph_isomorphisms_iter()
        flag, query_copy = shrink_one(query_copy)
    print('匹配失败')
    return False


def match_2(target, query, loss_atom):
    for i in range(min(loss_atom, len(query.nodes)) + 1):
        subgraphs = gen_k(query, len(query.nodes) - i)
        for sub in subgraphs:
            res = check_subgraph(target, sub)
            if res:
                return res.subgraph_isomorphisms_iter()
    print('匹配失败')
    return False


def rmsd(match_result):
    res = 0.0
    for atom1 in match_result.keys():
        for neighbor in atom1.neighbors:
            if neighbor in match_result.keys():
                d1 = atom1.neighbors[neighbor]
                d2 = match_result[atom1].neighbors[match_result[neighbor]]
                res += (d1 - d2) ** 2
    return math.sqrt(res/2)

