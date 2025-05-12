from PyQt5.QtCore import QObject, QThread, pyqtSignal
import traceback

class ReviewLoaderWorker(QObject):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, file_path, data_handler, model_strategy):
        super().__init__()
        self.file_path = file_path
        self.data_handler = data_handler
        self.model_strategy = model_strategy

    def run(self):
        try:
            self.data_handler.load_data(self.file_path)
            reviews = self.data_handler.get_all_reviews()
            predicted = self.model_strategy.predict(reviews)
            self.finished.emit(predicted)
        except Exception:
            self.error.emit(traceback.format_exc())
