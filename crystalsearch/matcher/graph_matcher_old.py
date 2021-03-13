import math

from networkx.algorithms import isomorphism

from crystalsearch import graph, matcher


def shrink_one(old_graph):
    """尝试删除graph的一个终端原子，返回删除后结果"""
    result = set()
    nodes = old_graph.nodes()
    for n in nodes:
        new_graph = old_graph.copy()
        new_graph.remove_node(n)
        result.add(new_graph)
    return result


def shrink(graph_set):
    """生成graph所有k个原子组成的子图"""
    subgraph_dict = {}
    for g in graph_set:
        new_set = shrink_one(g)
        for sub in new_set:
            if sub not in subgraph_dict:
                subgraph_dict[sub] = 0
    return subgraph_dict


class GraphMatcherOld:

    def __init__(self, target: graph.Graph, query: graph.Graph, loss_atom=0.2):
        self.target = target
        self.query = query
        self.loss_atom = loss_atom
        if isinstance(self.loss_atom, float):
            self.loss_atom = int(math.ceil(len(query.nodes()) * loss_atom))
        self.node_match = matcher.node_match_old
        self.edge_match = matcher.edge_match

    def get_result(self):
        """完整匹配，依次匹配全部的删去k个原子的子图"""
        gm = isomorphism.GraphMatcher(self.target.g, self.query.g, node_match=self.node_match, edge_match=self.edge_match)
        if gm.subgraph_is_isomorphic():
            return matcher.Result(True, self.target, self.query, gm.subgraph_isomorphisms_iter())
        subgraph_dict = shrink({self.query})
        for i in range(min(self.loss_atom, len(self.query.nodes()))):
            if len(subgraph_dict) > 2000:
                break
            for sub in subgraph_dict:
                if subgraph_dict[sub] == 1:
                    return
                subgraph_dict[sub] = 1
                gm = isomorphism.GraphMatcher(self.target.g, sub.g, node_match=self.node_match, edge_match=self.edge_match)
                if gm.subgraph_is_isomorphic():
                    return matcher.Result(True, self.target, self.query, gm.subgraph_isomorphisms_iter())
            subgraph_dict = shrink(subgraph_dict)
        return matcher.Result(False, self.target, self.query, None)