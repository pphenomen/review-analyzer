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

    def build_title(self):
        title = QLabel("Список отзывов")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            color: #2F2F2F;
            margin-top: 20px;
            margin-bottom: 20px;
        """)
        return title

    def build_review_area(self):
        self.review_area = QScrollArea()
        self.review_area.setWidgetResizable(True)

        self.reviews_widget = QWidget()
        self.reviews_layout = QVBoxLayout()
        self.reviews_layout.setAlignment(Qt.AlignTop)
        self.reviews_widget.setLayout(self.reviews_layout)

        self.review_area.setWidget(self.reviews_widget)
        return self.review_area

    def build_footer(self):
        footer = QHBoxLayout()

        self.review_count_label = QLabel("Количество отзывов: 0")
        self.review_count_label.setStyleSheet("""
            font-size: 16px; 
            font-weight: bold; 
            color: #2F2F2F;
        """)

        plot_button = QPushButton("Построить диаграмму")
        plot_button.clicked.connect(self.controller.plot_reviews_chart)
        plot_button.setStyleSheet("""
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
        """)

        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.controller.go_to_start_page)
        back_button.setStyleSheet("""
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
        """)

        footer.addWidget(self.review_count_label, alignment=Qt.AlignLeft)
        footer.addStretch()
        footer.addWidget(plot_button, alignment=Qt.AlignRight)
        footer.addWidget(back_button, alignment=Qt.AlignRight)

        return footer

    def display_reviews(self, reviews):
        # сохраняем все отзывы
        self.all_reviews = reviews
        
        # очищаем старые отзывы
        for i in reversed(range(self.reviews_layout.count())):
            widget = self.reviews_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # добавляем новые отзывы
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
        
    def build_filters_panel(self):
        group_box = QGroupBox("Фильтрация")
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

        filter_layout = QHBoxLayout()

        # поле для поиска по ключевому слову
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по тексту...")
        self.search_input.setFixedWidth(250)
        self.search_input.setStyleSheet("""
            font-size: 14px;
            padding: 8px;
        """)
        
        # кнопка поиска по словам
        self.search_button = QPushButton()
        self.search_button.setText("Найти")
        self.search_button.setFixedSize(80, 35)
        self.search_button.clicked.connect(self.apply_filters_clicked)
        self.search_button.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 10px 20px;
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1c1c1c, stop:1 #3c3c3c
                );
                color: #ffffff;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background: #2d2d2d;
            }
        """)
        
        # layout поиска и кнопки
        search_block = QHBoxLayout()
        search_block.addWidget(self.search_input)
        search_block.addWidget(self.search_button)

        search_block_widget = QWidget()
        search_block_widget.setLayout(search_block)
        
        # выпадающий список по количеству звёзд
        self.stars_combo = QComboBox()
        self.stars_combo.addItems([
            "Все оценки",
            "5 звезд",
            "4 звезды",
            "3 звезды",
            "2 звезды",
            "1 звезда"
        ])
        self.stars_combo.setFixedWidth(150)
        self.stars_combo.setStyleSheet("""
            font-size: 14px;
            padding: 5px;
        """)
        self.stars_combo.currentIndexChanged.connect(self.apply_filters_clicked)
        
        # выпадающий список лучшие/худшие
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["По умолчанию", "Сначала лучшие", "Сначала худшие"])
        self.sort_combo.setFixedWidth(200)
        self.sort_combo.setStyleSheet("""
            font-size: 14px;
            padding: 5px;
        """)
        self.sort_combo.currentIndexChanged.connect(self.apply_filters_clicked)
        
        # выпадающий список по тональности
        self.sentiment_combo = QComboBox()
        self.sentiment_combo.addItems(["Все", "Позитивный", "Негативный"])
        self.sentiment_combo.setFixedWidth(200)
        self.sentiment_combo.setStyleSheet("""
            font-size: 14px;
            padding: 5px;
        """)
        self.sentiment_combo.currentIndexChanged.connect(self.apply_filters_clicked)

        filter_layout.addWidget(search_block_widget)
        filter_layout.addStretch()
        filter_layout.addWidget(self.stars_combo)
        filter_layout.addWidget(self.sort_combo)
        filter_layout.addWidget(self.sentiment_combo)

        group_box.setLayout(filter_layout)

        return group_box

    def build_review_card(self, text, sentiment, stars):
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
        review_text.setStyleSheet("""
            font-size: 16px;
            color: #333333;
        """)
        sentiment_label = QLabel(f"<b>Тональность:</b> {sentiment}")
        sentiment_label.setStyleSheet("""
            font-size: 16px;
            color: #333333;
        """)
        stars_label = QLabel("⭐" * stars)
        stars_label.setStyleSheet("font-size: 18px; color: #FFD700;")

        layout.addWidget(review_text)
        layout.addWidget(stars_label)
        layout.addWidget(sentiment_label)

        frame.setLayout(layout)
        return frame