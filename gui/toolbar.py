from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout


class Toolbar(QWidget):

    new_clicked = Signal()
    import_clicked = Signal()
    generate_clicked = Signal()
    save_clicked = Signal()
    sample_clicked = Signal()

   

    def __init__(self):
        super().__init__()
        
        
        self.new_button = QPushButton("New Record")
        self.import_button = QPushButton("Import AAMVA")
        self.sample_button = QPushButton("Fill Sample Data")
        self.generate_button = QPushButton("Generate Barcode")
        self.save_button = QPushButton("Save As...")
        
        layout = QHBoxLayout(self)
        layout.addWidget(self.new_button)
        layout.addWidget(self.sample_button)
        layout.addWidget(self.import_button)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.save_button)
        layout.addStretch()
        
        self.new_button.clicked.connect(self.new_clicked.emit)
        self.sample_button.clicked.connect(self.sample_clicked.emit)
        self.import_button.clicked.connect(self.import_clicked.emit)
        self.generate_button.clicked.connect(self.generate_clicked.emit)
        self.save_button.clicked.connect(self.save_clicked.emit)