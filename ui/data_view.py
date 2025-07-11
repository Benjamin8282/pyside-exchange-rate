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
    QSizePolicy,
)
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, Signal
from PySide6.QtGui import QFont, QMouseEvent

from core.exchange_rate_model import ExchangeRate


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

        # 테이블 헤더 크기 조정
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        layout.addWidget(self.table_view)

        close_button = QPushButton("닫기")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)


class CurrencyRateWidget(QWidget):
    clicked = Signal(str) # 통화 코드를 전달하는 시그널

    def __init__(self, currency_code: str, currency_name: str, deal_bas_r: str, parent=None):
        super().__init__(parent)
        self.currency_code = currency_code
        self.currency_name = currency_name
        self.deal_bas_r = deal_bas_r

        self.setFixedSize(180, 120) # 고정 크기
        self.setStyleSheet("background-color: white; border: 1px solid #ccc; border-radius: 5px;")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0) # 마진 제거
        layout.setSpacing(0) # 위젯 간 간격 제거

        # 모든 정보를 담을 단일 라벨
        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setWordWrap(False) # 자동 줄바꿈 비활성화
        self.info_label.setFixedSize(178, 118) # QLabel의 크기를 위젯 내부 공간에 맞춰 고정 (테두리 1px 고려)

        # 폰트 설정
        font_code = QFont()
        font_code.setPointSize(12)
        font_code.setBold(True)

        font_rate = QFont()
        font_rate.setPointSize(28)
        font_rate.setBold(True)

        font_name = QFont()
        font_name.setPointSize(10)

        # HTML을 사용하여 폰트 크기 및 색상 적용
        # 매매 기준율은 큰 글씨, 통화 코드는 작게, 통화명은 더 작게
        html_text = f"""
        <div style="text-align:center;">
            <div style="font-size:{font_code.pointSize()}pt; font-weight:bold;">{self.currency_code}</div>
            <div style="font-size:{font_rate.pointSize()}pt; font-weight:bold;">{self.deal_bas_r}</div>
            <div style="font-size:{font_name.pointSize()}pt;">{self.currency_name}</div>
        </div>
        """

        # QLabel에 HTML 렌더링 설정 및 적용
        self.info_label.setTextFormat(Qt.RichText)  # HTML 렌더링 모드로 설정
        self.info_label.setText(html_text)  # HTML 내용 적용

        layout.addWidget(self.info_label)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.currency_code)
        super().mousePressEvent(event)


class DataViewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.exchange_rates: list[ExchangeRate] = []

        main_layout = QVBoxLayout(self)

        # 환율 정보 표시 그리드 레이아웃
        self.rates_grid_layout = QGridLayout()
        self.rates_grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft) # 상단 왼쪽 정렬
        main_layout.addLayout(self.rates_grid_layout)

        main_layout.addStretch() # 그리드 위젯들이 상단에 모이도록

        # 하단 상태 및 새로고침 영역
        bottom_layout = QHBoxLayout()
        self.status_label = QLabel("준비")
        self.refresh_button = QPushButton("새로고침")
        bottom_layout.addWidget(self.status_label)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.refresh_button)
        main_layout.addLayout(bottom_layout)

    def update_exchange_rates(self, rates: list[ExchangeRate]):
        self.exchange_rates = rates

        # 기존 위젯들 제거
        for i in reversed(range(self.rates_grid_layout.count())):
            widget_to_remove = self.rates_grid_layout.itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.setParent(None)
                widget_to_remove.deleteLater()

        if rates:
            row = 0
            col = 0
            for rate in rates:
                # result가 1인 경우에만 표시
                if rate.result == 1:
                    currency_widget = CurrencyRateWidget(
                        currency_code=rate.cur_unit,
                        currency_name=rate.cur_nm,
                        deal_bas_r=rate.deal_bas_r
                    )
                    currency_widget.clicked.connect(self._show_detail_dialog_for_currency)
                    self.rates_grid_layout.addWidget(currency_widget, row, col)
                    col += 1
                    if col >= 4: # 한 줄에 4개씩 표시
                        col = 0
                        row += 1
            self.status_label.setText(f"총 {len([r for r in rates if r.result == 1])}개 환율 정보 로드 완료")
        else:
            self.status_label.setText("환율 정보를 가져오지 못했습니다.")

    def _show_detail_dialog_for_currency(self, currency_code: str):
        # 클릭된 통화의 세부 정보만 보여주도록 수정
        selected_rate = next((r for r in self.exchange_rates if r.cur_unit == currency_code), None)
        if selected_rate:
            dialog = ExchangeRateDetailDialog([selected_rate], self) # 단일 통화 정보만 전달
            dialog.exec()
        else:
            self.status_label.setText(f"{currency_code} 환율 정보를 찾을 수 없습니다.")
