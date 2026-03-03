import sqlite3
import pandas as pd
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QTableWidget, QHeaderView, \
    QLabel, QTableWidgetItem
from src.config import DB_FILE, GENERATED_DB_FILE


class SearchTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()

        # left panel for search and table
        left_panel = QVBoxLayout()

        # search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText('Search by name or trait')
        self.search_bar.textChanged.connect(self.search)
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

        # right panel for monster details
        self.details_panel = QVBoxLayout()
        self.details_label = QLabel("Select a monster to see its details.")
        self.details_panel.addWidget(self.details_label)

        layout.addLayout(left_panel)
        layout.addLayout(self.details_panel)
        self.setLayout(layout)

        self.load_data()

    def load_data(self, query=""):
        columns = ['Name', 'Level', 'Traits']

        # load and query PF2 monster database
        conn_main = sqlite3.connect(DB_FILE)
        try:
            if query:
                like = f"%{query}%"
                sql_query = (
                    "SELECT Name, Level, Traits FROM pf2_monsters "
                    "WHERE Name LIKE ? OR Traits LIKE ?"
                )
                df_main = pd.read_sql_query(sql_query, conn_main, params=(like, like))
            else:
                sql_query = "SELECT Name, Level, Traits FROM pf2_monsters"
                df_main = pd.read_sql_query(sql_query, conn_main)
        finally:
            conn_main.close()

        # load and query user generated monster database (if it exists)
        try:
            conn_generated = sqlite3.connect(GENERATED_DB_FILE)
            try:
                if query:
                    like = f"%{query}%"
                    sql_query = (
                        "SELECT Name, Level, Traits FROM generated_monsters "
                        "WHERE Name LIKE ? OR Traits LIKE ?"
                    )
                    df_generated = pd.read_sql_query(sql_query, conn_generated, params=(like, like))
                else:
                    sql_query = "SELECT Name, Level, Traits FROM generated_monsters"
                    df_generated = pd.read_sql_query(sql_query, conn_generated)
            finally:
                conn_generated.close()
        except (sqlite3.OperationalError, sqlite3.DatabaseError):
            # generated database or table might not exist yet
            df_generated = pd.DataFrame(columns=columns)

        df_combined = pd.concat([df_main, df_generated], ignore_index=True)

        self.table.setRowCount(len(df_combined))
        self.table.setColumnCount(len(df_combined.columns))
        self.table.setHorizontalHeaderLabels(df_combined.columns)

        for row_index, row in df_combined.iterrows():
            for col_index, col in enumerate(df_combined.columns):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(row[col])))

    def search(self):
        query = self.search_bar.text()
        self.load_data(query)

    def display_monster_details(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return

        selected_name = selected_items[0].text()
        conn_main = sqlite3.connect(DB_FILE)
        try:
            query = "SELECT * FROM pf2_monsters WHERE Name = ?"
            df_main = pd.read_sql_query(query, conn_main, params=(selected_name,))
        finally:
            conn_main.close()

        try:
            conn_generated = sqlite3.connect(GENERATED_DB_FILE)
            try:
                query = "SELECT * FROM generated_monsters WHERE Name = ?"
                df_generated = pd.read_sql_query(query, conn_generated, params=(selected_name,))
            finally:
                conn_generated.close()
        except (sqlite3.OperationalError, sqlite3.DatabaseError):
            df_generated = pd.DataFrame()

        df_combined = pd.concat([df_main, df_generated], ignore_index=True)

        if df_combined.empty:
            return

        monster = df_combined.iloc[0]
        details = (f"Name: {monster['Name']}\nTraits: {monster['Traits']}\nLevel: {monster['Level']}\n"
                   f"Str: {monster['Str']}\nDex: {monster['Dex']}\nCon: {monster['Con']}\nInt: {monster['Int']}\n"
                   f"Wis: {monster['Wis']}\nCha: {monster['Cha']}\n")
        # TODO Add more details to display

        self.details_label.setText(details)
