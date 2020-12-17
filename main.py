import configparser
import getopt
import os
import sys

import matplotlib.pyplot as plt

from src import parser, matcher, graph


class Setting:
    def __init__(self, setting_dict):
        self.target = setting_dict['target']
        self.query = setting_dict['query']
        self.match = setting_dict['match']
        self.loss = setting_dict['loss']
        self.output_path = setting_dict['output_path']
        self.output_fig = setting_dict['output_fig']
        self.output_res = setting_dict['output_res']
        self.silent = setting_dict['silent']


def run_task(id, setting):
    silent = (setting.silent == 'True')
    print('开始执行%s' % id) if not silent else ''
    print('读取res文件%s...' % setting.target) if not silent else ''
    target = graph.convert_cell(parser.parse_res(setting.target))
    print('读取pdb文件%s...' % setting.query) if not silent else ''
    query = graph.convert_cell(parser.parse_pdb(setting.query)).max_subgraph()
    match = setting.match
    print('开始匹配，匹配算法为match_%s' % match) if not silent else ''
    result = None
    loss_atom = setting.loss
    if '.' in loss_atom:
        loss_atom = float(loss_atom)
    else:
        loss_atom = int(loss_atom)
    if match == '1':
        result = matcher.match(target, query, True, loss_atom)
    elif match == '2':
        result = matcher.match(target, query, False, loss_atom)

    if result.is_matched:
        target.draw_graph(result.best_match)
        plt.title('%s target=%s query=%s\n match_mode=%s loss_atom=%s\n %s' % (
            id, setting.target, setting.query, match, setting.loss, result.to_string()))
        if setting.output_fig in ('1', '2'):
            os.makedirs(setting.output_path, exist_ok=True)
            plt.savefig('%s%s.jpg' % (setting.output_path, id.lstrip('task:')))
        if setting.output_fig == '2':
            plt.show()
        plt.close()
        if setting.output_res == 'True':
            parser.to_res(setting.target, '%s%s.res' % (setting.output_path, id.lstrip('task:')), result.best_match)
    print('%s %s %s' % (id, result.is_matched, result.to_string()))


def config_mode(argv):
    opts, args = getopt.getopt(argv, '-c', ['config='])
    config_file = 'config.ini'
    for opt, arg in opts:
        if opt in ('c', 'config'):
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
        s = Setting(setting)
        run_task(task, s)


def cmd_mode(argv):
    setting_dict = {'target': argv[0], 'query': argv[1], 'match': 1, 'loss': 0.2, 'output_path': '', 'output_fig': 2,
                    'output_res': False, 'silent': False}
    opts, args = getopt.getopt(argv[2:], '', ['match=', 'loss=', 'score=', 'output_path=',
                                              'output_fig=', 'output_res', 'silent'])
    for opt, arg in opts:
        if opt == '--silent':
            setting_dict['silent'] = 'True'
        elif opt == '--output_res':
            setting_dict['output_res'] = 'True'
        else:
            setting_dict[opt[2:]] = arg
    s = Setting(setting_dict)
    run_task('task:default', s)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        config_mode('')
    elif sys.argv[1].startswith('-'):
        config_mode(sys.argv[1:])
    else:
        cmd_mode(sys.argv[1:])
