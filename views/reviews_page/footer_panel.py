from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QComboBox
from PyQt5.QtCore import Qt
from views.helpers.styles import LabelStyles
from views.helpers.buttons_factory import create_button, create_combo

class FooterPanel(QWidget):
    def __init__(self, controller, on_combo_change):
        super().__init__()
        self.controller = controller
        self.on_combo_change = on_combo_change

    def build_footer(self) -> QHBoxLayout:
        footer = QHBoxLayout()

        self.review_count_label = QLabel("Количество отзывов: 0")
        self.review_count_label.setStyleSheet(LabelStyles.review_text())

        self.chart_selector = create_combo(["Круговая", "Гистограмма"], self.on_combo_change)
        plot_button = create_button("Построить диаграмму", self.handle_plot_chart)
        back_button = create_button("Назад", self.controller.go_to_start_page)

        footer.addWidget(self.review_count_label, alignment=Qt.AlignLeft)
        footer.addStretch()
        footer.addWidget(self.chart_selector)
        footer.addWidget(plot_button, alignment=Qt.AlignRight)
        footer.addWidget(back_button, alignment=Qt.AlignRight)

        return footer

    def update_review_count(self, count: int):
        self.review_count_label.setText(f"Количество отзывов: {count}")
        
    def handle_plot_chart(self):
        selected = self.chart_selector.currentText()
        if selected == "Круговая":
            self.controller.plot_sentiment_pie_chart()
        elif selected == "Гистограмма":
            self.controller.plot_rating_histogram_chart()
