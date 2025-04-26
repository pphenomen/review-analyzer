from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QHBoxLayout
from PyQt5.QtCore import Qt

class ReviewsPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        layout.addWidget(self.build_title())
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

    def build_review_card(self, text, sentiment, stars):
        frame = QFrame()
        frame.setStyleSheet("""
            background-color: #ffffff;
            border: 1px solid #E0E0E0;
            border-radius: 10px;
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