import pandas as pd

from ..libs import *
from ..tabs import Ui_tabhklchecker
from ..thread.check import *


@singleton
class HklChecker(QWidget):
    check_signal = pyqtSignal(pd.DataFrame)

    def __init__(self):
        super().__init__()
        self.hkl_file = ''
        self.ui = Ui_tabhklchecker()
        self.ui.setupUi(self)
        self.check_signal.connect(self.update_result)
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
        self.set_text('开始检查...')
        thread = CheckThread(self.hkl_file, self.laue, self.error_level, self.check_signal)
        thread.start()
        self.ui.pB_check_start.setEnabled(False)

    def update_result(self, output):
        self.set_text('检查完成, 共%d个问题' % len(output))
        result_str = ''
        for i, row in output.iterrows():
            result_str += '{}:\n'.format(i + 1)
            for hkl in row['hkl']:
                result_str += '{}\n'.format(hkl)
            result_str += 'outliers: {}\n'.format(row['outliers'])
        self.ui.tB_check_view.setText(result_str)
        self.ui.pB_check_start.setEnabled(True)

    def set_text(self, text: str):
        self.ui.l_check_result.setText(text)
        self.ui.l_check_result.repaint()

    @property
    def has_file(self):
        return self.hkl_file != ''

    @property
    def is_seq(self):
        return self.ui.rB_check_seq.isChecked()

    @property
    def laue(self):
        return self.ui.cB_check_laue.currentIndex()

    @property
    def error_level(self):
        return self.ui.dSB_check_conf_level.value()

    @property
    def sequence(self):
        seq_hkl = self.ui.cB_check_seqh.text(), self.ui.cB_check_seqk.text(), self.ui.cB_check_seql.text()
        return seq_hkl
