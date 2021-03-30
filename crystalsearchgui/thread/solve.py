import threading
from crystalbase import processHkl


class SolveThread(threading.Thread):
    def __init__(self, hkl_files, ins_file, signal):
        super(SolveThread, self).__init__()
        self.hkl_files = hkl_files
        self.ins_file = ins_file
        self.signal = signal

    def run(self):
        """运行所有来自图形界面的任务"""
        process = 0
        for hkl_file in self.hkl_files:
            processHkl(hkl_file, self.ins_file)
            process += 1
            self.signal.emit(process)
