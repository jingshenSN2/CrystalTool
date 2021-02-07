import configparser
import getopt
import os

from crystalsearch.run import Setting, run_task


def run_task_in_config(argv):
    opts, args = getopt.getopt(argv, '-c', ['config='])
    config_file = 'task_config.ini'
    for opt, arg in opts:
        if opt in ('c', 'config'):
            config_file = arg
    cfp = configparser.ConfigParser()
    cfp.read(config_file, encoding='utf-8')
    section = cfp.sections()
    section.remove('global')
    global_setting = dict(cfp.items('global'))
    i = 1
    for task in section:
        setting = global_setting.copy()
        for k, v in cfp.items(task):
            setting[k] = v
        if setting['all_res'] == 'True':
            path = setting['target']
            files = os.listdir(path)
            for file in files:
                filetype = os.path.splitext(file)[1]
                if filetype == '.res':
                    s = Setting(setting)
                    s.target = path + file
                    run_task(i, s)
                    i = i + 1
        else:
            s = Setting(setting)
            run_task(i, s)
