from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from resources.palette import THEMES, get_theme_name
from resources.theme_manager import theme_manager
from services.category_service import create_category, get_all_categories


class SettingsPage(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.title: QLabel = QLabel("Settings")

        self.separator: QWidget = QWidget()
        self.separator.setFixedHeight(2)
        self.separator.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.theme_label: QLabel = QLabel("Theme")

        self.theme_picker: QComboBox = QComboBox()
        self.theme_picker.addItems(list(THEMES.keys()))
        self.theme_picker.setCurrentText(get_theme_name())
        self.theme_picker.currentTextChanged.connect(theme_manager.set_theme)

        self.categories_label: QLabel = QLabel("Categories")

        self.categories_list: QListWidget = QListWidget()

        self.new_category_input: QLineEdit = QLineEdit()
        self.new_category_input.setPlaceholderText("New category name")

        self.add_category_button: QPushButton = QPushButton("Add")
        self.add_category_button.clicked.connect(self.on_add_category)

        add_category_row: QHBoxLayout = QHBoxLayout()
        add_category_row.addWidget(self.new_category_input)
        add_category_row.addWidget(self.add_category_button)

        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        layout.addWidget(self.title)
        layout.addWidget(self.separator)
        layout.addWidget(self.theme_label)
        layout.addWidget(self.theme_picker)
        layout.addWidget(self.categories_label)
        layout.addWidget(self.categories_list)
        layout.addLayout(add_category_row)
        layout.addStretch()

        theme_manager.theme_changed.connect(self.apply_theme)
        self.apply_theme(theme_manager.current_theme)

        self.refresh_categories()

    def refresh_categories(self) -> None:
        self.categories_list.clear()
        for category in get_all_categories():
            self.categories_list.addItem(category.name)

    def on_add_category(self) -> None:
        name = self.new_category_input.text().strip()
        if not name:
            return
        create_category(name)
        self.new_category_input.clear()
        self.refresh_categories()

    def apply_theme(self, theme: dict[str, str]) -> None:
        self.title.setStyleSheet(
            f"color: {theme['text']}; font-size: 24px; font-weight: bold;"
        )
        self.separator.setStyleSheet(f"background-color: {theme['border']};")
        self.theme_label.setStyleSheet(f"color: {theme['text']}; font-size: 16px;")
        self.theme_picker.setStyleSheet(
            f"""
            color: {theme["text"]};
            background-color: {theme["header_hover"]};
            border: 1px solid {theme["border"]};
            border-radius: 6px;
            padding: 6px;
            """
        )
        self.categories_label.setStyleSheet(f"color: {theme['text']}; font-size: 16px;")
        self.setStyleSheet("background-color: transparent;")
