import pandas as pd

from ..libs import *
from ..tabs import Ui_tabhklchecker
from ..thread.check import *


@singleton
class HklChecker(QWidget):
    check_pat_signal = pyqtSignal(pd.DataFrame)
    check_seq_signal = pyqtSignal(pd.DataFrame)

    def __init__(self):
        super().__init__()
        self.hkl_file = ''
        self.ui = Ui_tabhklchecker()
        self.ui.setupUi(self)
        self.check_pat_signal.connect(self.update_pat_result)
        self.check_seq_signal.connect(self.update_seq_result)
        self.ui.pB_check_start.clicked.connect(self.check)
        self.ui.pB_check_choose.clicked.connect(self.open_hkl)

    def open_hkl(self):
        hkl_file, success = QFileDialog.getOpenFileName(caption='选择HKL文件', directory='./',
                                                        filter='Hkl File (*.hkl)')
        if not success:
            return
        self.hkl_file = hkl_file
        self.ui.l_check_status.setText('已选择%s' % hkl_file)

    def check(self):
        if not self.has_file:
            self.set_text('无可检查文件')
            return
        if not self.has_params:
            self.set_text('未提供检查方法和参数')
            return
        self.set_text('开始检查...')
        if self.method == 'pattern':
            thread = CheckPairThread(self.hkl_file, self.pattern, self.conf_level, self.check_pat_signal)
        else:
            thread = CheckSeqThread(self.hkl_file, self.sequence, self.n_limit, self.check_seq_signal)
        thread.start()
        self.ui.pB_check_start.setEnabled(False)

    def update_pat_result(self, output):
        self.set_text('检查完成, 共%d个问题' % len(output))
        result_str = ''
        for i, row in output.iterrows():
            result_str += '{}. {} and {}:\n'.format(i + 1, row['k'], row['v'])
            result_str += '强度分别为: {}, {}, t_value: {:.2f}\n'.format(row['k_int'], row['v_int'], row['t_value'])
        self.ui.tB_check_view.setText(result_str)
        self.ui.pB_check_start.setEnabled(True)

    def update_seq_result(self, output):
        self.set_text('检查完成, 共%d个问题' % len(output))
        result_str = ''
        for i, row in output.iterrows():
            result_str += '{}: '.format(row['hkl'])
            if row['exist']:
                result_str += '{}\n'.format(row['int'])
            else:
                result_str += '不存在!\n'
        self.ui.tB_check_view.setText(result_str)
        self.ui.pB_check_start.setEnabled(True)

    def set_text(self, text: str):
        self.ui.l_check_result.setText(text)
        self.ui.l_check_result.repaint()

    @property
    def has_file(self):
        return self.hkl_file != ''

    @property
    def has_params(self):
        if self.method == 'pattern':
            return self.pattern is not None
        else:
            return self.sequence is not None

    @property
    def method(self):
        if self.ui.rB_check_pattern.isChecked():
            return 'pattern'
        if self.ui.rB_check_seq.isChecked():
            return 'seq'

    @property
    def pattern(self):
        hkl1 = self.ui.lE_check_h1.text(), self.ui.lE_check_k1.text(), self.ui.lE_check_l1.text()
        hkl2 = self.ui.lE_check_h2.text(), self.ui.lE_check_k2.text(), self.ui.lE_check_l2.text()
        if '' in hkl1 or '' in hkl2:
            return None
        return hkl1, hkl2

    @property
    def conf_level(self):
        return self.ui.dSB_check_conf_level.value()

    @property
    def n_limit(self):
        return self.ui.sB_check_n.value()

    @property
    def sequence(self):
        seq_hkl = self.ui.lE_check_seqh.text(), self.ui.lE_check_seqk.text(), self.ui.lE_check_seql.text()
        if '' in seq_hkl:
            return None
        return seq_hkl
