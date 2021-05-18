import threading

from crystalbase import check_laue


class CheckThread(threading.Thread):
    def __init__(self, hkl_file, laue, error_level, signal):
        super(CheckThread, self).__init__()
        self.hkl_file = hkl_file
        self.laue = laue
        self.error_level = error_level
        self.signal = signal

    def run(self):
        """运行来自图形界面的任务"""
        output = check_laue(self.hkl_file, self.laue, self.error_level)
        self.signal.emit(output)
