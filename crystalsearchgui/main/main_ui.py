from PyQt5.QtCore import QRect, pyqtSignal
from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout

from crystalsearch import run
from crystalsearchgui.input.match_ui import MatchUI
from crystalsearchgui.input.parameter_ui import ParameterUI
from crystalsearchgui.input.solve_ui import SolveUI
from crystalsearchgui.output.result_table_ui import ResultTableUI


class MainUI(QWidget):

    solve_signal = pyqtSignal(int)
    match_signal = pyqtSignal(int, list)

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.solve_signal.connect(self.solve_update)
        self.match_signal.connect(self.match_update)

    def init_ui(self):
        self.setMinimumSize(1200, 800)
        self.setWindowTitle('电子衍射结构解析评分程序')

        self.layout = QGridLayout(self)
        self.layout.setGeometry(QRect(20, 20, 1200, 800))

        self.input_layout = QHBoxLayout(self)
        self.layout.addLayout(self.input_layout, 0, 0)

        self.solve_ui = SolveUI(self)
        self.match_ui = MatchUI(self)
        self.para_input_ui = ParameterUI()

        self.input_layout.addLayout(self.solve_ui.layout, 3)
        self.input_layout.addLayout(self.match_ui.layout, 3)
        self.input_layout.addLayout(self.para_input_ui.layout, 1)

        self.output_layout = QHBoxLayout(self)
        self.layout.addLayout(self.output_layout, 1, 0)

        self.result_table_ui = ResultTableUI()
        self.output_layout.addLayout(self.result_table_ui.layout)

    def solve(self):
        solve_ui = self.solve_ui
        if not solve_ui.start_run():
            return
        hkl_files = solve_ui.get_hkl_files()
        ins_file = solve_ui.get_ins_file()
        thread = run.SolveThread(hkl_files, ins_file, self.solve_signal)
        thread.start()

    def match(self):
        match_ui = self.match_ui
        if not match_ui.start_run():
            return
        res_files = match_ui.get_res_files()
        pdb_file = match_ui.get_pdb_file()
        use_old_algorithm = self.para_input_ui.use_old_algorithm()
        max_loss_atom = self.para_input_ui.get_max_loss_atom()
        thread = run.MatchThread(res_files, pdb_file, use_old_algorithm, max_loss_atom, self.match_signal)
        thread.start()

    def solve_update(self, process):
        self.solve_ui.set_process(process)

    def match_update(self, process, results):
        self.match_ui.set_process(process)
        self.result_table_ui.updateResults(results)
