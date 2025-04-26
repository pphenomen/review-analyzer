from PyQt5.QtWidgets import QWidget, QFrame, QLabel, QVBoxLayout

class ReviewsCard(QWidget):
    def __init__(self):
        super().__init__()

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
