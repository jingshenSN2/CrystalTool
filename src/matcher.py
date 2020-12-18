import math
import networkx.algorithms.isomorphism as nxis


def node_match(atom1, atom2):
    """节点匹配，原子质量之比0.8~1.2内为匹配"""
    ratio = atom1['mass'] / atom2['mass']
    return 0.8 < ratio < 1.2


def edge_match(edge1, edge2):
    """默认edge无条件匹配"""
    return True


def shrink_one(graph, keep_ring):
    """尝试删除graph的一个终端原子，返回删除后结果"""
    result = set()
    nodes = graph.nodes()
    degree = graph.degree()
    if keep_ring:
        nodes = [n for n in nodes if degree[n] == 1]
    for n in nodes:
        new_graph = graph.copy()
        new_graph.remove_node(n)
        result.add(new_graph)
    return result


def shrink(graph_set, keep_ring):
    """生成graph所有k个原子组成的子图"""
    subgraph_set = set()
    for graph in graph_set:
        subgraph_set = subgraph_set.union(shrink_one(graph, keep_ring))
    return subgraph_set


class GraphMatcher:
    class Result:
        """包装匹配结果类"""
        def __init__(self, is_matched, matcher, match_iters):
            self.is_matched = is_matched
            self.match_iters = match_iters
            self.match_number = 0
            self.match_ratio = 0
            self.match_weighted_ratio = 0
            if is_matched:
                for r in match_iters:
                    wr = sum([r[k].mass for k in r]) / sum([atom.mass for atom in matcher])
                    if wr > self.match_weighted_ratio:
                        self.match_weighted_ratio = wr
                        self.best_match = r
                self.match_number = len(self.best_match.keys())
                self.match_ratio = self.match_number / len(matcher)

        def to_string(self):
            return 'match_number=%d match_ratio=%.3f match_weighted_ratio=%.3f' % (
                self.match_number, self.match_ratio, self.match_weighted_ratio)

    def __init__(self, target, query, keep_ring, loss_atom=0.2):
        self.target = target
        self.query = query
        self.keep_ring = keep_ring
        self.loss_atom = loss_atom
        if isinstance(self.loss_atom, float):
            self.loss_atom = int(math.ceil(len(query.nodes()) * loss_atom))

    def match(self):
        """完整匹配，依次匹配全部的删去k个原子的子图"""
        gm = nxis.GraphMatcher(self.target.g, self.query.g, node_match=node_match, edge_match=edge_match)
        if gm.subgraph_is_isomorphic():
            print('matched without shrink')
            return self.Result(True, self.query.g, gm.subgraph_isomorphisms_iter())
        subgraph_set = shrink({self.query}, self.keep_ring)
        for i in range(min(self.loss_atom, len(self.query.nodes()))):
            for sub in subgraph_set:
                gm = nxis.GraphMatcher(self.target.g, sub.g, node_match=node_match, edge_match=edge_match)
                if gm.subgraph_is_isomorphic():
                    return self.Result(True, self.query.g, gm.subgraph_isomorphisms_iter())
            subgraph_set = shrink(subgraph_set, self.keep_ring)
        return self.Result(False, None, None)






