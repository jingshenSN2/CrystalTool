import sys
import os
import getopt
import configparser
from src import CrystalParser as CP, MatchRater as MR, GraphHandler as GH
import matplotlib.pyplot as plt


def run_task(id, setting):
    silent = (setting['silent'] == 'True')
    print('开始执行%s' % id) if not silent else ''
    print('读取res文件%s...' % setting['target']) if not silent else ''
    target = GH.graph_converter(CP.parse_res(setting['target']))
    print('读取pdb文件%s...' % setting['query']) if not silent else ''
    query = GH.max_subgraph_converter(CP.parse_pdb(setting['query']))
    match = setting['match']
    print('开始匹配，匹配算法为match_%s' % match) if not silent else ''
    result = None
    loss_atom = setting['loss']
    if '.' in loss_atom:
        loss_atom = float(loss_atom)
    else:
        loss_atom = int(loss_atom)
    if match == '1':
        result = MR.match_1(target, query, loss_atom)
    elif match == '2':
        result = MR.match_2(target, query, loss_atom)
    print('匹配成功！' if result else '匹配失败，请调整参数。') if not silent else ''
    rmsd = -1
    if result:
        rmsd, best_result = MR.best_result(result)
        GH.draw_graph_highlight(target, best_result)
        plt.title('%s target=%s query=%s\n match_mode=%s loss_atom=%s rmsd=%.2f' % (id, setting['target'], setting['query'], match, setting['loss'], rmsd))
        if setting['fig'] in ('1', '2'):
            os.makedirs(setting['output_path'], exist_ok=True)
            plt.savefig('%s%s.jpg' % (setting['output_path'], id.strip('task:')))
        if setting['fig'] == '2':
            plt.show()
        plt.close()
    print('%s True %.2f' % (id, rmsd)) if result else print('%s False' % id)


def main(argv):
    opts, args = getopt.getopt(argv, '-c', ['config='])
    config_file = 'config.ini'
    for opt, arg in opts:
        if opt in ('c','config'):
            config_file = arg
    cfp = configparser.ConfigParser()
    cfp.read(config_file, encoding='utf-8')
    section = cfp.sections()
    section.remove('global')
    global_setting = dict(cfp.items('global'))
    for task in section:
        setting = global_setting.copy()
        for k, v in cfp.items(task):
            setting[k] = v
        run_task(task, setting)


if __name__ == '__main__':
    main(sys.argv[1:])