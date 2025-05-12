from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QHBoxLayout, QComboBox
from PyQt5.QtCore import Qt
from .filters_panel import FiltersPanel
from .footer_panel import FooterPanel
from .reviews_card import ReviewsCard
from views.helpers.styles import LabelStyles
from views.helpers.buttons_factory import create_button

class ReviewsPage(QWidget):
    def __init__(self, controller, _unused):
        super().__init__()
        self.controller = controller
        self.filters_panel = FiltersPanel(self.controller, self.apply_filters_clicked)
        self.card_builder = ReviewsCard()
        self.page_title = QLabel("Отзывы")
        self.page_title.setStyleSheet(LabelStyles.page_title())
        self.footer_panel = FooterPanel(controller=self.controller, on_combo_change=self.apply_filters_clicked)
        self.model_description_label = QLabel()
        self.all_reviews = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(15)

        title_layout = QHBoxLayout()
        model_label = QLabel("Модель:")
        model_label.setStyleSheet(LabelStyles.review_text())
        self.model_selector = QComboBox()
        self.model_selector.addItems(["RuBERT", "LSTM"])
        self.model_selector.currentTextChanged.connect(self.on_model_changed)
        
        self.page_title.setStyleSheet(LabelStyles.page_title())
        self.page_title.setAlignment(Qt.AlignCenter)
        
        back_button = create_button("Назад", self.controller.go_to_start_page)

        title_layout.addWidget(model_label)
        title_layout.addWidget(self.model_selector)
        title_layout.addWidget(self.page_title, stretch=1)
        title_layout.addStretch()
        title_layout.addWidget(back_button)

        layout.addLayout(title_layout)
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

    def on_model_changed(self, model_name):
        self.controller.set_model_strategy(model_name)
        self.filters_panel.reset_filters()
        self.update_model_description(model_name)
    
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

    def update_model_description(self, model_name: str):
        sentiments = self.controller.get_available_sentiments()
        self.filters_panel.sentiment_combo.clear()
        self.filters_panel.sentiment_combo.addItem("Все")
        self.filters_panel.sentiment_combo.addItems(sentiments)

        if self.controller.data_handler.df is not None:
            reviews = self.controller.data_handler.get_all_reviews()
            predicted = self.controller.model_strategy.predict(reviews)
            self.controller.data_handler.set_predicted_reviews(predicted)
            self.display_reviews(predicted)