from .coord_matcher import coordinate_error
from ..graph import Graph


class Result:
    def __init__(self, is_matched: bool, target: Graph, query: Graph, match_pairs: list, threshold: dict,
                 sort_by: list):
        self.is_matched = is_matched
        self.match_pairs = match_pairs
        self.target = target
        self.query = query
        self.rotation = None
        self.threshold = threshold
        self.sort_by = sort_by
        self.best_feature = {'Nm': 0, 'Tm': 0, 'Rwm': 0, 'Rwe2': 0, 'Ram': 0, 'Rc': 0}
        self.results = []
        if self.is_matched:
            self.calculate_match_result()

    def calculate_match_result(self, base_query=None):
        if base_query is not None:
            self.query = base_query
        self.best_feature = {'Nm': 0, 'Tm': 0, 'Rwm': 0, 'Rwe2': 0, 'Ram': 0, 'Rc': 0}
        self.results.clear()
        tm_count = 0
        if 'Tm' in self.threshold:
            tm = self.threshold['Tm']
            tm_set = set()
            for p in self.match_pairs:
                new_set = tm_set.union(set(p.keys()))
                if len(new_set) - len(tm_set) >= 0.5 * len(p.keys()):
                    tm_set = new_set
                    tm_count += 1
            if tm_count < tm:
                self.is_matched = False
                return

        for p in self.match_pairs:
            feats = {'Tm': -1, 'pair': p, 'Nm': len(p.keys()),
                     'Rwm': sum([p[k].mass for k in p]) / sum([atom.mass for atom in self.query.g]),
                     'Rwe2': sum([p[k].aindex ** 2 for k in p]) / sum([atom.aindex ** 2 for atom in self.query.g]),
                     'Ram': 1 - pow(sum([(k.mass - p[k].mass) ** 2 for k in p]) / sum([p[k].mass ** 2 for k in p]),
                                    0.5)}
            feats['Rc'], self.rotation = coordinate_error(p)
            flag = True
            for k in self.threshold:
                if k == 'Tm':
                    continue
                if self.threshold[k] > feats[k]:
                    flag = False
            if flag:
                for k in self.best_feature:
                    self.best_feature[k] = max(self.best_feature[k], feats[k])
                self.results.append(feats)

        def sort_key(r):
            key = []
            for s in self.sort_by:
                if s[1:] not in r:
                    print('%s不是有效的排序依据，已自动忽略' % s[1:])
                    continue
                k = r[s[1:]]
                key.append(k if s[0] == '+' else -k)
            return tuple(key)

        self.results.sort(key=sort_key)
