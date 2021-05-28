from crystalbase import laue_group_name

from ..libs import *
from ..tabs import Ui_tabhklchecker
from ..thread.check import *


@singleton
class HklChecker(QWidget):
    check_signal = pyqtSignal(int, str)

    def __init__(self):
        super().__init__()
        self.hkl_file = ''
        self.ui = Ui_tabhklchecker()
        self.ui.setupUi(self)
        for idx, name in laue_group_name.items():
            self.ui.cB_check_laue.setItemText(idx, name)
        self.check_signal.connect(self.update_result)
        self.ui.pB_check_start.clicked.connect(self.check)
        self.ui.pB_check_with_save.clicked.connect(self.check)
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
        thread = CheckThread(self.hkl_file, self.laue, self.z_value, self.error_rate, self.recursive,
                             self.save_option, self.sequence, self.check_signal)
        thread.start()
        self.ui.pB_check_start.setEnabled(False)
        self.ui.pB_check_with_save.setEnabled(False)

    def update_result(self, issue_count, output):
        self.set_text('检查完成, 共找到%d组指标' % issue_count)
        self.ui.tB_check_view.setText(output)
        self.ui.pB_check_start.setEnabled(True)
        self.ui.pB_check_with_save.setEnabled(True)

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
    def z_value(self):
        return self.ui.dSB_check_z_value.value()

    @property
    def error_rate(self):
        return self.ui.dSB_check_error_rate.value()

    @property
    def recursive(self):
        return self.ui.cB_check_recursive.isChecked()

    @property
    def save_option(self):
        return {'remove_high_var': self.ui.cB_check_save_opt.currentIndex() in [0, 2],
                'remove_outlier': self.ui.cB_check_save_opt.currentIndex() in [1, 2]}

    @property
    def sequence(self):
        if self.is_seq:
            return self.ui.cB_check_seqh.currentText(), \
                   self.ui.cB_check_seqk.currentText(), \
                   self.ui.cB_check_seql.currentText()
        return None
