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
        self.figure_2d = plt.figure()
        self.axe1_2d = self.figure_2d.add_subplot(1, 2, 1)
        self.axe2_2d = self.figure_2d.add_subplot(1, 2, 2)
        self.figure_3d = plt.figure()
        self.canvas_2d = FigureCanvas(self.figure_2d)
        self.canvas_3d = FigureCanvas(self.figure_3d)
        self.ui.vL_detail_2d.addWidget(self.canvas_2d)
        self.ui.vL_detail_3d.addWidget(self.canvas_3d)
        self.ui.pB_detail_2d.clicked.connect(self._draw_2d)

    def update_and_draw(self, result=None, pair=None):
        if result is not None:
            self.result = result
        if pair is not None:
            self.pair = pair
            self._draw_2d()
        self._draw_3d()

    def _draw_2d(self):
        if self.result is None or self.pair is None:
            print('未找到绘图所需的匹配结果和映射关系...')
            return
        pd = self.project_direction()
        self.axe1_2d.clear()
        self.axe2_2d.clear()
        self.result.target.draw_graph(self.axe1_2d, self.pair.keys(), direction=pd, rotation=self.result.rotation)
        self.result.query.draw_graph(self.axe2_2d, self.pair.values(), direction=pd)
        self.canvas_2d.draw()

    def _draw_3d(self):
        if self.result is None:
            print('未找到绘图所需的匹配结果...')
            return
        self.result.target.draw_3d_graph(self.figure_3d, highlight=self.pair if self.pair is not None else [])
        self.canvas_3d.draw()

    def project_direction(self):
        text = self.ui.lE_detail_2d.text()
        if text == '':
            return tuple([0.0, 0.0, 1.0])
        match = re.match(r'[(](.*),(.*),(.*)[)]', text)
        pd = tuple([float(match.group(i + 1)) for i in range(3)])
        return pd

