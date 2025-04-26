from utils.filters.base_filter import ReviewFilter

class KeywordFilter(ReviewFilter):
    def __init__(self, wrapped, keyword):
        super().__init__(wrapped.filter())
        self.keyword = keyword.lower()

    def filter(self):
        return [review for review in self.reviews if self.keyword in review[0].lower()]
    
