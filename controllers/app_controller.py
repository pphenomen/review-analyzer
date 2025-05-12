from models.lstm.lstm_predictor import LSTMPredictor
from models.transformer.transformer_predictor import TransformerPredictor
from models.strategies.lstm_strategy import LSTMStrategy
from models.strategies.transformer_strategy import TransformerStrategy
from utils.data_handler import DataHandler
from utils.plotter import Plotter
from utils.filters.base_filter import ReviewFilter
from utils.filters.sentiment_filter import SentimentFilter
from utils.filters.keyword_filter import KeywordFilter
from utils.filters.stars_filter import StarsFilter
from utils.filters.best_worst_filter import BestWorstFilter
from views.main_window import MainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMessageBox
from utils.loading_dialog import LoadingDialog
from utils.review_loader import ReviewLoaderWorker

class AppController:
    def __init__(self):
        self.lstm_predictor = LSTMPredictor(
            model_path="models/lstm/model/lstm_model.h5",
            tokenizer_path="models/lstm/model/tokenizer.json"
        )
        self.transformer_predictor = TransformerPredictor(
            model_path="models/transformer/model"
        )
        self.data_handler = DataHandler()
        self.plotter = Plotter()
        
        self.set_model_strategy("RuBERT")
        self.main_window = MainWindow(controller=self)
           
    def set_model_strategy(self, model_name: str):
        strategy_map = {
            "LSTM": lambda: self._init_strategy("LSTM"),
            "RuBERT": lambda: self._init_strategy("RuBERT")
        }
        strategy_map.get(model_name, lambda: None)()
    
    def _init_strategy(self, model_name: str):
        if model_name == "LSTM":
            self.model_strategy = LSTMStrategy(self.lstm_predictor)
        elif model_name == "RuBERT":
            self.model_strategy = TransformerStrategy(self.transformer_predictor)
        
        if self.data_handler.df is not None:
            reviews = self.data_handler.get_all_reviews()
            predicted = self.model_strategy.predict(reviews)
            self.main_window.reviews_page.display_reviews(predicted)
                
    def analyze(self, texts):
        return self.model_strategy.predict(texts)
    
    def load_reviews(self, file_path):
        self.loading_dialog = LoadingDialog("Загрузка отзывов...", parent=self.main_window)
        self.loading_dialog.show()

        self.thread = QThread()
        self.worker = ReviewLoaderWorker(file_path, self.data_handler, self.model_strategy)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_reviews_loaded)
        self.worker.error.connect(self.on_reviews_load_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def on_reviews_loaded(self, predicted_reviews):
        self.data_handler.set_predicted_reviews(predicted_reviews)
        self.main_window.show_reviews(predicted_reviews)
        self.loading_dialog.close()
    
    def on_reviews_load_error(self, error_msg):
        self.loading_dialog.close()
        error_box = QMessageBox(self.main_window)
        error_box.setWindowTitle("Ошибка")
        error_box.setText("Произошла ошибка при загрузке отзывов:\n\n" + error_msg)
        error_box.setIcon(QMessageBox.Critical)
        error_box.exec_()
    
    def plot_sentiment_pie_chart(self):
        sentiment_counts = self.data_handler.get_sentiment_counts()
        self.plotter.pie_sentiment_plot(sentiment_counts)

    def plot_rating_histogram_chart(self):
        reviews = self.data_handler.get_reviews()
        if not reviews:
            self.show_no_results_message()
            return
        self.plotter.histogram_rating_plot(reviews)

    def go_to_start_page(self):
        msg_box = QMessageBox(self.main_window)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Предупреждение")
        msg_box.setText("Вы уверены, что хотите вернуться? Все несохранённые данные будут потеряны.")

        yes_button = msg_box.addButton("Да", QMessageBox.AcceptRole)
        no_button = msg_box.addButton("Нет", QMessageBox.RejectRole)

        msg_box.exec_()

        if msg_box.clickedButton() == yes_button:
            self.main_window.show_start_page()
            
    def apply_filters(self, sentiment="Все", keyword="", stars=None, sort_order="Без сортировки", stars_filter="Все оценки"):
        base = ReviewFilter(self.data_handler.get_reviews())
        
        allowed = self.get_available_sentiments()
        if sentiment != "Все":
            base = SentimentFilter(base, sentiment, allowed)
        if keyword.strip():
            base = KeywordFilter(base, keyword)
        if stars_filter != "Все оценки":
            stars_number = int(stars_filter[0])
            base = StarsFilter(base, stars_number)
            
        filtered_reviews = base.filter()

        if not filtered_reviews or len(filtered_reviews) == 1 and filtered_reviews[0][0] == "Совпадений не найдено":
            self.show_no_results_message()
            return []
        
        if sort_order == "По умолчанию":
            return filtered_reviews
    
        best_worst_filter = BestWorstFilter(base, sort_order)
        sorted_reviews = best_worst_filter.filter()
        
        return sorted_reviews
    
    def get_available_sentiments(self):
        if not hasattr(self, 'model_strategy') or self.model_strategy is None:
            return []
    
        if isinstance(self.model_strategy, LSTMStrategy):
            return ["Позитивный", "Негативный"]
        elif isinstance(self.model_strategy, TransformerStrategy):
            return ["Позитивный", "Нейтральный", "Негативный"]
        return []
    
    def show_no_results_message(self):
        msg = QMessageBox(self.main_window)
        msg.setWindowTitle("Предупреждение")
        msg.setText("По вашему запросу совпадений не найдено.")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def run(self):
        self.main_window.show()
