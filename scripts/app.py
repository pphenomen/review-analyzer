import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QFrame, QMessageBox, QScrollArea, QStackedWidget, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

from sentiment_predictor import SentimentPredictor
from data_handler import DataHandler
from plotter import Plotter
from widgets import DragDropFrame

class SentimentAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_handler = DataHandler()

        try:
            self.predictor = SentimentPredictor(
                model_path="../model/sentiment_model.h5",
                tokenizer_path="../model/tokenizer.json"
            )
        except ValueError as e:
            QMessageBox.critical(self, "Ошибка", str(e))
            sys.exit(1)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Revizer")
        self.setGeometry(100, 100, 1024, 768)
        self.setWindowIcon(QIcon("../images/icon.png"))
        self.setFixedSize(self.size())

        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self.start_page = self.create_start_page()
        self.reviews_page = self.create_reviews_page()

        self.stacked_widget.addWidget(self.start_page)
        self.stacked_widget.addWidget(self.reviews_page)

        self.stacked_widget.setCurrentWidget(self.start_page)

    def create_start_page(self):
        page = QWidget()

        logo_label = QLabel(self)
        logo_pixmap = QPixmap("../images/logo.png")
        logo_label.setPixmap(logo_pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)) 
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("margin-top: 150px;")
        
        description_label = QLabel(self)
        description_label.setText("Добро пожаловать в REVIZER!\n"
                          "Приложение предназначено для анализа и визуализации отзывов товаров с Wildberries.\n"
                          "Загружайте отзывы, определяйте их тональность и создавайте наглядные диаграммы со статистикой!\n")
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #505050; text-align: center; margin-bottom: 100px;")
        description_label.setWordWrap(True)
        description_label.setFixedWidth(450)

        self.load_file_button = QPushButton("Выберите файл", self)
        self.load_file_button.setStyleSheet("""
            font-size: 18px;
            padding: 15px;
            background: qlineargradient(
                spread: pad,
                x1: 0, y1: 0, x2: 1, y2: 1,
                stop: 0 #1c1c1c,
                stop: 1 #3c3c3c
            );
            color: #ffffff;
            border: none;
            border-radius: 8px;
        """)
        self.load_file_button.setFixedSize(250, 50)
        self.load_file_button.clicked.connect(self.load_file)

        self.drag_area = DragDropFrame(self)
        self.drag_area.setStyleSheet("""
            border: 2.5px dashed #333333;
            border-radius: 10px;
            background-color: #C0C0C0;
        """)
        self.drag_area.setFixedSize(600, 200)
        self.drag_area.fileDropped.connect(self.process_file)
        drag_area_layout = QVBoxLayout(self.drag_area)

        cloud_icon = QLabel(self)
        cloud_pixmap = QPixmap("../images/move-file.png")
        cloud_icon.setStyleSheet("border: none;")
        cloud_icon.setPixmap(cloud_pixmap.scaled(50, 50, Qt.KeepAspectRatio))
        cloud_icon.setAlignment(Qt.AlignCenter)
        drag_area_layout.addWidget(cloud_icon)

        drag_text = QLabel("Переместите файл сюда или", self)
        drag_text.setStyleSheet("font-size: 14px; font-weight: bold; color: #4A4A4A; border: none;")
        drag_text.setAlignment(Qt.AlignCenter)
        drag_area_layout.addWidget(drag_text)
        drag_area_layout.addWidget(self.load_file_button, alignment=Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(logo_label, alignment=Qt.AlignCenter)
        layout.addWidget(description_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.drag_area, alignment=Qt.AlignCenter)

        page.setLayout(layout)
        return page

    def create_reviews_page(self):
        page = QWidget()

        title_label = QLabel("Список отзывов", self)
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #2F2F2F;")
        title_label.setAlignment(Qt.AlignCenter)

        self.chart_button = QPushButton("Построить диаграмму", self)
        self.chart_button.setStyleSheet("""
            font-size: 16px; padding: 10px;
            background: qlineargradient(
                spread: pad,
                x1: 0, y1: 0, x2: 1, y2: 1,
                stop: 0 #1c1c1c,
                stop: 1 #3c3c3c
            );
            color: #ffffff;
            border: none; border-radius: 5px;
        """)
        self.chart_button.clicked.connect(self.plot_chart)

        back_button = QPushButton("Назад", self)
        back_button.setStyleSheet("""
            font-size: 16px; padding: 10px; 
            background: qlineargradient(
                spread: pad,
                x1: 0, y1: 0, x2: 1, y2: 1,
                stop: 0 #1c1c1c,
                stop: 1 #3c3c3c
            );
            color: #ffffff;
            border: none;
            border-radius: 5px;
        """)
        back_button.clicked.connect(self.go_to_start_page)

        self.review_count_label = QLabel(self)
        self.review_count_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #E0E0E0;")
        self.review_count_label.setAlignment(Qt.AlignLeft)

        footer_layout = QHBoxLayout()
        footer_layout.addWidget(self.review_count_label, alignment=Qt.AlignLeft)
        footer_layout.addStretch()
        footer_layout.addWidget(self.chart_button, alignment=Qt.AlignRight)
        footer_layout.addWidget(back_button, alignment=Qt.AlignRight)

        self.review_display = QWidget(self)
        self.review_display.setStyleSheet("font-size: 14px; color: #555; padding: 10px;")
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.review_display)
        self.scroll_area.setWidgetResizable(True)

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(self.scroll_area)
        layout.addLayout(footer_layout)

        page.setLayout(layout)
        return page

    def go_to_start_page(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Предупреждение")
        msg_box.setText("Вы уверены, что хотите вернуться? Все несохранённые данные будут потеряны.")
        msg_box.setIcon(QMessageBox.Warning)

        yes_button = msg_box.addButton("Да", QMessageBox.AcceptRole)
        no_button = msg_box.addButton("Нет", QMessageBox.RejectRole)

        msg_box.exec_()

        if msg_box.clickedButton() == yes_button:
            self.stacked_widget.setCurrentWidget(self.start_page)

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл Excel", "", "Excel Files (*.xlsx)")
        if file_path:
            self.process_file(file_path)

    def process_file(self, file_path):
        try:
            self.data_handler.load_data(file_path)
            self.data_handler.analyze_data(self.predictor)
            self.show_reviews()
            self.stacked_widget.setCurrentWidget(self.reviews_page)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при обработке файла: {e}")

    def show_reviews(self):
        reviews = self.data_handler.get_reviews()
        sentiment_counts = self.data_handler.get_sentiment_counts()

        layout = QVBoxLayout()
        for review, sentiment, stars in reviews:
            review_frame = QFrame(self)
            review_frame.setStyleSheet("""
                background-color: #ffffff;
                border-radius: 10px;
                margin-bottom: 15px;
                padding: 20px;
                border: 1px solid #E0E0E0;
            """)
            review_layout = QVBoxLayout()

            review_text = QLabel(f"<b>Отзыв:</b> {review}")
            review_text.setWordWrap(True)
            sentiment_label = QLabel(f"Тональность: {sentiment}")
            stars_label = QLabel("⭐" * stars)
            stars_label.setStyleSheet("font-size: 18px; color: #FFD700;")

            review_layout.addWidget(review_text)
            review_layout.addWidget(stars_label)
            review_layout.addWidget(sentiment_label)
            review_frame.setLayout(review_layout)
            layout.addWidget(review_frame)

        self.review_display.setLayout(layout)
        self.review_count_label.setText(f"Количество отзывов: {len(reviews)}")

    def plot_chart(self):
        sentiment_counts = self.data_handler.get_sentiment_counts()
        positive_reviews = sentiment_counts["positive"]
        negative_reviews = sentiment_counts["negative"]

        try:
            Plotter.plot_sentiment_distribution(positive_reviews, negative_reviews)
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = SentimentAnalyzerApp()
    main_window.show()
    sys.exit(app.exec_())
