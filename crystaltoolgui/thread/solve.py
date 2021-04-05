import threading

from crystalbase import solve_hkl


class SolveThread(threading.Thread):
    def __init__(self, hkl_files, ins_files, signal):
        super(SolveThread, self).__init__()
        self.hkl_files = hkl_files
        self.ins_files = ins_files
        self.signal = signal

    def run(self):
        """运行所有来自图形界面的任务"""
        process = 0
        res_files = []
        for ins_file in self.ins_files:
            for hkl_file in self.hkl_files:
                new_res = solve_hkl(hkl_file, ins_file)
                process += 1
                self.signal.emit(process, new_res)
