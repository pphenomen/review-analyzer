from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from views.start_page import StartPage
from views.reviews_page import ReviewsPage

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Revizer")
        self.setGeometry(100, 100, 1024, 768)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.start_page = StartPage(controller)
        self.reviews_page = ReviewsPage(controller)

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