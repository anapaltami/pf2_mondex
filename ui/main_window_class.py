import sqlite3
import pandas as pd
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QWidget, QPushButton, QTableWidgetItem, QTableWidget, QFormLayout, \
    QSpinBox, QComboBox, QLabel
from src.config import DB_FILE
from models.pokemon_model import PokemonModel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.model = PokemonModel()
        self.model.ensure_model_exists()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText('Search')
        self.layout.addWidget(self.search_bar)

        # search button
        self.search_button = QPushButton('Search', self)
        self.search_button.clicked.connect(self.search)
        self.layout.addWidget(self.search_button)

        # data display table
        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)

        # pokemon generation elements
        self.form_layout = QFormLayout()
        self.power_input = QSpinBox()
        self.power_input.setRange(1, 1000)
        self.type_input = QComboBox()
        self.type_input.addItems(self.get_pokemon_types())
        self.generate_button = QPushButton('Generate')
        self.generate_button.clicked.connect(self.generate_pokemon)
        self.form_layout.addRow(QLabel('Total Power'), self.power_input)
        self.form_layout.addRow(QLabel('Type'), self.type_input)
        self.form_layout.addWidget(self.generate_button)
        self.layout.addLayout(self.form_layout)

        self.setLayout(self.layout)
        self.setWindowTitle('Pokemon Dex Test')
        self.table.setSortingEnabled(True)
        self.load_data()

    def load_data(self, query=""):
        conn = sqlite3.connect(DB_FILE)
        if query:
            sql_query = f"SELECT * FROM Pokemon WHERE Name LIKE '{query}'"
        else:
            sql_query = f"SELECT * FROM Pokemon"
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

    def get_pokemon_types(self):
        conn = sqlite3.connect(DB_FILE)
        query = f"SELECT DISTINCT `Type 1` FROM Pokemon"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df['Type 1'].tolist()

    def generate_pokemon(self):
        total_power = self.power_input.value()
        pokemon_type = self.type_input.currentText()
        new_pokemon_stats = self.model.predict(total_power)
        if new_pokemon_stats is not None:
            self.display_generated_pokemon(new_pokemon_stats)

    def display_generated_pokemon(self, new_pokemon_stats):
        message = f'Generated Pokemon Stats:\n'
        for stat, value in new_pokemon_stats.items():
            message += f'{stat}: {value}\n'
        self.show_message(message)

    def show_message(self, message):
        msg = QLabel(message)
        msg.setWordWrap(True)
        self.layout.addWidget(msg)