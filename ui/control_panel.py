from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QComboBox,
    QLineEdit,
)


class ControlPanelWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        # 기준 통화 선택
        layout.addWidget(QLabel("기준 통화:"))
        self.base_currency_combo = QComboBox()
        layout.addWidget(self.base_currency_combo)

        # 통화 검색
        layout.addWidget(QLabel("통화 검색:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("예: USD, 유로")
        layout.addWidget(self.search_input)

        # 표시할 통화 선택 리스트
        layout.addWidget(QLabel("표시할 통화:"))
        self.currency_list_widget = QListWidget()
        self.currency_list_widget.setSelectionMode(QListWidget.MultiSelection)
        layout.addWidget(self.currency_list_widget)

        self.setMaximumWidth(250)

        # 임시 데이터 추가
        self._add_temp_data()

    def _add_temp_data(self):
        self.base_currency_combo.addItems(["KRW", "USD", "EUR", "JPY"])

        currencies = ["USD (미국 달러)", "EUR (유로)", "JPY (일본 옌)", "CNY (중국 위안)", "GBP (영국 파운드)"]
        for currency in currencies:
            item = QListWidgetItem(currency)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.currency_list_widget.addItem(item)
