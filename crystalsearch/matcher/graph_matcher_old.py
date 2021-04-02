from ..graph import Graph
from .graph_matcher_vf2 import GraphMatcherVF2
from .match_result import Result


def shrink_one(old_graph: Graph):
    """尝试删除graph的一个终端原子，返回删除后结果"""
    result = set()
    nodes = old_graph.nodes()
    for nd in nodes:
        new_graph = old_graph.copy()
        new_graph.remove_node(nd)
        result.add(new_graph)
    return result


def shrink(graph_dict: dict):
    """生成graph所有k个原子组成的子图"""
    subgraph_dict = {}
    for g in graph_dict:
        new_set = shrink_one(g)
        for sub in new_set:
            if sub not in subgraph_dict:
                subgraph_dict[sub] = 0
    return subgraph_dict


class GraphMatcherOld:

    def __init__(self, target: Graph, query: Graph, loss_atom: int):
        self.target = target
        self.query = query
        self.loss_atom = loss_atom

    def get_result(self, threshold):
        """完整匹配，依次匹配全部的删去k个原子的子图"""
        gm = GraphMatcherVF2(self.target, self.query)
        ret = gm.get_result(threshold)
        if ret.is_matched:
            return ret
        subgraph_dict = shrink({self.query: 1})
        for i in range(min(self.loss_atom, len(self.query.nodes()))):
            if len(subgraph_dict) > 2000:
                break
            for sub in subgraph_dict:
                if subgraph_dict[sub] == 1:
                    return
                subgraph_dict[sub] = 1
                gm = GraphMatcherVF2(self.target, sub)
                ret = gm.get_result(threshold)
                if ret.is_matched:
                    ret.calculate_match_result(self.query)
                    return ret
            subgraph_dict = shrink(subgraph_dict)
        return Result(False, self.target, self.query, [], {})
