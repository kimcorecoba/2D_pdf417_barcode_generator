from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableView

from gui.field_model import FieldTableModel


class FieldEditor(QWidget):

    def __init__(self):
        super().__init__()

        self.model = FieldTableModel()

        self.table = QTableView()

        self.table.setModel(self.model)

        self.table.verticalHeader().setVisible(False)

        self.table.horizontalHeader().setStretchLastSection(True)

        layout = QVBoxLayout(self)

        layout.addWidget(self.table)

    def load_fields(self, fields):

        self.model.load_fields(fields)