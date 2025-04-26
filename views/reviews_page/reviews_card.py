from PyQt5.QtWidgets import QWidget, QFrame, QLabel, QVBoxLayout
from views.helpers.styles import LabelStyles, FrameStyles

class ReviewsCard(QWidget):
    def __init__(self):
        super().__init__()

    def build_review_card(self, text: str, sentiment: str, stars: int) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet(FrameStyles.default())

        layout = QVBoxLayout()
        review_text = QLabel(f"<b>Отзыв:</b> {text}")
        review_text.setWordWrap(True)
        review_text.setStyleSheet(LabelStyles.description())

        sentiment_label = QLabel(f"<b>Тональность:</b> {sentiment}")
        sentiment_label.setStyleSheet(LabelStyles.description())

        stars_label = QLabel("⭐" * stars)
        stars_label.setStyleSheet(LabelStyles.star())

        layout.addWidget(review_text)
        layout.addWidget(stars_label)
        layout.addWidget(sentiment_label)

        frame.setLayout(layout)
        return frame
