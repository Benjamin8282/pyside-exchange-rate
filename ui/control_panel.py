from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
)

class ControlPanelWidget(QWidget):
    visibility_changed = Signal(str, bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        # 통화 검색
        layout.addWidget(QLabel("통화 검색:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("예: USD, 유로")
        self.search_input.textChanged.connect(self._filter_currencies)
        layout.addWidget(self.search_input)

        # 표시할 통화 선택 리스트
        layout.addWidget(QLabel("표시할 통화:"))
        self.currency_list_widget = QListWidget()
        self.currency_list_widget.itemChanged.connect(self._on_item_changed)
        layout.addWidget(self.currency_list_widget)

        self.setMaximumWidth(250)

    def populate_currencies(self, currencies: list[tuple[str, str]], visible_currencies: dict):
        self.currency_list_widget.blockSignals(True)
        self.currency_list_widget.clear()
        for code, name in currencies:
            item = QListWidgetItem(f"{code} ({name})")
            item.setData(Qt.UserRole, code)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            # 설정에서 불러온 값 또는 기본값(True)으로 체크 상태 설정
            is_checked = visible_currencies.get(code, True)
            item.setCheckState(Qt.Checked if is_checked else Qt.Unchecked)
            self.currency_list_widget.addItem(item)
        self.currency_list_widget.blockSignals(False)

    def _on_item_changed(self, item: QListWidgetItem):
        currency_code = item.data(Qt.UserRole)
        is_checked = item.checkState() == Qt.Checked
        self.visibility_changed.emit(currency_code, is_checked)

    def _filter_currencies(self, text: str):
        for i in range(self.currency_list_widget.count()):
            item = self.currency_list_widget.item(i)
            item.setHidden(text.lower() not in item.text().lower())
