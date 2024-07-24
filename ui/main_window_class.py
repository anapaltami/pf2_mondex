import sqlite3
import pandas as pd
from PyQt5.QtWidgets import (
    QVBoxLayout, QLineEdit, QWidget, QPushButton, QTableWidgetItem, QTableWidget, QFormLayout, QSpinBox, QComboBox,
    QLabel, QTabWidget, QTextEdit, QHBoxLayout, QHeaderView
)
from src.config import DB_FILE
from models.pf2_newmon_model import NewMonsterModel
import logging

logging.basicConfig(level=logging.DEBUG)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.model = NewMonsterModel()
        self.model.ensure_model_exists(level=0)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # init tab widget
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # add tabs
        self.tabs.addTab(self.search_tab(), "Search Monsters")
        self.tabs.addTab(self.generation_tab(), "Generate Monsters")
        self.tabs.addTab(self.legality_tab(), "Legal License Notes")

        # set layout
        self.setLayout(self.layout)
        self.setWindowTitle('PF2 Monster Dex')
        self.setGeometry(100, 100, 800, 600)

        # load data table on startup
        self.load_data()

    def search_tab(self):
        search_tab = QWidget()
        layout = QHBoxLayout()

        # left panel for search and table
        left_panel = QVBoxLayout()

        # search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText('Search by name or trait')
        self.search_bar.textChanged.connect(self.search)  # dynamic searching
        left_panel.addWidget(self.search_bar)

        # search button
        self.search_button = QPushButton('Search', self)
        self.search_button.clicked.connect(self.search)
        left_panel.addWidget(self.search_button)

        # data display table
        self.table = QTableWidget(self)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.itemSelectionChanged.connect(self.display_monster_details)
        left_panel.addWidget(self.table)

        layout.addLayout(left_panel)

        # right panel for monster details
        self.details_panel = QVBoxLayout()
        self.details_label = QLabel("Select a monster to see its details.")
        self.details_panel.addWidget(self.details_label)

        layout.addLayout(self.details_panel)
        search_tab.setLayout(layout)
        return search_tab

    def generation_tab(self):
        generate_tab = QWidget()
        layout = QHBoxLayout()

        # left panel for generation elements
        left_panel = QVBoxLayout()

        # PF2 monster generation elements
        self.form_layout = QFormLayout()
        self.level_input = QSpinBox()
        self.level_input.setRange(-1, 25)
        self.trait_input = QComboBox()
        self.trait_input.addItems(self.get_monster_traits())
        self.generate_button = QPushButton('Generate Monster')
        self.generate_button.clicked.connect(self.generate_monster)
        self.form_layout.addRow(QLabel('Level'), self.level_input)
        self.form_layout.addRow(QLabel('Trait'), self.trait_input)
        self.form_layout.addWidget(self.generate_button)
        left_panel.addLayout(self.form_layout)

        layout.addLayout(left_panel)

        # right panel for generated monster details
        self.generated_details_panel = QVBoxLayout()
        self.generated_details_label = QLabel("Generate a monster to see its details.")
        self.generated_details_panel.addWidget(self.generated_details_label)

        layout.addLayout(self.generated_details_panel)
        generate_tab.setLayout(layout)
        return generate_tab

    def legality_tab(self):
        legal_tab = QWidget()
        layout = QVBoxLayout()

        # legal license notes
        self.license_text = QTextEdit(self)
        self.license_text.setReadOnly(True)
        self.license_text.setText(
            "Legal License Notes:\n\n"
            "This product is licensed under the ORC License located at the Library of Congress at TX 9-307-067 and "
            "available online at various locations. All warranties are disclaimed as set forth therein.\n\n"
            "This product is based on the following Licensed Material: PF2 Monster Dex, © 2024, Developed by "
            "Anastasia Altamirano.\n\n"
            "If you use our Licensed Material in your own published works, please credit us as follows: "
            "PF2 Monster Dex, © 2024, Developed by Anastasia Altamirano.\n\n"
            "Reserved Material elements in this product include, but may not be limited to: "
            "Specific characters, world lore.\n\n"
            "The following elements are owned by the Licensor and would otherwise constitute Reserved Material and "
            "are hereby designated as Licensed Material: General monster statblocks, game rules, and mechanics.\n"
        )

        layout.addWidget(self.license_text)
        legal_tab.setLayout(layout)
        return legal_tab

    def load_data(self, query=""):
        conn = sqlite3.connect(DB_FILE)
        if query:
            sql_query = (f"SELECT Name, Traits FROM pf2_monsters "
                         f"WHERE Name LIKE '%{query}%' OR Traits LIKE '%{query}%'")
        else:
            sql_query = f"SELECT Name, Level, Traits FROM pf2_monsters"
        df = pd.read_sql_query(sql_query, conn)
        conn.close()

        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)

        for row_index, row in df.iterrows():
            for col_index, col in enumerate(df.columns):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(row[col])))

    def search(self):
        query = self.search_bar.text()
        self.load_data(query)

    def display_monster_details(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return

        selected_name = selected_items[0].text()
        conn = sqlite3.connect(DB_FILE)
        query = f"SELECT * FROM pf2_monsters WHERE Name = ?"
        df = pd.read_sql_query(query, conn, params=(selected_name,))
        conn.close()

        if df.empty:
            return

        monster = df.iloc[0]
        details = f"Name: {monster['Name']}\nTraits: {monster['Traits']}\n"
        details += f"Level: {monster['Level']}\nStr: {monster['Str']}\nDex: {monster['Dex']}\n"
        details += f"Con: {monster['Con']}\nInt: {monster['Int']}\nWis: {monster['Wis']}\nCha: {monster['Cha']}\n"
        # TODO Add more details to display

        self.details_label.setText(details)

    def get_monster_traits(self):
        conn = sqlite3.connect(DB_FILE)
        query = f"SELECT DISTINCT `Traits` FROM pf2_monsters"
        df = pd.read_sql_query(query, conn)
        conn.close()
        all_traits = df['Traits'].str.split(',').explode().str.strip().unique()
        return sorted(all_traits.tolist())

    def generate_monster(self):
        level = self.level_input.value()
        monster_trait = self.trait_input.currentText()
        logging.debug(f"Generating monster with level: {level} and trait: {monster_trait}")
        new_monster_block = self.model.predict(level, trait=monster_trait)
        if new_monster_block is not None:
            self.display_generated_monster(new_monster_block)
        else:
            self.show_message(f"No data available for trait: {monster_trait}")

    def display_generated_monster(self, new_monster_block):
        level = self.level_input.value()
        monster_trait = self.trait_input.currentText()
        details = f'Level {level} {monster_trait} Monster:\n'
        for stat, value in new_monster_block.items():
            details += f'{stat}: {value}\n'
        self.generated_details_label.setText(details)

    def show_message(self, message):
        msg = QLabel(message)
        msg.setWordWrap(True)
        self.layout.addWidget(msg)
