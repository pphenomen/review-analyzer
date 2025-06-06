from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QComboBox, QPushButton, QGroupBox
from views.helpers.styles import ButtonStyles, LabelStyles, GroupBoxStyles
from views.helpers.buttons_factory import create_button, create_combo

class FiltersPanel(QWidget):
    def __init__(self, controller, on_filter_apply):
        super().__init__()
        self.controller = controller
        self.on_filter_apply = on_filter_apply

    def build(self) -> QGroupBox:
        group_box = QGroupBox("Фильтрация")
        group_box.setStyleSheet(GroupBoxStyles.default())

        filter_layout = QHBoxLayout()
        self.search_input = self.create_search_input()
        self.search_button = create_button("Найти", self.on_filter_apply)
        self.stars_combo = create_combo(
            ["Все оценки", "5 звезд", "4 звезды", "3 звезды", "2 звезды", "1 звезда"],
            self.on_filter_apply, width=150
        )
        self.sort_combo = create_combo(
            ["По умолчанию", "Сначала лучшие", "Сначала худшие"],
            self.on_filter_apply, width=200
        )
        sentiments = self.controller.get_available_sentiments()
        self.sentiment_combo = create_combo(
            ["Все"] + sentiments,
            self.on_filter_apply, width=200
        )

        self.reset_button = create_button("Сбросить фильтры", self.reset_filters)
        
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
        filter_layout.addWidget(self.reset_button)

        group_box.setLayout(filter_layout)
        return group_box

    def create_search_input(self) -> QLineEdit:
        search_input = QLineEdit()
        search_input.setPlaceholderText("Поиск по тексту...")
        search_input.setFixedWidth(250)
        search_input.setStyleSheet(LabelStyles.filter_text())
        search_input.textChanged.connect(self.on_filter_apply)
        return search_input
    
    def reset_filters(self):
        self.sentiment_combo.setCurrentIndex(0)
        self.search_input.clear()
        self.stars_combo.setCurrentIndex(0)
        self.sort_combo.setCurrentIndex(0)