import threading

from crystalbase import check_pattern, check_sequence


class CheckPairThread(threading.Thread):
    def __init__(self, hkl_file, pattern, conf_level, signal):
        super(CheckPairThread, self).__init__()
        self.hkl_file = hkl_file
        self.pattern = pattern
        self.conf_level = conf_level
        self.signal = signal

    def run(self):
        """运行来自图形界面的任务"""
        output = check_pattern(self.hkl_file, self.pattern, self.conf_level)
        self.signal.emit(output)


class CheckSeqThread(threading.Thread):
    def __init__(self, hkl_file, sequence, n_limit, signal):
        super(CheckSeqThread, self).__init__()
        self.hkl_file = hkl_file
        self.sequence = sequence
        self.n_limit = n_limit
        self.signal = signal

    def run(self):
        """运行来自图形界面的任务"""
        output = check_sequence(self.hkl_file, self.sequence, self.n_limit)
        self.signal.emit(output)
