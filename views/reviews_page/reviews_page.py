from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
from .filters_panel import FiltersPanel
from .footer_panel import FooterPanel
from .reviews_card import ReviewsCard

class ReviewsPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.filters_panel = FiltersPanel(self.apply_filters_clicked)
        self.footer_panel = FooterPanel(self.controller)
        self.card_builder = ReviewsCard()
        self.all_reviews = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        layout.addWidget(self.filters_panel.build())
        layout.addWidget(self.build_review_area())
        layout.addLayout(self.footer_panel.build_footer())

        self.setLayout(layout)

    def build_review_area(self) -> QScrollArea:
        self.review_area = QScrollArea()
        self.review_area.setWidgetResizable(True)

        self.reviews_widget = QWidget()
        self.reviews_layout = QVBoxLayout()
        self.reviews_layout.setAlignment(Qt.AlignTop)
        self.reviews_widget.setLayout(self.reviews_layout)

        self.review_area.setWidget(self.reviews_widget)
        return self.review_area

    def display_reviews(self, reviews: list):
        self.all_reviews = reviews

        for i in reversed(range(self.reviews_layout.count())):
            widget = self.reviews_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for text, sentiment, stars in reviews:
            review_frame = self.card_builder.build_review_card(text, sentiment, stars)
            self.reviews_layout.addWidget(review_frame)

        self.footer_panel.update_review_count(len(reviews))

    def apply_filters_clicked(self):
        sentiment = self.filters_panel.sentiment_combo.currentText()
        keyword = self.filters_panel.search_input.text()
        sort_order = self.filters_panel.sort_combo.currentText()
        stars_filter = self.filters_panel.stars_combo.currentText()

        filtered_reviews = self.controller.apply_filters(
            sentiment=sentiment,
            keyword=keyword,
            sort_order=sort_order,
            stars_filter=stars_filter
        )
        self.display_reviews(filtered_reviews)