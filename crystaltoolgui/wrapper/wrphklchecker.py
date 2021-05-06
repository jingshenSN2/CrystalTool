from ..libs import *
from ..tabs import Ui_tabhklchecker
from ..thread.check import CheckThread


@singleton
class HklChecker(QWidget):
    check_signal = pyqtSignal(list)

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

    def check(self):
        if not self.has_files:
            self.set_text('无可检查文件')
            return
        if not self.has_params:
            self.set_text('未提供检查方法和参数')
            return
        self.set_text('开始检查...')
        thread = CheckThread(self.hkl_file, self.method, self.pattern, self.sequence, self.check_signal)
        thread.start()
        self.ui.pB_check_start.setEnabled(False)

    def update_result(self, output):
        self.set_text('检查完成')
        print(output)
        self.ui.pB_check_start.setEnabled(True)

    def set_text(self, text: str):
        self.ui.l_check_status.setText(text)
        self.ui.l_check_status.repaint()

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
    def sequence(self):
        seq_hkl = self.ui.lE_check_seqh.text(), self.ui.lE_check_seqk.text(), self.ui.lE_check_seql.text()
        if '' in seq_hkl:
            return None
        return seq_hkl
