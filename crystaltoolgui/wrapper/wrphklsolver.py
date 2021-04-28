from ..libs import *
from ..tabs import Ui_tabhklsolver
from ..thread import SolveThread


@singleton
class HklSolver(QWidget):

    solve_signal = pyqtSignal(int, list)

    def __init__(self):
        super().__init__()
        self.hkl_files = []
        self.ins_files = []
        self.res_files = []
        self.ui = Ui_tabhklsolver()
        self.ui.setupUi(self)
        self.solve_signal.connect(self.set_process)
        self.ui.pB_solve_choose_hkl.clicked.connect(self.open_hkl)
        self.ui.pB_solve_ins.clicked.connect(self.open_ins)
        self.ui.pB_solve.clicked.connect(self.solve)
        self.ui.pB_solve_send.clicked.connect(self.send_selected)

    @property
    def has_files(self):
        return self.hkl_files != [] and self.ins_files != []

    @property
    def job_count(self):
        return len(self.hkl_files) * len(self.ins_files)

    def solve(self):
        if not self.has_files:
            self.set_text('缺失文件')
            return
        self.set_text('开始求解...')
        thread = SolveThread(self.hkl_files, self.ins_files, self.solve_signal)
        thread.start()
        self.ui.pB_solve.setEnabled(False)

    def set_process(self, process: int, new_res: list):
        if self.job_count == 0:
            return
        self.set_text('正在求解...已完成%d/%d' % (process, self.job_count))
        self.ui.bar_solve.setValue(int(process * 100 / self.job_count))
        for file in new_res:
            if file not in self.res_files:
                self.res_files.append(file)
        self.ui.l_solve_res_count.setText('总计%d个' % len(self.res_files))
        slm = QStringListModel()
        slm.setStringList(self.res_files)
        self.ui.lV_solve_res.setModel(slm)
        if process == self.job_count:
            self.set_text('求解完成')
            self.ui.pB_solve.setEnabled(True)

    def set_text(self, text: str):
        self.ui.l_solve.setText(text)
        self.ui.l_solve.repaint()

    def update_hkl(self, hkl_files):
        self.hkl_files = hkl_files
        self.ui.l_solve_hkl_count.setText('已选%d个' % len(hkl_files))
        slm = QStringListModel()
        slm.setStringList(self.hkl_files)
        self.ui.lV_solve_hkl.setModel(slm)

    def open_hkl(self):
        hkl_files, success = QFileDialog.getOpenFileNames(caption='选择衍射结构的HKL文件', directory='./', filter='Hkl Files (*.hkl)')
        if not success:
            return
        self.update_hkl(hkl_files)

    def open_ins(self):
        self.ins_files, success = QFileDialog.getOpenFileNames(caption='选择衍射结构的INS文件', directory='./',
                                                               filter='Ins Files (*.ins)')
        if not success:
            return
        self.ui.l_solve_ins.setText('已选%s个INS文件' % len(self.ins_files))
        self.ui.l_solve_ins.setToolTip('\n'.join(self.ins_files))

    def send_selected(self):
        from .wrpresmatcher import ResMatcher
        ResMatcher().update_res(self.res_files)

    @property
    def shelxt_params(self):
        return self.ui.lE_solve_xtparam.text()
