from networkx.algorithms.isomorphism import GraphMatcher
import networkx as nx


def node_match(atom1,atom2):
    cno = ['C','N','O','Q']
    if atom1['element'] in cno and atom2['element'] in cno:
        return True
    return atom1['element'] == atom2['element']


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


class MatchRater:
    def __init__(self, target, query, node_match=node_match, edge_match=edge_match):
        self.target = target
        self.query = query
        self.result = None
        self.node_match = node_match
        self.edge_match = edge_match

    def match(self):
        gm = GraphMatcher(self.target, self.query, node_match=self.node_match,
                          edge_match=self.edge_match)
        while not gm.subgraph_is_isomorphic():
            flag, self.query = shrink_one(self.query)
            if not flag:
                print('匹配失败')
                return False
            gm = GraphMatcher(self.target, self.query, node_match=self.node_match,
                          edge_match=self.edge_match)
        return gm.subgraph_isomorphisms_iter()






