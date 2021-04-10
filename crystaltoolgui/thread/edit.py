import threading

from crystalbase import edit_hkl


class EditThread(threading.Thread):
    def __init__(self, hkl_files, method, params, signal):
        super(EditThread, self).__init__()
        self.hkl_files = hkl_files
        self.method = method
        self.params = params
        self.signal = signal

    def run(self):
        """运行所有来自图形界面的任务"""
        process = 0
        for hkl_file in self.hkl_files:
            process += 1
            output = edit_hkl(hkl_file, self.method, self.params)
            self.signal.emit(process, output)
