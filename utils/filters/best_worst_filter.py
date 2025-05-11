from utils.filters.base_filter import ReviewFilter

class BestWorstFilter(ReviewFilter):
    def __init__(self, wrapped, sort_order="Сначала лучшие"):
        super().__init__(wrapped.filter())
        self.sort_order = sort_order

    def sort_reviews(self):
        sentiment_priority = {
            "Позитивный": 1,
            "Нейтральный": 2,
            "Негативный": 3
        }

        # сортировка по тональности
        sorted_reviews = sorted(
            self.reviews,
            key=lambda review: sentiment_priority.get(review[1], 4)
        )

        if self.sort_order == "Сначала лучшие":
            return sorted_reviews
        else:
            return sorted_reviews[::-1]

    def filter(self):
        return self.sort_reviews()