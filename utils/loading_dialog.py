from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class LoadingDialog(QDialog):
    def __init__(self, message="Загрузка...", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Уведомление")
        self.setModal(True)
        self.setFixedSize(300, 100)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        if parent:
            self.setWindowIcon(parent.windowIcon())
            self.move(
                parent.frameGeometry().center() - self.rect().center()
            )

        layout = QVBoxLayout()
        self.label = QLabel(message)
        self.label.setAlignment(Qt.AlignCenter)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)

        layout.addWidget(self.label)
        layout.addWidget(self.progress)
        self.setLayout(layout)
