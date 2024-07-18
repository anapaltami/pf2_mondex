import sqlite3
import joblib
import numpy as np
import pandas as pd
from src.config import DB_FILE, AI_FOLDER, MODEL_FILE
from sklearn.linear_model import LinearRegression


class PokemonModel:
    def __init__(self):
        self.model_file = MODEL_FILE
        self.model = None

    def train(self):
        conn = sqlite3.connect(DB_FILE)
        query = "SELECT * FROM pokemon"
        df = pd.read_sql_query(query, conn)
        conn.close()

        # set input and output features
        X = df[['Total']]
        y = df[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']]

        # training
        self.model = LinearRegression()
        self.model.fit(X, y)

        # save model
        self.model_file.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, (AI_FOLDER / 'pokemon_model.pkl'))

    def load_model(self):
        if self.model is None:
            self.model = joblib.load(self.model_file)

    def predict(self, total_power):
        if self.model is None:
            self.load_model()

        input_df = pd.DataFrame({'Total': [total_power]})

        pred_stats = self.model.predict(input_df)
        pred_stats = np.round(pred_stats).astype(int).flatten()
        columns = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
        return dict(zip(columns, pred_stats))

    def ensure_model_exists(self):
        if not self.model_file.exists():
            self.train()
