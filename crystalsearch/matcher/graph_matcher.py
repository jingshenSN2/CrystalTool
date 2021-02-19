import math

from networkx.algorithms import isomorphism

from crystalsearch import graph, matcher


def node_match(atom1, atom2):
    """节点匹配，原子质量之比0.7~1.4内为匹配"""
    ratio = atom1['mass'] / atom2['mass']
    return 0.7 < ratio < 1.4


def edge_match(edge1, edge2):
    """默认edge无条件匹配"""
    return True if edge1 == edge2 else True


def shrink_one(old_graph, keep_ring):
    """尝试删除graph的一个终端原子，返回删除后结果"""
    result = set()
    nodes = old_graph.nodes()
    degree = old_graph.degree()
    if keep_ring:
        nodes = [n for n in nodes if degree[n] == 1]
    for n in nodes:
        new_graph = old_graph.copy()
        new_graph.remove_node(n)
        result.add(new_graph)
    return result


def shrink(graph_set, keep_ring):
    """生成graph所有k个原子组成的子图"""
    subgraph_set = set()
    for g in graph_set:
        subgraph_set = subgraph_set.union(shrink_one(g, keep_ring))
    return subgraph_set


class GraphMatcher:
    class Result:
        """包装匹配结果类"""

        def __init__(self, is_matched, target, query, match_pairs):
            self.is_matched = is_matched
            self.match_pairs = match_pairs
            self.target = target
            self.query = query
            self.best_feature = [0, 0, 1000]
            self.results = []
            if self.is_matched:
                self.calculate_match_result()

        def calculate_match_result(self):
            feature_set = set()
            for p in self.match_pairs:
                n = len(p.keys())
                wr = sum([p[k].mass for k in p]) / sum([atom.mass for atom in self.query.g])
                ce = matcher.coordinate_error(p)
                if (n, wr, ce) in feature_set:
                    continue
                self.best_feature[0] = max(self.best_feature[0], n)
                self.best_feature[1] = max(self.best_feature[1], wr)
                self.best_feature[2] = min(self.best_feature[2], ce)
                self.results.append((p, n, wr, ce))

    def __init__(self, target: graph.Graph, query: graph.Graph, keep_ring=True, loss_atom=0.2, max_subgraph=1000):
        self.target = target
        self.query = query
        self.keep_ring = keep_ring
        self.loss_atom = loss_atom
        if isinstance(self.loss_atom, float):
            self.loss_atom = int(math.ceil(len(query.nodes()) * loss_atom))
        self.max_subgraph = max_subgraph

    def match(self):
        """完整匹配，依次匹配全部的删去k个原子的子图"""
        gm = isomorphism.GraphMatcher(self.target.g, self.query.g, node_match=node_match, edge_match=edge_match)
        if gm.subgraph_is_isomorphic():
            return self.Result(True, self.target, self.query, gm.subgraph_isomorphisms_iter())
        subgraph_set = shrink({self.query}, self.keep_ring)
        for i in range(min(self.loss_atom, len(self.query.nodes()))):
            if len(subgraph_set) > self.max_subgraph:
                break
            for sub in subgraph_set:
                gm = isomorphism.GraphMatcher(self.target.g, sub.g, node_match=node_match, edge_match=edge_match)
                if gm.subgraph_is_isomorphic():
                    return self.Result(True, self.target, self.query, gm.subgraph_isomorphisms_iter())
            subgraph_set = shrink(subgraph_set, self.keep_ring)
        return self.Result(False, self.target, self.query, None)
