import pandas as pd

class DataHandler:
    def __init__(self):
        self.reviews = []
        self.sentiment_counts = {"positive": 0, "negative": 0}

    def load_data(self, file_path):
        self.reviews = []
        self.sentiment_counts = {"positive": 0, "negative": 0}
        df = pd.read_excel(file_path)
        if "Описание" not in df.columns or "Звезды" not in df.columns:
            raise ValueError("Некорректный формат файла!")
        df = df.dropna(subset=["Описание", "Звезды"])
        self.df = df

    def analyze_data(self, predictor):
        for _, row in self.df.iterrows():
            text = row["Описание"].strip()
            stars = row["Звезды"]
            sentiment = predictor.predict(text)
            if sentiment == "Позитивный":
                self.sentiment_counts["positive"] += 1
            else:
                self.sentiment_counts["negative"] += 1
            self.reviews.append((text, sentiment, stars))

    def get_reviews(self):
        return self.reviews

    def get_sentiment_counts(self):
        return self.sentiment_counts