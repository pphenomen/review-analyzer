from models.strategies.base_strategy import ModelStrategy

class TransformerStrategy(ModelStrategy):
    def __init__(self, predictor):
        self.predictor = predictor

    def predict(self, texts):
        return self.predictor.predict(texts)
