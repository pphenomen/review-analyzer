from PyQt5.QtWidgets import QPushButton, QComboBox
from helpers.styles import button_style

def create_button(text: str, callback) -> QPushButton:
    button = QPushButton(text)
    button.setFixedSize(80, 35)
    button.setStyleSheet(button_style())
    button.clicked.connect(callback)
    return button

def create_combo(items: list, callback, width=200) -> QComboBox:
    combo = QComboBox()
    combo.addItems(items)
    combo.setFixedWidth(width)
    combo.setStyleSheet("font-size: 14px; padding: 5px;")
    combo.currentIndexChanged.connect(callback)
    return combo
