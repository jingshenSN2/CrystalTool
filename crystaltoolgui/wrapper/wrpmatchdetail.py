import re

import matplotlib

from ..libs import *
from ..tabs import Ui_tabmatchdetail

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


@singleton
class MatchDetail(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_tabmatchdetail()
        self.ui.setupUi(self)
        self.result = None
        self.pair = None
        self.res_2d = plt.subplots()
        self.pdb_2d = plt.subplots()
        self.res_3d = plt.figure()
        self.pdb_3d = plt.figure()
        self.canvas_res_2d = FigureCanvas(self.res_2d[0])
        self.canvas_pdb_2d = FigureCanvas(self.pdb_2d[0])
        self.canvas_res_3d = FigureCanvas(self.res_3d)
        self.canvas_pdb_3d = FigureCanvas(self.pdb_3d)
        hL_res_2d = QHBoxLayout(self.ui.t_res_2d)
        hL_pdb_2d = QHBoxLayout(self.ui.t_pdb_2d)
        hL_res_3d = QHBoxLayout(self.ui.t_res_3d)
        hL_pdb_3d = QHBoxLayout(self.ui.t_pdb_3d)
        hL_res_2d.addWidget(self.canvas_res_2d)
        hL_pdb_2d.addWidget(self.canvas_pdb_2d)
        hL_res_3d.addWidget(self.canvas_res_3d)
        hL_pdb_3d.addWidget(self.canvas_pdb_3d)
        self.ui.pB_detail_2d.clicked.connect(self._draw_2d)

    def update_and_draw(self, result, pair=None):
        self.result = result
        self.pair = pair if pair else {}
        self._draw_2d()
        self._draw_3d()

    def _draw_2d(self):
        if self.result is None:
            print('未找到绘图所需的匹配结果和映射关系...')
            return
        pd = self.project_direction()
        self.res_2d[1].clear()
        self.pdb_2d[1].clear()
        self.result.target.draw_graph(self.res_2d[1], self.pair.keys(), direction=pd, rotation=self.result.rotation)
        self.result.query.draw_graph(self.pdb_2d[1], self.pair.values(), direction=pd)
        self.canvas_res_2d.draw()
        self.canvas_pdb_2d.draw()

    def _draw_3d(self):
        if self.result is None:
            print('未找到绘图所需的匹配结果...')
            return
        self.result.target.draw_3d_graph(self.res_3d, highlight=self.pair.keys())
        self.result.query.draw_3d_graph(self.pdb_3d, highlight=self.pair.values())
        self.canvas_res_3d.draw()
        self.canvas_pdb_3d.draw()

    def project_direction(self):
        text = self.ui.lE_detail_2d.text()
        if text == '':
            return tuple([0.0, 0.0, 1.0])
        match = re.match(r'[(](.*),(.*),(.*)[)]', text)
        pd = tuple([float(match.group(i + 1)) for i in range(3)])
        return pd

