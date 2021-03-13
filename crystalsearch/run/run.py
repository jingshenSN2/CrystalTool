import threading

from crystalsearch import parser, matcher, graph


class SolveThread(threading.Thread):
    def __init__(self, hkl_files, ins_file, process_q):
        super(SolveThread, self).__init__()
        self.hkl_files = hkl_files
        self.ins_file = ins_file
        self.process_q = process_q

    def run(self):
        """运行所有来自图形界面的任务"""
        process = 0
        for hkl_file in self.hkl_files:
            parser.process_one_hkl(hkl_file, self.ins_file)
            process += 1
            self.process_q.put(process)


class MatchThread(threading.Thread):
    def __init__(self, res_files, pdb_file, use_old_algorithm, max_loss_atom, process_q, result_q):
        super(MatchThread, self).__init__()
        self.res_files = res_files
        self.pdb_file = pdb_file
        self.use_old_algorithm = use_old_algorithm
        self.max_loss_atom = max_loss_atom
        self.process_q = process_q
        self.result_q = result_q

    def run(self):
        """运行所有来自图形界面的任务"""
        results = []
        process = 0
        for res in self.res_files:
            result = match_one(res, self.pdb_file, self.use_old_algorithm, self.max_loss_atom)
            results.append(result)
            process += 1
            self.process_q.put(process)
        self.result_q.put(results)


def match_one(res_file, pdb_file, use_old_algorithm, max_loss_atom):
    """运行一个来自图形界面的任务"""
    target = graph.cell2graph(parser.parseFromRES(res_file))
    query = graph.cell2graph(parser.parseFromPDB(pdb_file)).max_subgraph()
    if use_old_algorithm:
        gm = matcher.GraphMatcherOld(target, query, loss_atom=max_loss_atom)
    else:
        gm = matcher.GraphMatcherVF2(target, query, loss_atom=max_loss_atom)
    result = gm.get_result()
    return result
