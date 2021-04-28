from .coord_matcher import coordinate_error
from ..graph import Graph


class Result:
    def __init__(self, is_matched: bool, target: Graph, query: Graph, match_pairs: list, threshold: dict,
                 sort_by: list):
        """
        匹配结果类
        :param is_matched: 是否匹配成功
        :param target: 匹配的目标图（RES文件）
        :param query: 匹配的查询图（PDB文件）
        :param match_pairs: 匹配映射
        :param threshold: 汇报阈值，key是阈值类型，value是对应的阈值，低于此值的结果被视为匹配失败
        :param sort_by: 结果的排序方法，例如['-Nm', '-Rwm']，先按Nm倒序排列，Nm相同者按Rwm排序
        """
        self.is_matched = is_matched
        self.match_pairs = match_pairs
        self.target = target
        self.query = query
        self.rotation = None
        self.threshold = threshold
        self.sort_by = sort_by
        self.avg_feature = {'Nm': 0, 'Tm': 0, 'Rwm': 0, 'Rwe2': 0, 'Ram': 0, 'Rc': 0}
        self.best_feature = {'Nm': 0, 'Tm': 0, 'Rwm': 0, 'Rwe2': 0, 'Ram': 0, 'Rc': 0}
        self.results = []
        if self.is_matched:
            self.calculate_match_result()

    def calculate_match_result(self, base_query=None):
        """
        计算各个评价指标，根据汇报阈值筛选后排序
        :param base_query: 用于旧匹配算法，表示完整的查询图
        :return:
        """
        if base_query is not None:
            self.query = base_query
        self.avg_feature = {'Nm': 0, 'Tm': 0, 'Rwm': 0, 'Rwe2': 0, 'Ram': 0, 'Rc': 0}
        self.best_feature = {'Nm': 0, 'Tm': 0, 'Rwm': 0, 'Rwe2': 0, 'Ram': 0, 'Rc': 0}
        self.results.clear()
        # 只保留匹配上原子数最多的那些结果
        max_nm = max([len(p.keys()) for p in self.match_pairs])
        self.match_pairs = [p for p in self.match_pairs if len(p.keys()) == max_nm]
        # 计算匹配上次数Tm
        tm_count = 0
        if 'Tm' in self.threshold:
            tm = self.threshold['Tm']
            tm_set = set()
            for p in self.match_pairs:
                new_set = tm_set.union(set(p.keys()))
                if len(new_set) - len(tm_set) >= 0.5 * len(p.keys()):
                    # 当某个映射有50%的原子与其他映射不同时，认为是单独的一个匹配
                    tm_set = new_set
                    tm_count += 1
            if tm_count < tm:
                self.is_matched = False
                return

        match_count = len(self.match_pairs)
        for p in self.match_pairs:
            # 计算评价指标
            feats = {'Tm': tm_count, 'pair': p, 'Nm': len(p.keys()),
                     'Rwm': sum([p[k].mass for k in p]) / sum([atom.mass for atom in self.query.g]),
                     'Rwe2': sum([p[k].aindex ** 2 for k in p]) / sum([atom.aindex ** 2 for atom in self.query.g]),
                     'Ram': 1 - pow(sum([(k.mass - p[k].mass) ** 2 for k in p]) / sum([p[k].mass ** 2 for k in p]),
                                    0.5)}
            feats['Rc'], self.rotation = coordinate_error(p)
            # 检查结果是否符合汇报阈值
            flag = True
            for k in self.threshold:
                if k == 'Tm':
                    continue
                if self.threshold[k] > feats[k]:
                    flag = False
            if flag:
                # 更新结果到avg_feature和best_feature
                for k in self.best_feature:
                    self.best_feature[k] = max(self.best_feature[k], feats[k])
                    self.avg_feature[k] += feats[k] / match_count
                self.results.append(feats)

        def sort_key(r):
            # 排序函数，会自动解析sort_by字符串为排序规则
            key = []
            for s in self.sort_by:
                if s[1:] not in r:
                    print('%s不是有效的排序依据，已自动忽略' % s[1:])
                    continue
                k = r[s[1:]]
                key.append(k if s[0] == '+' else -k)
            return tuple(key)

        self.results.sort(key=sort_key)
