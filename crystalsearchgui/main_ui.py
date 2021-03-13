import queue

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout

from crystalsearch import run
from crystalsearchgui.input.match_ui import MatchUI
from crystalsearchgui.input.parameter_ui import ParameterUI
from crystalsearchgui.input.solve_ui import SolveUI
from crystalsearchgui.output.result_table_ui import ResultTableUI


class MainGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(1200, 800)
        self.setWindowTitle('电子衍射结构解析评分程序')

        self.layout = QGridLayout(self)
        self.layout.setGeometry(QRect(20, 20, 1200, 600))

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
        process_q = queue.Queue()
        hkl_files = self.solve_ui.get_hkl_files()
        ins_file = self.solve_ui.get_ins_file()
        thread = run.SolveThread(hkl_files, ins_file, process_q)
        thread.start()
        process = 0
        while True:
            if not process_q.empty():
                process = process_q.get()
                self.solve_ui.set_process(process)
            if process == len(hkl_files):
                break

    def match(self):
        process_q = queue.Queue()
        result_q = queue.Queue()
        res_files = self.match_ui.get_res_files()
        pdb_file = self.match_ui.get_pdb_file()
        keep_skeleton = self.para_input_ui.use_old_algorithm()
        max_loss_atom = self.para_input_ui.get_max_loss_atom()
        thread = run.MatchThread(res_files, pdb_file, keep_skeleton, max_loss_atom, process_q, result_q)
        thread.start()
        while True:
            if not process_q.empty():
                process = process_q.get()
                self.match_ui.set_process(process)
            if not result_q.empty():
                results = result_q.get()
                break
        self.result_table_ui.updateResults(results)