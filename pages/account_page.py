from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from models.account import Account
from resources.theme_manager import theme_manager
from services.account_service import create_account, get_all_accounts
from ui.add_account_dialog import AddAccountDialog


class AccountPage(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.title: QLabel = QLabel("Accounts")

        self.add_account_button: QPushButton = QPushButton("Add account")
        self.add_account_button.setObjectName("add_account_button")
        self.add_account_button.clicked.connect(self.open_add_account_dialog)

        header_row: QHBoxLayout = QHBoxLayout()
        header_row.addWidget(self.title)
        header_row.addStretch()
        header_row.addWidget(self.add_account_button)

        self.separator: QWidget = QWidget()
        self.separator.setFixedHeight(2)
        self.separator.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.accounts_table: QTableWidget = QTableWidget()
        self.accounts_table.setColumnCount(4)
        self.accounts_table.setHorizontalHeaderLabels(
            ["Name", "Category", "Balance", ""]
        )
        self.accounts_table.horizontalHeader().setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self.accounts_table.verticalHeader().setStyleSheet(
            "QHeaderView::section { border none,}"
        )
        self.accounts_table.setFrameShape(QFrame.Shape.NoFrame)
        self.accounts_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.accounts_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.accounts_table.horizontalHeader().setSectionsClickable(False)
        self.accounts_table.verticalHeader().setVisible(False)
        self.accounts_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.accounts_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.accounts_table.setShowGrid(False)

        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        layout.addLayout(header_row)
        layout.addWidget(self.separator)
        layout.addWidget(self.accounts_table)

        theme_manager.theme_changed.connect(self.apply_theme)
        self.apply_theme(theme_manager.current_theme)

        self.refresh_accounts()

    def apply_theme(self, theme: dict[str, str]) -> None:
        self.title.setStyleSheet(
            f"color: {theme['text']}; font-size: 24px; font-weight: bold;"
        )
        self.separator.setStyleSheet(f"background-color: {theme['border']};")

        self.accounts_table.setStyleSheet(
            f"""
            QHeaderView::section {{
                background-color: transparent;
                color: {theme["text"]};
                font-size: 14px;
                font-weight: bold;
                border: none;
                padding: 4px;
            }}
            QTableWidget::item {{
                border-bottom: 1px solid {theme["border"]};
                padding: 6px 4px;
            }}
            """
        )

        self.setStyleSheet(f"""
    QWidget {{
        background-color: transparent;
    }}
    #add_account_button {{
        color: {theme["accent"]};
        background-color: {theme["header_hover"]};
        border: none;
        border-radius: 10px;
        text-align: left;
        padding: 8px 12px;
        font-size: 14px;
    }}
    #add_account_button:hover {{
        background-color: {theme["header_active"]};
    }}
    #add_account_button:pressed {{
        background-color: {theme["border_light"]};
    }}
""")

    def refresh_accounts(self) -> None:
        accounts: list[Account] = get_all_accounts()
        self.accounts_table.setRowCount(len(accounts))
        for row, account in enumerate(accounts):
            self.accounts_table.setItem(row, 0, QTableWidgetItem(account.name))
            self.accounts_table.setItem(row, 1, QTableWidgetItem(account.category.name))
            self.accounts_table.setItem(
                row, 2, QTableWidgetItem(f"{account.balance:.2f}")
            )
            self.accounts_table.setCellWidget(
                row, 3, self._build_actions_widget(account.id)
            )

    def _build_actions_widget(self, account_id: int) -> QWidget:
        theme = theme_manager.current_theme

        container = QWidget()
        container.setProperty("class", "action_cell")

        layout = QHBoxLayout(container)
        layout.setContentsMargins(4, 0, 4, 0)
        layout.setSpacing(6)

        edit_button = QPushButton("Edit")
        delete_button = QPushButton("Delete")

        for button in (edit_button, delete_button):
            button.setStyleSheet(
                f"""
                color: {theme["accent"]};
                background-color: transparent;
                border: none;
                padding: 4px 8px;
                """
            )

        edit_button.clicked.connect(lambda: self.on_edit_account(account_id))
        delete_button.clicked.connect(lambda: self.on_delete_account(account_id))

        layout.addStretch()
        layout.addWidget(edit_button)
        layout.addWidget(delete_button)

        return container

    def on_edit_account(self, account_id: int) -> None:
        pass

    def on_delete_account(self, account_id: int) -> None:
        pass

    def open_add_account_dialog(self) -> None:
        dialog: AddAccountDialog = AddAccountDialog(parent=self)
        if dialog.exec() == AddAccountDialog.DialogCode.Accepted:
            create_account(
                name=dialog.name_input.text(),
                category_id=dialog.category_input.currentData(),
                balance=float(dialog.balance_input.text() or 0),
            )
            self.refresh_accounts()
