from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor, QFont
from core.models import Field
from core.validator import Validator
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, Signal


class FieldTableModel(QAbstractTableModel):
    fieldEdited = Signal()

    HEADERS = ["Code", "Field", "Value", "Status"]

    def __init__(self):
        super().__init__()
        self.fields: list[Field] = []

    def load_fields(self, fields: list[Field]):
        self.beginResetModel()
        self.fields = fields
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return len(self.fields)

    def columnCount(self, parent=QModelIndex()):
        return 4

    def data(self, index, role):

        if not index.isValid():
            return None

        field = self.fields[index.row()]
        
        if role == Qt.FontRole:

            if index.column() == 2 and field.changed:
                font = QFont()
                font.setBold(True)
                return font
        
        if role == Qt.ForegroundRole:
            

            if field.name == "Unknown Field":
                return QColor("darkorange")

            if not field.valid:
                return QColor("red")
        if role == Qt.ToolTipRole:

            if index.column() == 3 and field.message:
                return field.message
                
        if role in (Qt.DisplayRole, Qt.EditRole):

            if index.column() == 0:
                return field.code

            if index.column() == 1:
                return field.name

            if index.column() == 2:
                return field.value

            if index.column() == 3:

                if field.valid:
                    if field.changed:
                        return "✓ ✎"
                    return "✓"

                if field.changed:
                    return "✗ ✎"

                return "✗"

        return None

    def headerData(self, section, orientation, role):

        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self.HEADERS[section]

        return None

    def flags(self, index):

        flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled

        if index.column() == 2:
            flags |= Qt.ItemIsEditable

        return flags

    def setData(self, index, value, role):

        if role != Qt.EditRole:
            return False

        field = self.fields[index.row()]

        if index.column() == 2:

            field.value = value

            field.changed = (
                field.value != field.original_value
            )

            validator = Validator()
            validator.validate(self.fields)

            top_left = self.index(0, 0)
            bottom_right = self.index(
                self.rowCount() - 1,
                self.columnCount() - 1
            )

            self.dataChanged.emit(top_left, bottom_right)
            self.fieldEdited.emit()

            return True

        return False