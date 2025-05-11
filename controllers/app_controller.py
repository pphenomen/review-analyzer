from models.lstm.lstm_predictor import LSTMPredictor
from models.transformer.transformer_predictor import TransformerPredictor
from utils.data_handler import DataHandler
from utils.plotter import Plotter
from utils.filters.base_filter import ReviewFilter
from utils.filters.sentiment_filter import SentimentFilter
from utils.filters.keyword_filter import KeywordFilter
from utils.filters.stars_filter import StarsFilter
from views.main_window import MainWindow
from PyQt5.QtWidgets import QMessageBox

class AppController:
    def __init__(self):
        self.lstm_predictor = LSTMPredictor(
            model_path="models/lstm/model/lstm_model.h5",
            tokenizer_path="models/lstm/model/tokenizer.json"
        )
        self.transformer_predictor = TransformerPredictor(
            model_path="models/transformer/model"
        )
        self.set_model_strategy("LSTM")
        self.data_handler = DataHandler()
        self.plotter = Plotter()

        self.main_window = MainWindow(controller=self)
        self.set_model_strategy("RuBERT")
    
    def set_model_strategy(self, model_name: str):
        strategy_map = {
            "LSTM": lambda: self._init_strategy("LSTM"),
            "RuBERT": lambda: self._init_strategy("RuBERT")
        }
        strategy_map.get(model_name, lambda: None)()    
    
    def _init_strategy(self, model_name: str):
        if model_name == "LSTM":
            from models.strategies.lstm_strategy import LSTMStrategy
            self.model_strategy = LSTMStrategy(self.lstm_predictor)
        elif model_name == "RuBERT":
            from models.strategies.transformer_strategy import TransformerStrategy
            self.model_strategy = TransformerStrategy(self.transformer_predictor)

            if hasattr(self.data_handler, "df"):
                reviews = self.data_handler.get_all_reviews()
                predicted = self.model_strategy.predict(reviews)
                self.main_window.reviews_page.display_reviews(predicted)

    def analyze(self, texts):
        return self.model_strategy.predict(texts)
    
    def load_reviews(self, file_path):
        self.data_handler.load_data(file_path)
        self.data_handler.analyze_data(self.model_strategy)
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

        yes_button = msg_box.addButton("Да", QMessageBox.AcceptRole)
        no_button = msg_box.addButton("Нет", QMessageBox.RejectRole)

        msg_box.exec_()

        if msg_box.clickedButton() == yes_button:
            self.main_window.show_start_page()
            
    def apply_filters(self, sentiment="Все", keyword="", stars=None, sort_order="Без сортировки", stars_filter="Все оценки"):
        base = ReviewFilter(self.data_handler.get_reviews())

        if sentiment != "Все":
            base = SentimentFilter(base, sentiment)
        if keyword.strip():
            base = KeywordFilter(base, keyword)
        if stars_filter != "Все оценки":
            stars_number = int(stars_filter[0])
            base = StarsFilter(base, stars_number)
            
        filtered_reviews = base.filter()

        if not filtered_reviews or len(filtered_reviews) == 1 and filtered_reviews[0][0] == "Совпадений не найдено":
            self.show_no_results_message()
            return []
        
        if sort_order == "Сначала лучшие":
            filtered_reviews = sorted(filtered_reviews, key=lambda x: x[2], reverse=True)
        elif sort_order == "Сначала худшие":
            filtered_reviews = sorted(filtered_reviews, key=lambda x: x[2])
        
        return filtered_reviews 
    
    def show_no_results_message(self):
        msg = QMessageBox(self.main_window)
        msg.setWindowTitle("Предупреждение")
        msg.setText("По вашему запросу совпадений не найдено.")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def run(self):
        self.main_window.show()
