from models.sentiment_predictor import SentimentPredictor
from utils.data_handler import DataHandler
from utils.plotter import Plotter
from views.main_window import MainWindow
from PyQt5.QtWidgets import QMessageBox

class AppController:
    def __init__(self):
        self.predictor = SentimentPredictor(
            model_path="models/sentiment_model.h5",
            tokenizer_path="models/tokenizer.json"
        )
        self.data_handler = DataHandler()
        self.plotter = Plotter()

        self.main_window = MainWindow(controller=self)

    def load_reviews(self, file_path):
        self.data_handler.load_data(file_path)
        self.data_handler.analyze_data(self.predictor)
        self.main_window.show_reviews(self.data_handler.get_reviews())

    def plot_reviews_chart(self):
        sentiment_counts = self.data_handler.get_sentiment_counts()
        self.plotter.plot_sentiment_distribution(
            sentiment_counts["positive"], 
            sentiment_counts["negative"]
        )

    def go_to_start_page(self):
        msg_box = QMessageBox(self.main_window)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Предупреждение")
        msg_box.setText("Вы уверены, что хотите вернуться? Все несохранённые данные будут потеряны.")
        msg_box.setIcon(QMessageBox.Warning)

        yes_button = msg_box.addButton("Да", QMessageBox.AcceptRole)
        no_button = msg_box.addButton("Нет", QMessageBox.RejectRole)

        msg_box.exec_()

        if msg_box.clickedButton() == yes_button:
            self.main_window.show_start_page()
    
    def run(self):
        self.main_window.show()
