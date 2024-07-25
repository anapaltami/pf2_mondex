import sys

from PyQt5.QtWidgets import QApplication
from ui.main_window_class import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle('PF2 Monster Dex')
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
