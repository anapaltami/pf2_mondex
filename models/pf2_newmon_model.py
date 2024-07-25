import os
import sqlite3
import joblib
import numpy as np
import pandas as pd
import logging
from src.config import DB_FILE, MODEL_FILE
from sklearn.linear_model import LinearRegression

logging.basicConfig(level=logging.DEBUG)


class NewMonsterModel:
    def __init__(self):
        self.model_file = MODEL_FILE
        self.model = None

    def train(self, level=None, trait=None):
        logging.debug(f"Training model with trait: {trait} and level: {level}")
        conn = sqlite3.connect(DB_FILE)
        query = "SELECT * FROM pf2_monsters"
        df = pd.read_sql_query(query, conn)
        conn.close()

        if trait:
            df_trait = df[df['Traits'].str.contains(trait, case=False, na=False)]
            logging.debug(f"Filtered DataFrame shape for trait '{trait}': {df_trait.shape}")

            if df_trait.empty:
                logging.warning(f"No data found for trait: {trait}")
                df_trait = df

        else:
            df_trait = df

        if level is not None:
            df_level = df_trait[(df_trait['Level'] == level) | (df_trait['Level'] == level + 1) |
                                (df_trait['Level'] == level - 1)]
            logging.debug(f"Filtered DataFrame shape for level '{level}': {df_level.shape}")

            if df_level.empty:
                logging.warning(f"No data found for level: {level} and trait: {trait}")
                df_level = df[(df['Level'] == level) | (df['Level'] == level + 1) | (df['Level'] == level - 1)]
                logging.debug(f"Filtered DataFrame shape for level '{level}' with any trait: {df_level.shape}")

                if df_level.empty:
                    logging.warning(f"No data found for level: {level}")
                    return False

        else:
            df_level = df_trait

        # set input and output features
        X = df_level[['Level']]
        y = df_level[['Str', 'Dex', 'Con', 'Int', 'Wis', 'Cha']]

        # training
        self.model = LinearRegression()
        self.model.fit(X, y)

        # save model
        os.makedirs(os.path.dirname(self.model_file), exist_ok=True)
        joblib.dump(self.model, self.model_file)
        return True

    def load_model(self):
        if self.model is None:
            self.model = joblib.load(self.model_file)

    def predict(self, level, trait=None):
        success = self.train(level, trait)
        if not success:
            logging.error(f"Failed to train model for level: {level} and trait: {trait}")
            return None

        input_df = pd.DataFrame({'Level': [level]})

        pred_stats = self.model.predict(input_df)
        pred_stats = np.round(pred_stats).astype(int).flatten()
        columns = ['Str', 'Dex', 'Con', 'Int', 'Wis', 'Cha']
        return dict(zip(columns, pred_stats))

    def ensure_model_exists(self, level, trait=None):
        if not os.path.exists(self.model_file):
            self.train(level, trait)
