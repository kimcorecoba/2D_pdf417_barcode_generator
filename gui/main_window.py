from PySide6.QtCore import Qt
from core.default_header import default_header
from core.templates import driver_license_fields
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QFrame,
)
from gui.dashboard import Dashboard
from gui.field_editor import FieldEditor
from core.models import Field
from gui.toolbar import Toolbar
from core.parser import AAMVAParser
from core.validator import Validator
from core.barcode import BarcodeGenerator
from gui.barcode_preview import BarcodePreview
from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QFileDialog,
) 



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.header = default_header()
        self.barcode_generated = False

        self.setWindowTitle("PDF417 Studio")
        self.resize(1600, 900)

        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        
        # Toolbar
        self.toolbar = Toolbar()
        root.addWidget(self.toolbar)
        

        # Connect the Import button
        self.toolbar.new_clicked.connect(self.new_record)
        self.toolbar.sample_clicked.connect(self.fill_sample_data)
        self.toolbar.import_clicked.connect(self.import_aamva)
        self.toolbar.generate_clicked.connect(self.generate_barcode)
        self.toolbar.save_clicked.connect(self.save_as)
        

        # Dashboard
        self.dashboard = Dashboard()
        self.dashboard.setFixedHeight(130)

        self.dashboard.update_summary(
            health="100%",
            barcode_status="Ready",
            validation="No Issues",
            field_count=0,
        )

        root.addWidget(self.dashboard)

        # Main Area
        content = QHBoxLayout()

        # Field Editor
        self.editor = FieldEditor()
        
        self.editor.model.fieldEdited.connect(self.on_field_edited)

        
        # Barcode Preview
        self.preview = BarcodePreview()
        self.preview.setFixedWidth(420)

        content.addWidget(self.editor, 3)
        content.addWidget(self.preview, 1)
        root.addLayout(content)

        # Status Bar
        self.statusBar().showMessage("Ready")
    
    def new_record(self):
        self.header = default_header()
        self.dashboard.update_file_type("DL")

        fields = driver_license_fields()

        self.editor.load_fields(fields) 
       
     
    def fill_sample_data(self):
        
        
        sample_values = {
            "DAQ": "D12345678",
            "DCS": "DOE",
            "DAC": "JOHN",
            "DAD": "MICHAEL",
            "DCT": "JOHN MICHAEL",
            "DCU": "JR",
            "DBB": "01011990",
            "DBD": "01012025",
            "DBA": "01012033",
            "DBC": "1",
            "DAY": "BLU",
            "DAG": "123 MAIN STREET",
            "DAI": "ANYTOWN",
            "DAJ": "CA",
            "DAK": "90210",
            "DAU": "070 IN",
            "DAW": "180",
            "DAX": "180",
        }

        for field in self.editor.model.fields:
            if field.code in sample_values:
                field.value = sample_values[field.code]
        
        self.editor.model.refresh()
                   
    
    def import_aamva(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open AAMVA File",
            "",
            "Text Files (*.txt);;All Files (*)"
        )

        if not filename:
            return

        print(filename)    
        
        

        with open(filename, "r", encoding="utf-8") as file:
            raw = file.read()
            print("========== RAW FILE ==========")
            print(repr(raw))
            print("==============================")

        parser = AAMVAParser()
        validator = Validator()

        fields = parser.parse(raw)
        self.header = parser.header
        fields = validator.validate(fields)
        
        header = parser.header

        if header:
            from core.aamva_versions import AAMVA_STANDARDS

            self.dashboard.update_version(header.version)

            standard = AAMVA_STANDARDS.get(
                header.version,
                "Unknown"
            )

            self.dashboard.update_standard(standard)
            self.dashboard.update_iin(header.iin)
            self.dashboard.update_jurisdiction(
                header.jurisdiction_version
            
            )
            self.dashboard.update_file_type("DL")

        self.editor.load_fields(fields)

        valid_fields = sum(
            1 for field in fields
            if field.valid
        )

        health = round(
            (valid_fields / len(fields)) * 100
        )

        self.dashboard.update_summary(
            health=f"{health}%",
            barcode_status="Not Generated",
            validation="Imported",
            field_count=len(fields),
        )
        self.statusBar().showMessage(
            f"Imported {len(fields)} fields"
        )
    
    def generate_barcode(self):

        if not self.editor.model.fields:
            self.statusBar().showMessage("No data loaded.")
            return

        generator = BarcodeGenerator()

        print("\n===== FIELDS SENT TO ENCODER =====")

        for field in self.editor.model.fields:
            print(field.code, "=", repr(field.value))

        print("==================================\n")

        try:
            generator.generate(
                self.editor.model.fields,
                self.header,
            )
        except ValueError as error:
            QMessageBox.warning(
                self,
                "Invalid Data",
                str(error),
            )
            return

        self.preview.load_image("output/barcode.png")
        
        self.barcode_generated = True
        self.dashboard.update_summary(
            health=self.dashboard.health.text().replace("Record Health: ", ""),
            barcode_status="Up to Date",
            validation=self.dashboard.validation.text().replace("Validation: ", ""),
            field_count=len(self.editor.model.fields),
        )
        
        self.statusBar().showMessage("TEST MESSAGE", 10000)
        #self.statusBar().showMessage("Barcode generation started.")
        QMessageBox.information(
            self,
            "Generate",
            "Barcode generation started."
        )    
    def on_field_edited(self):

        fields = self.editor.model.fields

        valid_fields = sum(
            1 for field in fields
            if field.valid
        )

        health = round(
            (valid_fields / len(fields)) * 100
        ) if fields else 0

        validation = (
            "No Issues"
            if valid_fields == len(fields)
            else "Issues Found"
        )

        if self.barcode_generated:
            barcode_status = "Out of Date"
        else:
            barcode_status = "Ready"

        self.dashboard.update_summary(
            health=f"{health}%",
            barcode_status=barcode_status,
            validation=validation,
            field_count=len(fields),
        )
    
    def save_as(self):

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save AAMVA Record",
            "",
            "Text Files (*.txt);;All Files (*)"
        )

        if not filename:
            return

        encoder = BarcodeGenerator()

        try:
            
            data = encoder.generate(
                self.editor.model.fields,
                self.header,
            )
        except ValueError as error:
            QMessageBox.warning(
                self,
                "Save Failed",
                str(error),
            )
            return

        with open(filename, "w", encoding="utf-8") as file:
            file.write(data["payload"])

        QMessageBox.information(
            self,
            "Save",
            "Record saved successfully."
        )