from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from core.file_compare import FileComparisonResult


class CompareDialog(QDialog):

    def __init__(self, result: FileComparisonResult, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Compare Files")
        self.resize(980, 640)

        root = QVBoxLayout(self)

        title = QLabel(
            "<h2>Match</h2>"
            if result.byte_identical
            else "<h2>Differences Found</h2>"
        )
        root.addWidget(title)

        summary = QLabel(result.summary)
        summary.setWordWrap(True)
        root.addWidget(summary)

        details = QLabel(self._build_details(result))
        details.setWordWrap(True)
        root.addWidget(details)

        root.addWidget(QLabel("<b>Field Comparison</b>"))

        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(
            ["Subfile", "Code", "Left Value", "Right Value", "Status"]
        )
        table.setRowCount(len(result.field_comparisons))
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectRows)

        for row, comparison in enumerate(result.field_comparisons):
            values = [
                comparison.subfile,
                comparison.code,
                self._format_value(comparison.left_value),
                self._format_value(comparison.right_value),
                comparison.status.replace("_", " ").title(),
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                if comparison.status != "same":
                    item.setForeground(QColor("red"))
                table.setItem(row, column, item)

        table.resizeColumnsToContents()
        table.horizontalHeader().setStretchLastSection(True)
        root.addWidget(table)

        buttons = QHBoxLayout()
        buttons.addStretch()

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        buttons.addWidget(close_button)
        root.addLayout(buttons)

    def _build_details(self, result: FileComparisonResult) -> str:
        left_name = Path(result.left_path).name
        right_name = Path(result.right_path).name

        lines = [
            f"<b>Left:</b> {left_name} ({result.left_size} bytes)",
            f"<b>Right:</b> {right_name} ({result.right_size} bytes)",
            f"<b>Subfile headers:</b> "
            f"{'Match' if result.subfiles_match else 'Differ'}",
            f"<b>Field order:</b> "
            f"{'Match' if result.field_order_match else 'Differ'}",
            f"<b>Matching fields:</b> "
            f"{result.matching_field_count}/{result.total_field_count}",
        ]

        if result.left_subfiles:
            lines.append(
                "<b>Left subfiles:</b> "
                + ", ".join(
                    f"{subfile.file_type}@{subfile.offset:04d}/{subfile.length:04d}"
                    for subfile in result.left_subfiles
                )
            )

        if result.right_subfiles:
            lines.append(
                "<b>Right subfiles:</b> "
                + ", ".join(
                    f"{subfile.file_type}@{subfile.offset:04d}/{subfile.length:04d}"
                    for subfile in result.right_subfiles
                )
            )

        return "<br>".join(lines)

    def _format_value(self, value: str | None) -> str:
        if value is None:
            return "<missing>"

        if value == "":
            return '""'

        return value
