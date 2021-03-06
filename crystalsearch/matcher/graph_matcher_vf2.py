from crystalsearch import graph, matcher


def node_match(atom1, atom2):
    """节点匹配，原子质量之比0.7~1.4内为匹配"""
    ratio = atom1['mass'] / atom2['mass']
    return 0.7 < ratio < 1.4


class GraphMatcherVF2:

    def __init__(self, G1: graph.Graph, G2: graph.Graph, node_match=node_match, loss_atom=0):
        self.G1 = G1
        self.G2 = G2
        self.G1_nodes = set(self.G1.nodes())
        self.G2_nodes = set(self.G2.nodes())
        self.node_match = node_match
        self.stop_len = len(G1) - loss_atom
        self.state = State(self)

        pf = self.calculate_prob()
        self.G2_order = self.generate_node_order(pf)

        self.core_1 = {}
        self.core_2 = {}
        self.inout_1 = {}
        self.inout_2 = {}

    def get_result(self):
        return Result(self.subgraph_is_isomorphic(), self.G1, self.G2, self.subgraph_isomorphisms_iter())

    def calculate_prob(self):
        pf = {}
        for u in self.G2_nodes:
            pl = 0
            pd = 0
            d = self.G2.degree(u)
            for v in self.G1_nodes:
                if self.node_match(u, v):
                    pl += 1
                if self.G1.degree(v) >= d:
                    pd += 1
            pf[u] = pl * pd
        return pf

    def generate_node_order(self, pf):
        seq = sorted(pf.keys(), key=lambda x:pf[x], reverse=True)
        return {i: seq[i] for i in range(len(seq))}

    def match(self):
        if len(self.core_1) >= self.stop_len:
            self.mapping = self.core_1.copy()
            yield self.mapping
        else:
            for u, v in self.candidate_pairs_iter():
                if self.syntactic_feasibility(u, v):
                    if self.semantic_feasibility(u, v):
                        s = State(self, u, v)
                        yield from self.match()
                        s.restore()

    def candidate_pairs_iter(self):
        G1_nodes = self.G1_nodes
        G2_nodes = self.G2_nodes
        min_order = self.G2_order.__getitem__

        T1 = [node for node in self.inout_1 if node not in self.core_1]
        T2 = [node for node in self.inout_2 if node not in self.core_2]

        if T1 and T2:
            node_2 = min(T2, key=min_order)
            for node_1 in T1:
                yield node_1, node_2
        else:
            other_node = min(G2_nodes - set(self.core_2), key=min_order)
            for node in self.G1_nodes:
                if node not in self.core_1:
                    yield node, other_node

    def syntactic_feasibility(self, u, v):
        return self.node_match(u, v)

    def semantic_feasibility(self, G1_node, G2_node):
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

    def subgraph_is_isomorphic(self):
        try:
            x = next(self.subgraph_isomorphisms_iter())
            return True
        except StopIteration:
            return False

    def subgraph_isomorphisms_iter(self):
        yield from self.match()


class State:

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


class Result:

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

