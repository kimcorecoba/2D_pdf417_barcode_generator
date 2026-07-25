from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class BarcodePreview(QWidget):

    def __init__(self):
        super().__init__()

        self.label = QLabel("No barcode generated")
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

    def load_image(self, filename):

        pixmap = QPixmap(filename)

        if pixmap.isNull():
            self.label.setText("Unable to load barcode.")
            return

        self.label.setPixmap(
            pixmap.scaled(
                350,
                500,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
        )