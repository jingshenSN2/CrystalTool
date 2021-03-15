from crystalsearch import graph, matcher


class Result:
    def __init__(self, is_matched: bool, target: graph.Graph, query: graph.Graph, match_pairs: list):
        self.is_matched = is_matched
        self.match_pairs = match_pairs
        self.target = target
        self.query = query
        self.best_feature = [0, 0, 1000]
        self.results = []
        self.rotation = None
        if self.is_matched:
            self.calculate_match_result()

    def calculate_match_result(self, base_query=None):
        if base_query is not None:
            self.query = base_query
        self.best_feature = [0, 0, 1000]
        feature_set = set()
        for p in self.match_pairs:
            n = len(p.keys())
            wr = sum([p[k].mass for k in p]) / sum([atom.mass for atom in self.query.g])
            ce, self.rotation = matcher.coordinate_error(p)
            if (n, wr, ce) in feature_set:
                continue
            self.best_feature[0] = max(self.best_feature[0], n)
            self.best_feature[1] = max(self.best_feature[1], wr)
            self.best_feature[2] = min(self.best_feature[2], ce)
            self.results.append((p, n, wr, ce))
