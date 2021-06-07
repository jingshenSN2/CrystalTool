import threading

from crystalsearch import match_one


class MatchThread(threading.Thread):
    def __init__(self, res_files, pdb_file, use_old_algorithm, max_loss_atom, multilayer, threshold, sort_by, signal):
        super(MatchThread, self).__init__()
        self.res_files = res_files
        self.pdb_file = pdb_file
        self.use_old_algorithm = use_old_algorithm
        self.max_loss_atom = max_loss_atom
        self.multilayer = multilayer
        self.threshold = threshold
        self.sort_by = sort_by
        self.signal = signal

    def run(self):
        """运行所有来自图形界面的任务"""
        results = []
        process = 0
        for res in self.res_files:
            result = match_one(res, self.pdb_file, self.use_old_algorithm, self.max_loss_atom,
                               self.multilayer, self.threshold, self.sort_by)
            results.append(result)
            process += 1
            self.signal.emit(process, [])

        def sort_key(r):
            # 排序函数，会自动解析sort_by字符串为排序规则
            feat = r.best_feature
            key = []
            for s in self.sort_by:
                sstrip = s.strip('+-')
                if sstrip not in feat:
                    print('%s不是有效的排序依据，已自动忽略' % s)
                    continue
                k = feat[sstrip]
                key.append(-k if '-' in s else k)
            return tuple(key)

        results.sort(key=sort_key)
        self.signal.emit(process, results)
