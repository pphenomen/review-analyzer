from utils.filters.base_filter import ReviewFilter

class SentimentFilter(ReviewFilter):
    def __init__(self, wrapped, sentiment, allowed_labels):
        super().__init__(wrapped.filter())
        self.sentiment = sentiment
        self.allowed_labels = allowed_labels

    def filter(self):
        if self.sentiment == "Все" or self.sentiment not in self.allowed_labels:
            return self.reviews
        
        return [review for review in self.reviews if review[1] == self.sentiment]
        
