from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtGui import QIcon
from views.start_page import StartPage
from views.reviews_page.reviews_page import ReviewsPage

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("REVIZER")
        self.setGeometry(100, 100, 1024, 768)
        self.setWindowIcon(QIcon("images/icon.png"))

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.start_page = StartPage(controller)
        self.reviews_page = ReviewsPage(controller, self.on_model_changed)

        self.stacked_widget.addWidget(self.start_page)
        self.stacked_widget.addWidget(self.reviews_page)

        self.show_start_page()

    def show_start_page(self):
        self.stacked_widget.setCurrentWidget(self.start_page)

    def show_reviews_page(self):
        self.stacked_widget.setCurrentWidget(self.reviews_page)

    def show_reviews(self, reviews):
        self.reviews_page.display_reviews(reviews)
        self.show_reviews_page()
        
    def on_model_changed(self, model_name):
        self.controller.set_model_strategy(model_name)
        self.reviews_page.update_model_description(model_name)