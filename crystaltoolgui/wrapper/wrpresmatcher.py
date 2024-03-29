from ..libs import *
from ..tabs import Ui_tabresmatcher
from ..thread import MatchThread


@singleton
class ResMatcher(QWidget):

    match_signal = pyqtSignal(int, list)

    def __init__(self):
        super().__init__()
        self.res_files = []
        self.pdb_file = ''
        self.results = []
        self.ui = Ui_tabresmatcher()
        self.ui.setupUi(self)
        self.match_signal.connect(self.set_process)
        self.ui.pB_match_choose_res.clicked.connect(self.open_res)
        self.ui.pB_pdb.clicked.connect(self.open_pdb)
        self.ui.pB_match_start.clicked.connect(self.match)

    @property
    def has_files(self):
        return self.res_files != [] and self.pdb_file != ''

    @property
    def job_count(self):
        return len(self.res_files)

    def match(self):
        if not self.has_files:
            self.set_text('缺失文件')
            return
        self.set_text('开始求解...')
        self.ui.bar_match.setValue(0)
        thread = MatchThread(self.res_files, self.pdb_file, self.use_old_algorithm, self.max_loss_atom,
                             self.multilayer, self.threshold, self.sort_by, self.match_signal)
        thread.start()
        self.ui.pB_match_start.setEnabled(True)

    def set_process(self, process: int, results: list):
        if self.job_count == 0:
            return
        self.set_text('正在匹配...已完成%d/%d' % (process, self.job_count))
        self.ui.bar_match.setValue(int(process * 100 / self.job_count))
        self.results = results
        if process == self.job_count:
            self.set_text('匹配完成')
            self.ui.pB_match_start.setEnabled(True)
            from ..main import MainUI
            MainUI().tabmatchresult.update_result(self.results, self.report_features)
            MainUI().setMatchResultTab()

    def set_text(self, text: str):
        self.ui.l_match_start.setText(text)
        self.ui.l_match_start.repaint()

    def update_res(self, res_files):
        self.res_files = res_files
        slm = QStringListModel()
        slm.setStringList(self.res_files)
        self.ui.lV_match_res.setModel(slm)

    def open_res(self):
        res_files, success = QFileDialog.getOpenFileNames(caption='选择衍射结构的RES文件', directory='./', filter='Res Files (*.res)')
        if not success:
            return
        self.update_res(res_files)

    def open_pdb(self):
        self.pdb_file, success = QFileDialog.getOpenFileName(caption='选择待搜索结构的PDB文件', directory='./', filter='Pdb Files (*.pdb)')
        if not success:
            return
        self.ui.l_pdb.setText('已选%s' % self.pdb_file.split('/')[-1])

    @property
    def use_old_algorithm(self):
        return self.ui.rB_old_algorithm.isChecked()

    @property
    def max_loss_atom(self):
        return self.ui.sB_loss_atom.value()

    @property
    def multilayer(self):
        return self.ui.cB_thick_x.isChecked(), self.ui.cB_thick_y.isChecked(), self.ui.cB_thick_z.isChecked()

    @property
    def threshold(self):
        if self.ui.cB_threshold.currentIndex() == 0:  # 未选择汇报阈值
            return {}
        return {self.ui.cB_threshold.currentText().split('(')[0]: self.ui.dSB_threshold.value()}

    @property
    def report_features(self):
        features = []
        if self.ui.cB_Tm.isChecked():
            features.append('Tm')
        if self.ui.cB_Nm.isChecked():
            features.append('Nm')
        if self.ui.cB_Rw.isChecked():
            features.append('Rw')
        if self.ui.cB_Ra.isChecked():
            features.append('Ra')
        if self.ui.cB_Rb.isChecked():
            features.append('Rb')
        if self.ui.cB_Rc.isChecked():
            features.append('Rc')
        if self.ui.cB_R1.isChecked():
            features.append('R1')
        if self.ui.cB_Rweak.isChecked():
            features.append('Rweak')
        if self.ui.cB_Alpha.isChecked():
            features.append('Alpha')
        return features

    @property
    def sort_by(self):
        return self.ui.lE_match_sort.text().split(',')
