import sys

from PyQt5.QtWidgets import QApplication

from crystalsearchgui.main import MainUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainUI()
    window.show()
    sys.exit(app.exec_())
