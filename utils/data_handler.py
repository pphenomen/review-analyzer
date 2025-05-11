import pandas as pd
from collections import defaultdict

class DataHandler:
    def __init__(self):
        self.df = None
        self.reviews = []
        self.sentiment_counts = defaultdict(int)

    def load_data(self, file_path):
        self.reviews.clear()
        self.sentiment_counts.clear()

        df = pd.read_excel(file_path)
        if "Описание" not in df.columns or "Звезды" not in df.columns:
            raise ValueError("Некорректный формат файла! Отзывы для анализа не найдены")
        
        df = df.dropna(subset=["Описание", "Звезды"])
        self.df = df

    def analyze_data(self, predictor):
        self.reviews.clear()
        self.sentiment_counts.clear()

        for _, row in self.df.iterrows():
            text = str(row["Описание"]).strip()
            stars = row["Звезды"]
            sentiment = predictor.predict(text)

            self.sentiment_counts[sentiment] += 1
            self.reviews.append((text, sentiment, stars))

    def get_reviews(self):
        return self.reviews

    def get_sentiment_counts(self):
        return self.sentiment_counts

    def get_all_reviews(self):
        return [(str(row["Описание"]).strip(), row["Звезды"]) for _, row in self.df.iterrows()]
