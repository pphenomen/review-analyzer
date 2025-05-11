from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

class TransformerPredictor:
    def __init__(self, model_path="models/transformer/model", max_len=128, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.max_len = max_len
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.to(self.device)
        self.model.eval()

    def preprocess_text(self, text):
        return self.tokenizer(
            text,
            padding="max_length",
            truncation=True,
            max_length=self.max_len,
            return_tensors="pt"
        ).to(self.device)

class TransformerPredictor:
    def __init__(self, model_path="models/transformer/model", max_len=128, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.max_len = max_len
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.model.to(self.device)
        self.model.eval()

        self.label_map = {0: "Негативный", 1: "Нейтральный", 2: "Позитивный"}

    def preprocess_text(self, text):
        return self.tokenizer(
            text,
            padding="max_length",
            truncation=True,
            max_length=self.max_len,
            return_tensors="pt"
        ).to(self.device)

    def predict(self, data):
        if isinstance(data, str):
            return self._predict_one(data)

        if isinstance(data, list):
            if isinstance(data[0], str):
                data = [(t, None) for t in data]
            return self._predict_many(data)

        raise TypeError("Формат данных должен быть строкой или списком (строк или кортежей)")

    def _predict_one(self, text):
        inputs = self.preprocess_text(text)
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = F.softmax(outputs.logits, dim=1)
            predicted_class = torch.argmax(probs, dim=1).item()
        return self.label_map[predicted_class]

    def _predict_many(self, data):  # data = [(text, stars), ...]
        results = []
        for text, stars in data:
            sentiment = self._predict_one(text)
            results.append((text, sentiment, stars))
        return results

