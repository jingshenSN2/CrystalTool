import itertools

import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher


def node_match(atom1, atom2):
    return abs(atom1['mass'] - atom2['mass']) <= 3


def edge_match(edge1, edge2):
    return True


def shrink_one(graph):
    newgraph = nx.Graph(graph)
    degree = newgraph.degree
    flag = False
    for node in newgraph.nodes():
        if degree[node] == 1:
            newgraph.remove_node(node)
            flag = True
            break
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


class MatchRater:
    def __init__(self, target, query):
        self.target = target
        self.query = query
        self.result = None

    def match_1(self):
        query = self.query
        gm = GraphMatcher(self.target, query, node_match=node_match,
                          edge_match=edge_match)
        while not gm.subgraph_is_isomorphic():
            flag, query = shrink_one(query)
            if not flag:
                print('匹配失败')
                return False
            gm = GraphMatcher(self.target, query, node_match=node_match,
                              edge_match=edge_match)
        return gm.subgraph_isomorphisms_iter()

    def match_2(self, loss_atom):
        result = None
        for i in range(loss_atom + 1):
            subgraphs = gen_k(self.query, len(self.query.nodes) - i)
            for sub in subgraphs:
                res = check_subgraph(self.target, sub)
                if res:
                    result = res
            if result is not None:
                break
        if result is None:
            print('匹配失败')
            return False
        return result.subgraph_isomorphisms_iter()
