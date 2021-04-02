from ..graph import Graph
from .match_condition import node_match
from .match_result import Result


def calculate_prob(g1: Graph, g2: Graph):
    """计算匹配概率"""
    pf = {}
    for u in g2.nodes():
        pl, pd = 0, 0
        d = g2.degree(u)
        for v in g1.nodes():
            if node_match(u, v):
                pl += 1
            if g1.degree(v) >= d:
                pd += 1
        pf[u] = pl * pd
    return pf


def generate_node_order(pf: dict):
    """根据匹配概率排序，概率大的节点靠前"""
    seq = sorted(pf.keys(), key=pf.__getitem__, reverse=True)
    return {seq[i]: i for i in range(len(seq))}


class GraphMatcherVF2:

    def __init__(self, G1: Graph, G2: Graph, loss_atom=0):
        self.G1 = G1
        self.G2 = G2
        self.G1_nodes = set(self.G1.nodes())
        self.G2_nodes = set(self.G2.nodes())
        self.stop_len = len(G2) - loss_atom

        self.core_1 = {}
        self.core_2 = {}
        self.inout_1 = {}
        self.inout_2 = {}

        pf = calculate_prob(self.G1, self.G2)
        self.G2_order = generate_node_order(pf)
        self.state = State(self)
        self.mappings = []

    def get_result(self, threshold):
        """获取匹配结果，Result类"""
        is_matched, iso_iter = self.subgraph_isomorphisms_iter()
        return Result(is_matched, self.G1, self.G2, iso_iter, threshold)

    def match(self):
        """递归匹配函数"""
        if len(self.core_2) >= self.stop_len:
            self.mappings.append(self.core_1.copy())
            if len(self.core_2) == len(self.G2):
                return
        for u, v in self.candidate_pairs_iter():
            if self.syntactic_feasibility(u, v):
                if self.semantic_feasibility(u, v):
                    s = State(self, u, v)
                    self.match()
                    s.restore()

    def candidate_pairs_iter(self):
        """根据VF2规则，生成可能的匹配对"""
        G1_nodes = self.G1_nodes
        G2_nodes = self.G2_nodes
        min_key = self.G2_order.__getitem__

        T1 = [node for node in self.inout_1 if node not in self.core_1]
        T2 = [node for node in self.inout_2 if node not in self.core_2]

        if T1 and T2:
            node_2 = min(T2, key=min_key)
            for node_1 in T1:
                yield node_1, node_2
        else:
            other_node = min(G2_nodes - set(self.core_2), key=min_key)
            for node in G1_nodes:
                if node not in self.core_1:
                    yield node, other_node

    def syntactic_feasibility(self, G1_node, G2_node):
        return node_match(G1_node, G2_node)

    def semantic_feasibility(self, G1_node, G2_node):
        """根据VF2规则，剪枝"""
        if self.G1.degree(G1_node) < self.G2.degree(G2_node):
            return False
        for neighbor in self.G1[G1_node]:
            if neighbor in self.core_1:
                if not (self.core_1[neighbor] in self.G2[G2_node]):
                    return False
                elif self.G1.number_of_edges(neighbor, G1_node) != \
                        self.G2.number_of_edges(self.core_1[neighbor], G2_node):
                    return False
        for neighbor in self.G2[G2_node]:
            if neighbor in self.core_2:
                if not (self.core_2[neighbor] in self.G1[G1_node]):
                    return False
                elif self.G1.number_of_edges(self.core_2[neighbor], G1_node) != \
                        self.G2.number_of_edges(neighbor, G2_node):
                    return False
        num1 = 0
        for neighbor in self.G1[G1_node]:
            if (neighbor in self.inout_1) and (neighbor not in self.core_1):
                num1 += 1
        num2 = 0
        for neighbor in self.G2[G2_node]:
            if (neighbor in self.inout_2) and (neighbor not in self.core_2):
                num2 += 1
        if num1 < num2:
            return False

        num1 = 0
        for neighbor in self.G1[G1_node]:
            if neighbor not in self.inout_1:
                num1 += 1
        num2 = 0
        for neighbor in self.G2[G2_node]:
            if neighbor not in self.inout_2:
                num2 += 1
        if not (num1 >= num2):
            return False
        return True

    def subgraph_isomorphisms_iter(self):
        """返回匹配是否成功和所有的匹配映射"""
        self.mappings = []
        self.match()
        return len(self.mappings) > 0, self.mappings


class State:
    """Networkx的VF2-State实现"""

    def __init__(self, GM: GraphMatcherVF2, G1_node=None, G2_node=None):
        self.GM = GM

        self.G1_node = None
        self.G2_node = None
        self.depth = len(GM.core_1)

        if G1_node is None or G2_node is None:
            GM.core_1 = {}
            GM.core_2 = {}
            GM.inout_1 = {}
            GM.inout_2 = {}

        if G1_node is not None and G2_node is not None:
            GM.core_1[G1_node] = G2_node
            GM.core_2[G2_node] = G1_node

            self.G1_node = G1_node
            self.G2_node = G2_node

            self.depth = len(GM.core_1)

            if G1_node not in GM.inout_1:
                GM.inout_1[G1_node] = self.depth
            if G2_node not in GM.inout_2:
                GM.inout_2[G2_node] = self.depth

            new_nodes = set()
            for node in GM.core_1:
                new_nodes.update([neighbor for neighbor in GM.G1[node] if neighbor not in GM.core_1])
            for node in new_nodes:
                if node not in GM.inout_1:
                    GM.inout_1[node] = self.depth

            new_nodes = set()
            for node in GM.core_2:
                new_nodes.update([neighbor for neighbor in GM.G2[node] if neighbor not in GM.core_2])
            for node in new_nodes:
                if node not in GM.inout_2:
                    GM.inout_2[node] = self.depth

    def restore(self):
        if self.G1_node is not None and self.G2_node is not None:
            del self.GM.core_1[self.G1_node]
            del self.GM.core_2[self.G2_node]

        for vector in (self.GM.inout_1, self.GM.inout_2):
            for node in list(vector.keys()):
                if vector[node] == self.depth:
                    del vector[node]
