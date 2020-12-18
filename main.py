import configparser
import getopt
import os
import sys
import matplotlib.pyplot as plt
from src import parser, matcher, graph


class Setting:
    """任务参数类"""
    def __init__(self, setting_dict):
        self.target = setting_dict['target']
        self.query = setting_dict['query']
        self.keep_ring = (setting_dict['keep_ring'] == 'True')
        self.loss = setting_dict['loss']
        self.output_path = setting_dict['output_path']
        self.output_fig = setting_dict['output_fig']
        self.output_res = (setting_dict['output_res'] == 'True')
        self.silent = (setting_dict['silent'] == 'True')

    def to_string(self):
        return '%s target=%s query=%s\n keep_ring=%s loss_atom=%s\n' \
               % (id, self.target, self.query, self.keep_ring, self.loss)


def run_task(id, setting):
    silent = setting.silent
    print('开始执行%s' % id) if not silent else ''
    print('读取res文件%s...' % setting.target) if not silent else ''
    target = graph.convert_cell(parser.parse_res(setting.target))
    print('读取pdb文件%s...' % setting.query) if not silent else ''
    query = graph.convert_cell(parser.parse_pdb(setting.query)).max_subgraph()
    print('开始匹配') if not silent else ''
    loss_atom = float(setting.loss) if '.' in setting.loss else int(setting.loss)

    gm = matcher.GraphMatcher(target, query, setting.keep_ring, loss_atom)
    result = gm.match()

    if result.is_matched:
        target.draw_graph(highlight=result.best_match)
        plt.title('%s%s' % (setting.to_string(), result.to_string()))
        if setting.output_fig in ('1', '2'):
            os.makedirs(setting.output_path, exist_ok=True)
            plt.savefig('%s%s.jpg' % (setting.output_path, id.lstrip('task:')))
        if setting.output_fig == '2':
            plt.show()
        plt.close()
        if setting.output_res:
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
    setting_dict = {'target': argv[0], 'query': argv[1], 'keep_ring': 1, 'loss': 0.2, 'output_path': '', 'output_fig': 2,
                    'output_res': False, 'silent': False}
    opts, args = getopt.getopt(argv[2:], '', ['keep_ring=', 'loss=', 'score=', 'output_path=',
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
