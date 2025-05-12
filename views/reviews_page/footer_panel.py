from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from views.helpers.styles import LabelStyles
from views.helpers.buttons_factory import create_button, create_combo

class FooterPanel(QWidget):
    def __init__(self, controller, on_combo_change, on_model_updated, reset_filters):
        super().__init__()
        self.controller = controller
        self.on_combo_change = on_combo_change
        self.on_model_updated = on_model_updated
        self.reset_filters = reset_filters

    def build_footer(self) -> QHBoxLayout:
        footer = QHBoxLayout()

        self.review_count_label = QLabel("Количество отзывов: 0")
        self.review_count_label.setStyleSheet(LabelStyles.review_text())

        model_label = QLabel("Модель:")
        model_label.setStyleSheet(LabelStyles.review_text())
        self.model_selector = create_combo(["RuBERT", "LSTM"], self.handle_model_change)

        chart_label = QLabel("Диаграмма:")
        chart_label.setStyleSheet(LabelStyles.review_text())
        self.chart_selector = create_combo(["Круговая", "Гистограмма"], self.on_combo_change)
        plot_button = create_button("Построить диаграмму", self.handle_plot_chart)

        footer.addWidget(self.review_count_label, alignment=Qt.AlignLeft)
        footer.addStretch()
        footer.addWidget(model_label)
        footer.addWidget(self.model_selector)
        footer.addWidget(chart_label)
        footer.addWidget(self.chart_selector)
        footer.addWidget(plot_button)

        return footer

    def handle_model_change(self, model_name):
        self.controller.set_model_strategy(model_name)
        self.reset_filters()
        self.on_model_updated(model_name)

    def update_review_count(self, count: int):
        self.review_count_label.setText(f"Количество отзывов: {count}")

    def handle_plot_chart(self):
        selected = self.chart_selector.currentText()
        if selected == "Круговая":
            self.controller.plot_sentiment_pie_chart()
        elif selected == "Гистограмма":
            self.controller.plot_rating_histogram_chart()