from utils.filters.base_filter import ReviewFilter

class StarsFilter(ReviewFilter):
    def __init__(self, wrapped, stars):
        super().__init__(wrapped.filter())
        self.stars = stars

    def filter(self):
        return [review for review in self.reviews if review[2] == self.stars]
