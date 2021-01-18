from crystalsearch.graph import Graph


class CoordinateMatcher:
    class Result:
        """包装匹配结果类"""
        def __init__(self, is_matched, matcher, match_pairs):
            self.is_matched = is_matched
            self.match_pairs = match_pairs
            self.match_number = 0
            self.match_ratio = 0
            self.match_weighted_ratio = 0
            if is_matched:
                for r in match_pairs:
                    wr = sum([r[k].mass for k in r]) / sum([atom.mass for atom in matcher])
                    if wr > self.match_weighted_ratio:
                        self.match_weighted_ratio = wr
                        self.best_match = r
                self.match_number = len(self.best_match.keys())
                self.match_ratio = self.match_number / len(matcher)

        def to_string(self):
            return 'match_number=%d match_ratio=%.3f match_weighted_ratio=%.3f' % (
                self.match_number, self.match_ratio, self.match_weighted_ratio)

    def __init__(self, target: Graph, query: Graph):
        self.target = target
        self.query = query

