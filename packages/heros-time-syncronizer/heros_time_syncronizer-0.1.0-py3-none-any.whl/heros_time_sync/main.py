import sys
from PyQt5.QtWidgets import QApplication, QWidget

from main_controller import MainController
from main_ui import Ui_Form


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("server time settings")
        self.show()


def main():
    app = QApplication(sys.argv)
    main_widget = MainWidget()
    main_controller = MainController(main_widget)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()