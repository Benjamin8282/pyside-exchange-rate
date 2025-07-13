from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableView,
    QPushButton,
    QLabel,
    QDialog,
    QHeaderView,
    QGridLayout,
)
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, Signal
from PySide6.QtGui import QFont, QMouseEvent

from model.exchange_rate_model import ExchangeRate
from viewmodel.exchange_rate_viewmodel import ExchangeRateViewModel


class ExchangeRateTableModel(QAbstractTableModel):
    def __init__(self, data: list[ExchangeRate]):
        super().__init__()
        self._data = data
        self._headers = [
            "통화코드", "통화명", "전신환(송금) 받으실 때", "전신환(송금) 보내실 때",
            "매매 기준율", "장부가격", "년환가료율", "10일환가료율",
            "서울외국환중개장부가격", "서울외국환중개매매기준율"
        ]

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._data)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            rate = self._data[index.row()]
            column = index.column()
            if column == 0: return rate.cur_unit
            if column == 1: return rate.cur_nm
            if column == 2: return rate.ttb
            if column == 3: return rate.tts
            if column == 4: return rate.deal_bas_r
            if column == 5: return rate.bkpr
            if column == 6: return rate.yy_efee_r
            if column == 7: return rate.ten_dd_efee_r
            if column == 8: return rate.kftc_bkpr
            if column == 9: return rate.kftc_deal_bas_r
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        return None


class ExchangeRateDetailDialog(QDialog):
    def __init__(self, exchange_rates: list[ExchangeRate], parent=None):
        super().__init__(parent)
        self.setWindowTitle("환율 정보")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout(self)

        self.table_view = QTableView()
        self.table_model = ExchangeRateTableModel(exchange_rates)
        self.table_view.setModel(self.table_model)

        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        layout.addWidget(self.table_view)

        close_button = QPushButton("닫기")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)


class CurrencyRateWidget(QWidget):
    clicked = Signal(str)

    def __init__(self, currency_code: str, currency_name: str, deal_bas_r: str, parent=None):
        super().__init__(parent)
        self.currency_code = currency_code
        self.currency_name = currency_name
        self.deal_bas_r = deal_bas_r

        self.setFixedSize(180, 120)
        self.setStyleSheet("background-color: white; border: 1px solid #ccc; border-radius: 5px;")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setWordWrap(False)
        self.info_label.setFixedSize(178, 118)

        font_code = QFont()
        font_code.setPointSize(12)
        font_code.setBold(True)

        font_rate = QFont()
        font_rate.setPointSize(28)
        font_rate.setBold(True)

        font_name = QFont()
        font_name.setPointSize(10)

        html_text = f"""
        <div style="text-align:center;">
            <div style="font-size:{font_code.pointSize()}pt; font-weight:bold;">{self.currency_code}</div>
            <div style="font-size:{font_rate.pointSize()}pt; font-weight:bold;">{self.deal_bas_r}</div>
            <div style="font-size:{font_name.pointSize()}pt;">{self.currency_name}</div>
        </div>
        """

        self.info_label.setTextFormat(Qt.RichText)
        self.info_label.setText(html_text)

        layout.addWidget(self.info_label)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.currency_code)
        super().mousePressEvent(event)


class DataViewWidget(QWidget):
    def __init__(self, viewmodel: ExchangeRateViewModel, parent=None):
        super().__init__(parent)
        self.viewmodel = viewmodel

        main_layout = QVBoxLayout(self)

        self.rates_grid_layout = QGridLayout()
        self.rates_grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        main_layout.addLayout(self.rates_grid_layout)

        main_layout.addStretch()

        bottom_layout = QHBoxLayout()
        self.status_label = QLabel("준비")
        self.refresh_button = QPushButton("새로고침")
        bottom_layout.addWidget(self.status_label)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.refresh_button)

        main_layout.addLayout(bottom_layout)

        # ViewModel과 연결
        self.viewmodel.exchange_rates_changed.connect(self.update_exchange_rates)
        self.viewmodel.status_changed.connect(self.status_label.setText)
        self.refresh_button.clicked.connect(self.viewmodel.fetch_exchange_rates)

    def update_exchange_rates(self, rates: list[ExchangeRate]):
        for i in reversed(range(self.rates_grid_layout.count())):
            widget_to_remove = self.rates_grid_layout.itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.setParent(None)
                widget_to_remove.deleteLater()

        if rates:
            row, col = 0, 0
            for rate in rates:
                if rate.result == 1:
                    currency_widget = CurrencyRateWidget(
                        currency_code=rate.cur_unit,
                        currency_name=rate.cur_nm,
                        deal_bas_r=rate.deal_bas_r
                    )
                    currency_widget.clicked.connect(self._show_detail_dialog_for_currency)
                    self.rates_grid_layout.addWidget(currency_widget, row, col)
                    col += 1
                    if col >= 4:
                        col = 0
                        row += 1

    def _show_detail_dialog_for_currency(self, currency_code: str):
        selected_rate = next((r for r in self.viewmodel.exchange_rates if r.cur_unit == currency_code), None)
        if selected_rate:
            dialog = ExchangeRateDetailDialog([selected_rate], self)
            dialog.exec()
        else:
            self.status_label.setText(f"{currency_code} 환율 정보를 찾을 수 없습니다.")
