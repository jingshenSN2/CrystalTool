from ..graph import Graph
from .coord_matcher import coordinate_error


class Result:
    def __init__(self, is_matched: bool, target: Graph, query: Graph, match_pairs: list, threshold: dict):
        self.is_matched = is_matched
        self.match_pairs = match_pairs
        self.target = target
        self.query = query
        self.rotation = None
        self.threshold = threshold
        self.best_feature = {'Nm': 0, 'Tm': 0, 'Rwm': 0, 'Rwe2': 0, 'Rc': 0}
        self.results = []
        if self.is_matched:
            self.calculate_match_result()

    def calculate_match_result(self, base_query=None):
        if base_query is not None:
            self.query = base_query
        self.best_feature = {'Nm': 0, 'Tm': 0, 'Rwm': 0, 'Rwe2': 0, 'Rc': 0}
        self.results.clear()
        if 'Tm' in self.threshold:
            tm = self.threshold['Tm']
            tm_count = 0
            tm_set = set()
            for p in self.match_pairs:
                new_set = tm_set.union(set(p.keys()))
                if len(new_set) - len(tm_set) >= 0.5 * len(p.keys()):
                    # 不同原子大于50%时，认为是不同的匹配
                    tm_set = new_set
                    tm_count += 1
            if tm_count < tm:
                self.is_matched = False
                return

        feats = {}
        for p in self.match_pairs:
            feats['pair'] = p
            feats['Nm'] = len(p.keys())
            feats['Rwm'] = sum([p[k].mass for k in p]) / sum([atom.mass for atom in self.query.g])
            feats['Rwe2'] = sum([p[k].aindex ** 2 for k in p]) / sum([atom.aindex ** 2 for atom in self.query.g])
            feats['Rc'], self.rotation = coordinate_error(p)
            flag = True
            for k in self.threshold:
                if self.threshold[k] > feats[k]:
                    flag = False
            if flag:
                for k in self.best_feature:
                    self.best_feature[k] = max(self.best_feature[k], feats[k])
                self.results.append(feats)
