import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from controllers.app_controller import AppController

def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Bahnschrift"))
    controller = AppController()
    controller.run()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
