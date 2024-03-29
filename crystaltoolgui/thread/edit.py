import threading

from crystalbase import edit_hkl


class EditThread(threading.Thread):
    def __init__(self, hkl_files, method, edit_range, params, is_scale, signal):
        super(EditThread, self).__init__()
        self.hkl_files = hkl_files
        self.method = method
        self.edit_range = edit_range
        self.params = params
        self.is_scale = is_scale
        self.signal = signal

    def run(self):
        """运行所有来自图形界面的任务"""
        process = 0
        for hkl_file in self.hkl_files:
            process += 1
            output = edit_hkl(hkl_file, self.method, self.edit_range, self.params, self.is_scale)
            self.signal.emit(process, output)
