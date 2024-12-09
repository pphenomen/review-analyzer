import json
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences

class SentimentPredictor:
    def __init__(self, model_path, tokenizer_path, max_len=200):
        self.max_len = max_len
        self.model = load_model(model_path)
        with open(tokenizer_path, "r", encoding="utf-8") as f:
            tokenizer_data = f.read()
            self.tokenizer = tokenizer_from_json(tokenizer_data)

    def preprocess_text(self, text):
        sequence = self.tokenizer.texts_to_sequences([text])
        return pad_sequences(sequence, maxlen=self.max_len)

    def predict(self, text):
        processed_text = self.preprocess_text(text)
        prediction = self.model.predict(processed_text, verbose=0)[0]
        sentiment = "Позитивный" if prediction[1] > prediction[0] else "Негативный"
        return sentiment
