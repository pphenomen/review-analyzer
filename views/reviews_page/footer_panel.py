from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from views.helpers.styles import LabelStyles
from views.helpers.buttons_factory import create_button

class FooterPanel(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    def build_footer(self) -> QHBoxLayout:
        footer = QHBoxLayout()

        self.review_count_label = QLabel("Количество отзывов: 0")
        self.review_count_label.setStyleSheet(LabelStyles.review_text())

        plot_button = create_button("Построить диаграмму", self.controller.plot_reviews_chart)
        back_button = create_button("Назад", self.controller.go_to_start_page)

        footer.addWidget(self.review_count_label, alignment=Qt.AlignLeft)
        footer.addStretch()
        footer.addWidget(plot_button, alignment=Qt.AlignRight)
        footer.addWidget(back_button, alignment=Qt.AlignRight)

        return footer

    def update_review_count(self, count: int):
        self.review_count_label.setText(f"Количество отзывов: {count}")