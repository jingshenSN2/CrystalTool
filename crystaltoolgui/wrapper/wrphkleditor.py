from ..libs import *
from ..tabs import Ui_tabhkleditor


@singleton
class HklEditor(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = Ui_tabhkleditor()
        self.ui.setupUi(self)
