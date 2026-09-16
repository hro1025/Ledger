from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from resources.theme_manager import theme_manager
from services.category_service import get_all_categories


class AddAccountDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setFixedSize(300, 400)
        self.setObjectName("AddAccountDialog")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.label: QLabel = QLabel("Enter account information")

        self.name_input: QLineEdit = QLineEdit()
        self.name_input.setPlaceholderText("Name")

        self.category_input: QComboBox = QComboBox()
        for category in get_all_categories():
            self.category_input.addItem(category.name, category.id)
        self.category_input.setCurrentIndex(-1)
        self.category_input.setPlaceholderText("Select a category")

        self.balance_input: QLineEdit = QLineEdit()
        self.balance_input.setPlaceholderText("0.00")
        self.balance_input.setValidator(QDoubleValidator())

        fields_column: QVBoxLayout = QVBoxLayout()
        fields_column.setSpacing(10)
        fields_column.addWidget(self.label)
        fields_column.addWidget(self.name_input)
        fields_column.addWidget(self.category_input)
        fields_column.addWidget(self.balance_input)

        self.import_button: QPushButton = QPushButton("Import")

        self.add_button: QPushButton = QPushButton("Add")
        self.add_button.clicked.connect(self.accept)

        button_row: QHBoxLayout = QHBoxLayout()
        button_row.addWidget(self.import_button)
        button_row.addStretch()
        button_row.addWidget(self.add_button)

        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addLayout(fields_column)
        layout.addStretch()
        layout.addLayout(button_row)

        theme_manager.theme_changed.connect(self.apply_theme)
        self.apply_theme(theme_manager.current_theme)

    def apply_theme(self, theme: dict[str, str]) -> None:
        self.label.setStyleSheet(f"color: {theme['text']}; font-size: 16px;")

        for input_field in (self.name_input, self.category_input, self.balance_input):
            input_field.setStyleSheet(
                f"""
                color: {theme["text"]};
                border: 1px solid {theme["border"]};
                border-radius: 6px;
                padding: 6px;
                """
            )

        for button in (self.import_button, self.add_button):
            button.setStyleSheet(
                f"""
                color: {theme["accent"]};
                background-color: {theme["header_hover"]};
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
                """
            )

        self.setStyleSheet(f"""
            #AddAccountDialog {{
                background-color: {theme["header"]};
                border: 2px solid {theme["border"]};
            }}
        """)
