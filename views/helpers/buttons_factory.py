from PyQt5.QtWidgets import QPushButton, QComboBox
from views.helpers.styles import ButtonStyles, LabelStyles

def create_button(text: str, callback) -> QPushButton:
    button = QPushButton(text)
    button.setFixedHeight(35)
    button.adjustSize()
    button.setStyleSheet(ButtonStyles.default())
    button.clicked.connect(callback)
    return button

def create_combo(items: list, callback, width=200) -> QComboBox:
    combo = QComboBox()
    combo.addItems(items)
    combo.setFixedWidth(width)
    combo.setStyleSheet(LabelStyles.filter_text())
    combo.currentIndexChanged.connect(callback)
    return combo