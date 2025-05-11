from abc import ABC, abstractmethod

class ModelStrategy(ABC):
    @abstractmethod
    def predict(self, texts: list[str]) -> list[str]:
        pass
