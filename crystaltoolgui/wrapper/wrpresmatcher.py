from ..tabs import Ui_tabresmatcher
from ..libs import *
from ..thread import MatchThread


class ResMatcher(QWidget):

    match_signal = pyqtSignal(int, list)

    def __init__(self):
        super().__init__()
        self.res_files = []
        self.pdb_file = ''
        self.results = None
        self.ui = Ui_tabresmatcher()
        self.ui.setupUi(self)
        self.match_signal.connect(self.set_process)
        self.ui.pB_match_choose_res.clicked.connect(self.open_res)
        self.ui.pB_match_delete_res.clicked.connect(self.delete_selected_res)
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
        use_old_algorithm = self.use_old_algorithm()
        max_loss_atom = self.get_max_loss_atom()
        threshold = self.get_threshold()
        thread = MatchThread(self.res_files, self.pdb_file, use_old_algorithm, max_loss_atom, threshold, self.match_signal)
        thread.start()

    def set_process(self, process: int, results: list):
        if self.job_count == 0:
            return
        self.set_text('正在求解...已完成%d/%d' % (process, self.job_count))
        self.results = results
        if process == self.job_count:
            self.set_text('求解完成')

    def set_text(self, text: str):
        self.ui.l_match_res.setText(text)
        self.ui.l_match_res.repaint()

    def open_res(self):
        new_res_files, success = QFileDialog.getOpenFileNames(caption='选择衍射结构的RES文件', directory='./', filter='Res Files (*.res)')
        if not success:
            return
        for file in new_res_files:
            if file not in self.res_files:
                self.res_files.append(file)
        slm = QStringListModel()
        slm.setStringList(self.hkl_files)
        self.ui.lV_match_res.setModel(slm)

    def open_pdb(self):
        self.pdb_file, success = QFileDialog.getOpenFileName(caption='选择待搜索结构的PDB文件', directory='./', filter='Pdb Files (*.pdb)')
        if not success:
            return
        self.ui.l_pdb.setText('已选%s' % self.ins_files)

    def delete_selected_res(self):
        for index in self.ui.lV_match_res.selectedIndexes():
            self.ui.lV_match_res.model().removeRow(index.row())

    def use_old_algorithm(self):
        return self.ui.rB_old_algorithm.isChecked()

    def get_max_loss_atom(self):
        return self.ui.sB_loss_atom.value()

    def get_threshold(self):
        if self.ui.cB_threshold.currentIndex() == 0:  # 未选择汇报阈值
            return {}
        return {self.ui.cB_threshold.currentText().split('(')[0]: self.ui.dSB_threshold.value()}

    def get_report_features(self):
        features = []
        if self.ui.cB_Nm.isChecked():
            features.append('Nm')
        if self.ui.cB_Rwm.isChecked():
            features.append('Rwm')
        if self.ui.cB_Rwe2.isChecked():
            features.append('Rwe2')
        if self.ui.cB_Rc.isChecked():
            features.append('Rc')
        return features