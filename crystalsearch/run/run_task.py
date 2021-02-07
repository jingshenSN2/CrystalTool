import os

import matplotlib.pyplot as plt

from crystalsearch import parser, matcher, graph
from crystalsearch.run import Setting


def run_task(task_id, setting: Setting):
    silent = setting.silent
    print('开始执行%s' % task_id) if not silent else ''
    print('读取res文件%s...' % setting.target) if not silent else ''
    target = graph.cell2graph(parser.parseFromRES(setting.target))
    if len(target.g.nodes) == 0:
        print('读取res文件失败，请直接使用Shelxt程序给出的文件')
        return
    print('读取pdb文件%s...' % setting.query) if not silent else ''
    query = graph.cell2graph(parser.parseFromPDB(setting.query)).max_subgraph()
    if len(query.g.nodes) == 0:
        print('读取pdb文件失败，请直接使用Vesta程序给出的文件')
        return

    print('开始匹配') if not silent else ''
    loss_atom = float(setting.loss) if '.' in setting.loss else int(setting.loss)
    gm = matcher.GraphMatcher(target, query, setting.keep_ring, loss_atom)
    result = gm.match()

    if result.is_matched:
        target.draw_graph(highlight=result.best_match)
        plt.title('%s%s' % (setting.to_string(), result.to_string()))
        if setting.output_fig in ('1', '2'):
            os.makedirs(setting.output_path, exist_ok=True)
            plt.savefig('%s%s.jpg' % (setting.output_path, task_id))
        if setting.output_fig == '2':
            plt.show()
        plt.close()
        if setting.output_res:
            parser.to_res(setting.target, '%s%s.res' %
                          (setting.output_path, task_id.lstrip('task:')), result.best_match)
    print('; %s %s %s' % (setting.target, result.is_matched, result.to_string()))
