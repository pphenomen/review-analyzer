from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QSizePolicy
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from views.helpers.drag_drop_frame import DragDropFrame
from views.helpers.styles import LabelStyles, DragDropStyles, ButtonStyles
import os

class StartPage(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        logo_desc_container = QWidget()
        logo_desc_layout = QVBoxLayout()
        logo_desc_layout.setAlignment(Qt.AlignCenter)
        logo_desc_layout.setSpacing(20)

        logo_desc_layout.addWidget(self.build_logo())
        logo_desc_layout.addWidget(self.build_description())

        logo_desc_container.setLayout(logo_desc_layout)

        main_layout.addWidget(logo_desc_container)
        main_layout.addWidget(self.build_drag_area())

        self.setLayout(main_layout)

    def build_logo(self):
        label = QLabel(self)
        pixmap = QPixmap("images/logo.png")
        label.setPixmap(pixmap.scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("margin-top: 125px;")
        return label

    def build_description(self):
        label = QLabel(
            "Приложение предназначено для анализа и визуализации отзывов товаров с маркетплейсов.\n"
            "Для начала работы загрузите файл с отзывами.\n"
        )
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)
        label.setFixedWidth(450)
        label.setStyleSheet(LabelStyles.description())
        return label

    def build_drag_area(self):
        self.drag_area = DragDropFrame(self)
        self.drag_area.setStyleSheet(DragDropStyles.drag_area())
        self.drag_area.setFixedSize(500, 200)
        self.drag_area.fileDropped.connect(self.process_file)

        drag_layout = QVBoxLayout(self.drag_area)
        drag_layout.setAlignment(Qt.AlignCenter)

        cloud_icon = QLabel(self)
        cloud_pixmap = QPixmap("images/move-file.png")
        cloud_icon.setPixmap(cloud_pixmap.scaled(48, 48, Qt.KeepAspectRatio))
        cloud_icon.setStyleSheet("border: none;")
        cloud_icon.setAlignment(Qt.AlignCenter)
        drag_layout.addWidget(cloud_icon)

        drag_text = QLabel("Переместите файл сюда или", self)
        drag_text.setStyleSheet(DragDropStyles.drag_text())
        drag_text.setAlignment(Qt.AlignCenter)
        drag_layout.addWidget(drag_text)

        self.load_file_button = QPushButton("Выберите файл", self)
        self.load_file_button.setStyleSheet(ButtonStyles.rounded())
        self.load_file_button.clicked.connect(self.load_file)
        drag_layout.addWidget(self.load_file_button, alignment=Qt.AlignCenter)

        return self.drag_area

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл Excel", "", "Excel Files (*.xlsx)")
        if file_path:
            self.process_file(file_path)

    def process_file(self, file_path):
        self.controller.load_reviews(file_path)