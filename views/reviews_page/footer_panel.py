from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt

class FooterPanel(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    def build_footer(self) -> QHBoxLayout:
        footer = QHBoxLayout()

        self.review_count_label = QLabel("Количество отзывов: 0")
        self.review_count_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2F2F2F;")

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

    def update_review_count(self, count: int):
        self.review_count_label.setText(f"Количество отзывов: {count}")

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