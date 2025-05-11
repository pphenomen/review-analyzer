from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QComboBox, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from .filters_panel import FiltersPanel
from .footer_panel import FooterPanel
from .reviews_card import ReviewsCard
from views.helpers.styles import LabelStyles
from views.helpers.buttons_factory import create_combo

class ReviewsPage(QWidget):
    def __init__(self, controller, on_model_select):
        super().__init__()
        self.controller = controller
        self.on_model_select = on_model_select
        self.filters_panel = FiltersPanel(self.controller, self.apply_filters_clicked)
        self.footer_panel = FooterPanel(self.controller, self.apply_filters_clicked)
        self.card_builder = ReviewsCard()
        self.model_description_label = QLabel()
        self.all_reviews = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        
        layout.addWidget(self.model_description_label)
        
        model_label = QLabel("Модель:")
        model_label.setStyleSheet(LabelStyles.review_text())
        
        self.model_selector = create_combo(["RuBERT", "LSTM"], self.on_model_select)
        self.model_selector.currentTextChanged.connect(self.on_model_changed)
        
        model_select_layout = QHBoxLayout()
        model_select_layout.addWidget(model_label)
        model_select_layout.addWidget(self.model_selector)
        layout.addLayout(model_select_layout)
        
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
        
        # очищаем текущие отзывы
        for i in reversed(range(self.reviews_layout.count())):
            widget = self.reviews_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # добавляем новые отзывы
        for text, sentiment, stars in reviews:
            review_frame = self.card_builder.build_review_card(text, sentiment, stars)
            self.reviews_layout.addWidget(review_frame)

        # обновляем количество отзывов
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
    
    def on_model_changed(self, model_name):
        self.controller.set_model_strategy(model_name)
        self.filters_panel.reset_filters()
        self.update_model_description(model_name)
    
    def update_model_description(self, model_name: str):
        descriptions = {
        "LSTMStrategy": "<b>LSTM</b>: простая модель, бинарная классификация (позитив / негатив), средняя точность.",
        "TransformerStrategy": "<b>RuBERT</b>: трансформер, трёхклассовая классификация (позитив / нейтрально / негатив), высокая точность."
        }
        self.model_description_label.setText(descriptions.get(model_name, ""))
        
        sentiments = self.controller.get_available_sentiments()
        self.filters_panel.sentiment_combo.clear()
        self.filters_panel.sentiment_combo.addItem("Все")
        self.filters_panel.sentiment_combo.addItems(sentiments)

        # обновляем отзывы
        if self.controller.data_handler.df is not None:
            reviews = self.controller.data_handler.get_all_reviews()
            predicted = self.controller.model_strategy.predict(reviews)
            self.controller.data_handler.set_predicted_reviews(predicted)
            self.display_reviews(predicted)