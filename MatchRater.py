from networkx.algorithms.isomorphism import GraphMatcher


class MatchRater:
    def __init__(self, target, query, node_match=None, edge_match=None):
        self.target = target
        self.query = query
        self.result = None
        self.node_match = node_match
        self.edge_match = edge_match

    def _is_subgraph(self, g1, g2):
        gm = GraphMatcher(g1, g2, node_match=self.node_match,
                          edge_match=self.edge_match)
        return gm.subgraph_is_isomorphic()

    def match(self):
        if self._is_subgraph(self.target, self.query):
            self.result = self.query

    def _shrink_match(self, sub_query):
        degree = sub_query.degree

    def _shrink_one(self, graph):
        degree = graph.degree
        d1_nodes = set()
        for node in graph.nodes():
            if degree[node] == 1:
                d1_nodes.add(node)





