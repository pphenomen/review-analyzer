import json
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing.text import tokenizer_from_json # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences # type: ignore

class LSTMPredictor:
    def __init__(self, model_path, tokenizer_path, max_len=200):
        self.max_len = max_len
        self.model = load_model(model_path)
        with open(tokenizer_path, "r", encoding="utf-8") as f:
            self.tokenizer = tokenizer_from_json(f.read())

    def preprocess_text(self, text):
        sequence = self.tokenizer.texts_to_sequences([text])
        return pad_sequences(sequence, maxlen=self.max_len)

    def predict(self, data):
        if isinstance(data, str):
            return self._predict_one(data)
        
        if isinstance(data, list):
            # если это список строк, добавим None для звёзд
            if isinstance(data[0], str):
                data = [(t, None) for t in data]
            return self._predict_many(data)
        
        raise TypeError("Формат данных должен быть строкой или списком (строк или кортежей)")

    def _predict_one(self, text):
        processed = self.preprocess_text(text)
        pred = self.model.predict(processed, verbose=0)[0]
        return "Позитивный" if pred[1] > pred[0] else "Негативный"

    def _predict_many(self, data):
        results = []
        for text, stars in data:
            sentiment = self._predict_one(text)
            results.append((text, sentiment, stars))
        return results