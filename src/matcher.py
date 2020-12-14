import itertools
import math
import random

import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher


class Result:
    def __init__(self, is_matched, matcher, match_iters):
        self.is_matched = is_matched
        self.match_iters = match_iters
        self.match_number = 0
        self.match_ratio = 0
        self.match_weighted_ratio = 0
        if is_matched:
            for r in match_iters:
                wr = sum([atom.mass for atom in r]) / sum([atom.mass for atom in matcher])
                if wr > self.match_weighted_ratio:
                    self.match_weighted_ratio = wr
                    self.best_match = r
            self.match_number = len(self.best_match.keys())
            self.match_ratio = self.match_number / len(matcher)

    def to_string(self):
        return 'match_number=%d match_ratio=%.3f match_weighted_ratio=%.3f' % (
        self.match_number, self.match_ratio, self.match_weighted_ratio)


def node_match(atom1, atom2):
    """节点匹配，原子质量之比0.8~1.2内为匹配"""
    ratio = atom1['mass'] / atom2['mass']
    return 0.8 < ratio < 1.2


def edge_match(edge1, edge2):
    """默认edge无条件匹配"""
    return True


def shrink_one(graph):
    """尝试删除graph的一个终端原子，返回删除后结果"""
    new_graph = nx.Graph(graph)
    degree = new_graph.degree
    flag = False
    d1_nodes = [node for node in new_graph.nodes() if degree[node] == 1]
    if len(d1_nodes) > 0:
        remove_index = random.randint(0, len(d1_nodes) - 1)
        new_graph.remove_node(d1_nodes[remove_index])
        flag = True
    return flag, new_graph


def gen_k(graph, k):
    """生成graph所有k个原子组成的子图"""
    sub_graphs = set()
    new_graph = nx.Graph(graph)
    for atom_combine in itertools.combinations(new_graph.nodes, k):
        sub = new_graph.subgraph(atom_combine)
        sub_graphs.add(sub)
    return sub_graphs


def check_subgraph(target, sub):
    """检查target是否包含于sub"""
    if not nx.is_connected(sub):
        return False
    gm = GraphMatcher(target, sub, node_match=node_match,
                      edge_match=edge_match)
    if gm.subgraph_is_isomorphic():
        return gm


def match_1(target, query, loss_atom=0.2):
    """快速匹配，每次随机删去原子后匹配"""
    if isinstance(loss_atom, float):
        loss_atom = int(math.ceil(len(query.nodes) * loss_atom))
    query_copy = query
    for i in range(min(loss_atom, len(query.nodes)) + 1):
        gm = GraphMatcher(target, query_copy, node_match=node_match,
                          edge_match=edge_match)
        if gm.subgraph_is_isomorphic():
            return Result(True, query, gm.subgraph_isomorphisms_iter())
        flag, query_copy = shrink_one(query_copy)
    return Result(False, None, None)


def match_2(target, query, loss_atom=0.2):
    """完整匹配，依次匹配全部的删去k个原子的子图"""
    if isinstance(loss_atom, float):
        loss_atom = int(math.ceil(len(query.nodes) * loss_atom))
    for i in range(min(loss_atom, len(query.nodes)) + 1):
        subgraphs = gen_k(query, len(query.nodes) - i)
        for sub in subgraphs:
            res = check_subgraph(target, sub)
            if res:
                return Result(True, query, res.subgraph_isomorphisms_iter())
    return Result(False, None, None)
