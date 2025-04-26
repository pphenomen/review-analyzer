from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QHBoxLayout, QLineEdit, QComboBox, QGroupBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from utils.filters.base_filter import ReviewFilter
from utils.filters.sentiment_filter import SentimentFilter
from utils.filters.keyword_filter import KeywordFilter
from utils.filters.stars_filter import StarsFilter

class ReviewsPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.all_reviews = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        layout.addWidget(self.build_title())
        layout.addWidget(self.build_filters_panel())
        layout.addWidget(self.build_review_area())
        layout.addLayout(self.build_footer())

        self.setLayout(layout)

    def build_title(self) -> QLabel:
        title = QLabel("Список отзывов")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            color: #2F2F2F;
            margin-top: 20px;
            margin-bottom: 20px;
        """)
        return title

    def build_review_area(self) -> QScrollArea:
        self.review_area = QScrollArea()
        self.review_area.setWidgetResizable(True)

        self.reviews_widget = QWidget()
        self.reviews_layout = QVBoxLayout()
        self.reviews_layout.setAlignment(Qt.AlignTop)
        self.reviews_widget.setLayout(self.reviews_layout)

        self.review_area.setWidget(self.reviews_widget)
        return self.review_area

    def build_footer(self) -> QHBoxLayout:
        footer = QHBoxLayout()

        self.review_count_label = QLabel("Количество отзывов: 0")
        self.review_count_label.setStyleSheet("""
            font-size: 16px; 
            font-weight: bold; 
            color: #2F2F2F;
        """)

        plot_button = self.create_plot_button()
        back_button = self.create_back_button()

        footer.addWidget(self.review_count_label, alignment=Qt.AlignLeft)
        footer.addStretch()
        footer.addWidget(plot_button, alignment=Qt.AlignRight)
        footer.addWidget(back_button, alignment=Qt.AlignRight)

        return footer

    def create_plot_button(self) -> QPushButton:
        button = QPushButton("Построить диаграмму")
        button.clicked.connect(self.controller.plot_reviews_chart)
        button.setStyleSheet(self.button_style())
        return button

    def create_back_button(self) -> QPushButton:
        button = QPushButton("Назад")
        button.clicked.connect(self.controller.go_to_start_page)
        button.setStyleSheet(self.button_style())
        return button

    def display_reviews(self, reviews: list):
        self.all_reviews = reviews

        for i in reversed(range(self.reviews_layout.count())):
            widget = self.reviews_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for text, sentiment, stars in reviews:
            review_frame = self.build_review_card(text, sentiment, stars)
            self.reviews_layout.addWidget(review_frame)

        self.review_count_label.setText(f"Количество отзывов: {len(reviews)}")

    def apply_filters_clicked(self):
        sentiment = self.sentiment_combo.currentText()
        keyword = self.search_input.text()
        sort_order = self.sort_combo.currentText()
        stars_filter = self.stars_combo.currentText()

        filtered_reviews = self.controller.apply_filters(sentiment=sentiment, keyword=keyword, sort_order=sort_order, stars_filter=stars_filter)
        self.display_reviews(filtered_reviews)

    def build_filters_panel(self) -> QGroupBox:
        group_box = self.create_filters_group_box()
        filter_layout = self.create_filter_layout()
        group_box.setLayout(filter_layout)
        return group_box

    def create_filters_group_box(self, title="Фильтрация") -> QGroupBox:
        group_box = QGroupBox(title)
        group_box.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
        """)
        return group_box

    def create_filter_layout(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        self.search_input = self.create_search_input()
        self.search_button = self.create_search_button()
        self.stars_combo = self.create_stars_combo()
        self.sort_combo = self.create_sort_combo()
        self.sentiment_combo = self.create_sentiment_combo()

        search_block = QHBoxLayout()
        search_block.addWidget(self.search_input)
        search_block.addWidget(self.search_button)

        search_block_widget = QWidget()
        search_block_widget.setLayout(search_block)

        layout.addWidget(search_block_widget)
        layout.addStretch()
        layout.addWidget(self.stars_combo)
        layout.addWidget(self.sort_combo)
        layout.addWidget(self.sentiment_combo)

        return layout

    def create_search_input(self) -> QLineEdit:
        search_input = QLineEdit()
        search_input.setPlaceholderText("Поиск по тексту...")
        search_input.setFixedWidth(250)
        search_input.setStyleSheet("""
            font-size: 14px;
            padding: 8px;
        """)
        search_input.textChanged.connect(self.on_search_text_changed)
        return search_input

    def on_search_text_changed(self, text: str):
        if text.strip() == "":
            self.apply_filters_clicked()

    def create_search_button(self) -> QPushButton:
        search_button = QPushButton("Найти")
        search_button.setFixedSize(80, 35)
        search_button.clicked.connect(self.apply_filters_clicked)
        search_button.setStyleSheet(self.button_style())
        return search_button

    def create_stars_combo(self) -> QComboBox:
        stars_combo = QComboBox()
        stars_combo.addItems(["Все оценки", "5 звезд", "4 звезды", "3 звезды", "2 звезды", "1 звезда"])
        stars_combo.setFixedWidth(150)
        stars_combo.setStyleSheet("""
            font-size: 14px;
            padding: 5px;
        """)
        stars_combo.currentIndexChanged.connect(self.apply_filters_clicked)
        return stars_combo

    def create_sort_combo(self) -> QComboBox:
        sort_combo = QComboBox()
        sort_combo.addItems(["По умолчанию", "Сначала лучшие", "Сначала худшие"])
        sort_combo.setFixedWidth(200)
        sort_combo.setStyleSheet("""
            font-size: 14px;
            padding: 5px;
        """)
        sort_combo.currentIndexChanged.connect(self.apply_filters_clicked)
        return sort_combo

    def create_sentiment_combo(self) -> QComboBox:
        sentiment_combo = QComboBox()
        sentiment_combo.addItems(["Все", "Позитивный", "Негативный"])
        sentiment_combo.setFixedWidth(200)
        sentiment_combo.setStyleSheet("""
            font-size: 14px;
            padding: 5px;
        """)
        sentiment_combo.currentIndexChanged.connect(self.apply_filters_clicked)
        return sentiment_combo

    def build_review_card(self, text: str, sentiment: str, stars: int) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet("""
            background-color: #ffffff;
            border: 1px solid #E0E0E0;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 10px;
        """)

        layout = QVBoxLayout()

        review_text = QLabel(f"<b>Отзыв:</b> {text}")
        review_text.setWordWrap(True)
        review_text.setStyleSheet("font-size: 16px; color: #333333;")

        sentiment_label = QLabel(f"<b>Тональность:</b> {sentiment}")
        sentiment_label.setStyleSheet("font-size: 16px; color: #333333;")

        stars_label = QLabel("⭐" * stars)
        stars_label.setStyleSheet("font-size: 18px; color: #FFD700;")

        layout.addWidget(review_text)
        layout.addWidget(stars_label)
        layout.addWidget(sentiment_label)

        frame.setLayout(layout)
        return frame

    def button_style(self) -> str:
        return """
            QPushButton {
                font-size: 14px;
                padding: 10px 20px;
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1c1c1c, stop:1 #3c3c3c
                );
                color: #ffffff;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background: #2d2d2d;
            }
        """
