from ..libs import *
from ..tabs import Ui_tabhklchecker


@singleton
class HklChecker(QWidget):
    edit_signal = pyqtSignal(int, list)

    def __init__(self):
        super().__init__()
        self.hkl_file = []
        self.ui = Ui_tabhklchecker()
        self.ui.setupUi(self)
        self.ui.pB_check_start.clicked.connect(self.check)
        self.ui.pB_check_choose.clicked.connect(self.open_hkl)

    def open_hkl(self):
        hkl_file, success = QFileDialog.getOpenFileName(caption='选择HKL文件', directory='./',
                                                        filter='Hkl File (*.hkl)')
        if not success:
            return
        self.hkl_file = hkl_file

    def check(self):
        pass

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
        return hkl1, hkl2
