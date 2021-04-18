from ..libs import *
from ..tabs import Ui_tabhkleditor
from ..thread import EditThread


@singleton
class HklEditor(QWidget):

    edit_signal = pyqtSignal(int, list)

    def __init__(self):
        super().__init__()
        self.hkl_files = []
        self.new_hkl_files = []
        self.ui = Ui_tabhkleditor()
        self.ui.setupUi(self)
        self.edit_signal.connect(self.set_process)
        self.ui.pB_editor_choose.clicked.connect(self.open_hkl)
        self.ui.pB_editor_delect_origin.clicked.connect(self.delete_selected_origin)
        self.ui.pB_editor_start.clicked.connect(self.edit)
        self.ui.pB_editor_reselect.clicked.connect(self.reselect)
        self.ui.pB_editor_send.clicked.connect(self.send_selected)

    def open_hkl(self):
        new_hkl_files, success = QFileDialog.getOpenFileNames(caption='选择HKL文件', directory='./',
                                                              filter='Hkl Files (*.hkl)')
        if not success:
            return
        self.hkl_files = new_hkl_files
        slm = QStringListModel()
        slm.setStringList(self.hkl_files)
        self.ui.lV_editor_origin.setModel(slm)

    def edit(self):
        if not self.has_files:
            self.set_text('无可编辑文件')
            return
        if not self.has_params:
            self.set_text('未提供编辑参数')
            return
        self.set_text('开始编辑...')
        thread = EditThread(self.hkl_files, self.edit_method, self.edit_params, self.edit_signal)
        thread.start()

    def set_process(self, process: int, new_hkl: list):
        if self.job_count == 0:
            return
        self.set_text('正在生成新HKL...已完成%d/%d' % (process, self.job_count))
        self.ui.bar_editor.setValue(int(process * 100 / self.job_count))
        for file in new_hkl:
            if file not in self.new_hkl_files:
                self.new_hkl_files.append(file)
        slm = QStringListModel()
        slm.setStringList(self.new_hkl_files)
        self.ui.lV_editor_modified.setModel(slm)
        if process == self.job_count:
            self.set_text('生成结束')

    def set_text(self, text: str):
        self.ui.l_editor_start.setText(text)
        self.ui.l_editor_start.repaint()

    def delete_selected_origin(self):
        for index in self.ui.lV_editor_origin.selectedIndexes():
            self.ui.lV_editor_origin.model().removeRow(index.row())
            self.hkl_files.pop(index.row())

    def reselect(self):
        for index in self.ui.lV_editor_modified.selectedIndexes():
            pass  # TODO
            self.ui.lV_editor_origin.model().removeRow(index.row())

    def send_selected(self):
        for index in self.ui.lV_editor_modified.selectedIndexes():
            pass  # TODO
            self.ui.lV_editor_origin.model().removeRow(index.row())

    @property
    def has_files(self):
        return len(self.hkl_files) != 0

    @property
    def has_params(self):
        return self.edit_method != 0 and self.edit_params != ''

    @property
    def job_count(self):
        return len(self.hkl_files)

    @property
    def edit_method(self):
        return self.ui.cB_editor_method.currentIndex()

    @property
    def edit_params(self):
        return self.ui.lE_editor_method.text()
