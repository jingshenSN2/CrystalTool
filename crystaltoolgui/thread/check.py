import threading

from crystalbase import check_laue, check_seq, laue_group_name


class CheckThread(threading.Thread):
    def __init__(self, hkl_file, laue, error_level, seq_pattern, signal):
        super(CheckThread, self).__init__()
        self.hkl_file = hkl_file
        self.laue = laue
        self.error_level = error_level
        self.seq_pattern = seq_pattern
        self.signal = signal

    def run(self):
        """运行来自图形界面的任务"""
        if self.seq_pattern is None:
            issue_count, output = check_laue(self.hkl_file, self.laue, self.error_level)
        else:
            issue_count, output = check_seq(self.hkl_file, self.laue, self.error_level, self.seq_pattern)
        self.signal.emit(issue_count, output)
