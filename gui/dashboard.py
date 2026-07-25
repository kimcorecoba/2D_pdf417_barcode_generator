from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QGridLayout,
    QVBoxLayout,
)


class Dashboard(QFrame):
    def __init__(self):
        super().__init__()

        self.setFrameShape(QFrame.StyledPanel)

        title = QLabel("<h2>Dashboard</h2>")

        self.health = QLabel("Record Health: --")
        self.barcode = QLabel("Barcode Status: --")
        self.validation = QLabel("Validation: --")
        self.fields = QLabel("Fields: 0")
        self.version = QLabel("AAMVA Version: --")
        self.standard = QLabel("AAMVA Standard: --")
        self.iin = QLabel("Issuer (IIN): --")
        self.jurisdiction = QLabel("Jurisdiction Version: --")
        self.file_type = QLabel("File Type: --")

        grid = QGridLayout()
        grid.addWidget(self.health, 0, 0)
        grid.addWidget(self.barcode, 0, 1)
        grid.addWidget(self.validation, 1, 0)
        grid.addWidget(self.fields, 1, 1)
        grid.addWidget(self.version, 2, 0)
        grid.addWidget(self.standard, 2, 1)
        grid.addWidget(self.iin, 3, 0)
        grid.addWidget(self.jurisdiction, 3, 1)
        grid.addWidget(self.file_type, 4, 0)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addLayout(grid)

    def update_summary(
        self,
        health: str,
        barcode_status: str,
        validation: str,
        field_count: int,
    ):
    
        self.health.setText(f"Record Health: {health}")
        self.barcode.setText(f"Barcode Status: {barcode_status}")
        self.validation.setText(f"Validation: {validation}")
        self.fields.setText(f"Fields: {field_count}")
        
    def update_version(self, version: str):
        self.version.setText(f"AAMVA Version: {version}")
        
    def update_standard(self, standard: str):
        self.standard.setText(f"AAMVA Standard: {standard}")
        
    def update_iin(self, iin: str):
        self.iin.setText(f"Issuer (IIN): {iin}")
        
    def update_jurisdiction(self, version: str):
        self.jurisdiction.setText(
            f"Jurisdiction Version: {version}"
        )
    def update_file_type(self, file_type: str):
        self.file_type.setText(
            f"File Type: {file_type}"
        )