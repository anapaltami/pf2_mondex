from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from src.config import STYLE_SHEET
from ui.search_tab import SearchTab
from ui.generation_tab import GenerationTab
from ui.legal_tab import LegalTab
import logging

logging.basicConfig(level=logging.DEBUG)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.apply_stylesheet()

    def apply_stylesheet(self):
        with open(STYLE_SHEET, 'r') as f:
            self.setStyleSheet(f.read())

    def initUI(self):
        self.layout = QVBoxLayout()

        # init tab widget
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # add tabs
        self.tabs.addTab(SearchTab(self), "Search Monsters")
        self.tabs.addTab(GenerationTab(self), "Generate Monsters")
        self.tabs.addTab(LegalTab(self), "Legal License Notes")

        # set layout
        self.setLayout(self.layout)
        self.setWindowTitle('PF2 Monster Dex')
        self.setGeometry(100, 100, 800, 600)
