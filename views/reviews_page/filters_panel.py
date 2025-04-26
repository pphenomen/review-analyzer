from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QComboBox, QPushButton, QGroupBox
from PyQt5.QtCore import Qt
from views.helpers.styles import ButtonStyles, LabelStyles, GroupBoxStyles

class FiltersPanel(QWidget):
    def __init__(self, on_filter_apply):
        super().__init__()
        self.on_filter_apply = on_filter_apply

    def build(self) -> QGroupBox:
        group_box = QGroupBox("Фильтрация")
        group_box.setStyleSheet(GroupBoxStyles.default())

        filter_layout = QHBoxLayout()
        self.search_input = self.create_search_input()
        self.search_button = self.create_search_button()
        self.stars_combo = self.create_stars_combo()
        self.sort_combo = self.create_sort_combo()
        self.sentiment_combo = self.create_sentiment_combo()

        search_block = QHBoxLayout()
        search_block.addWidget(self.search_input)
        search_block.addWidget(self.search_button)

        search_widget = QWidget()
        search_widget.setLayout(search_block)

        filter_layout.addWidget(search_widget)
        filter_layout.addStretch()
        filter_layout.addWidget(self.stars_combo)
        filter_layout.addWidget(self.sort_combo)
        filter_layout.addWidget(self.sentiment_combo)

        group_box.setLayout(filter_layout)
        return group_box

    def create_search_input(self) -> QLineEdit:
        search_input = QLineEdit()
        search_input.setPlaceholderText("Поиск по тексту...")
        search_input.setFixedWidth(250)
        search_input.setStyleSheet(LabelStyles.filter_text())
        search_input.textChanged.connect(self.on_filter_apply)
        return search_input

    def create_search_button(self) -> QPushButton:
        button = QPushButton("Найти")
        button.setFixedSize(80, 35)
        button.clicked.connect(self.on_filter_apply)
        button.setStyleSheet(ButtonStyles.default())
        return button

    def create_stars_combo(self) -> QComboBox:
        combo = QComboBox()
        combo.addItems(["Все оценки", "5 звезд", "4 звезды", "3 звезды", "2 звезды", "1 звезда"])
        combo.setFixedWidth(150)
        combo.setStyleSheet(LabelStyles.filter_text())
        combo.currentIndexChanged.connect(self.on_filter_apply)
        return combo

    def create_sort_combo(self) -> QComboBox:
        combo = QComboBox()
        combo.addItems(["По умолчанию", "Сначала лучшие", "Сначала худшие"])
        combo.setFixedWidth(200)
        combo.setStyleSheet(LabelStyles.filter_text())
        combo.currentIndexChanged.connect(self.on_filter_apply)
        return combo

    def create_sentiment_combo(self) -> QComboBox:
        combo = QComboBox()
        combo.addItems(["Все", "Позитивный", "Негативный"])
        combo.setFixedWidth(200)
        combo.setStyleSheet(LabelStyles.filter_text())
        combo.currentIndexChanged.connect(self.on_filter_apply)
        return combo
