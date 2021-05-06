import threading

from crystalbase import check_pattern, check_sequence


class CheckThread(threading.Thread):
    def __init__(self, hkl_file, method, pattern, sequence, signal):
        super(CheckThread, self).__init__()
        self.hkl_file = hkl_file
        self.method = method
        self.pattern = pattern
        self.sequence = sequence
        self.signal = signal

    def run(self):
        """运行来自图形界面的任务"""
        if self.method == 'pattern':
            output = check_pattern(self.hkl_file, self.pattern)
        else:
            output = check_sequence(self.hkl_file, self.sequence)
        self.signal.emit(output)