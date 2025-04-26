from utils.filters.base_filter import ReviewFilter

class SentimentFilter(ReviewFilter):
    def __init__(self, wrapped, sentiment):
        super().__init__(wrapped.filter())
        self.sentiment = sentiment

    def filter(self):
        if self.sentiment == "Все":
            return self.reviews
        
        return [review for review in self.reviews if review[1] == self.sentiment]
        
