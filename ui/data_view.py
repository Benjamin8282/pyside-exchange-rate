# -*- coding: utf-8 -*-

# 필요한 모듈들을 임포트합니다.
from PySide6.QtWidgets import (
    QWidget,         # 기본 위젯 클래스
    QVBoxLayout,     # 수직 레이아웃
    QHBoxLayout,     # 수평 레이아웃
    QTableView,      # 테이블 형태로 데이터를 표시하는 위젯
    QPushButton,     # 버튼 위젯
    QLabel,          # 텍스트 라벨 위젯
    QDialog,         # 독립적인 창 (다이얼로그) 위젯
    QHeaderView,     # 테이블 헤더 뷰
    QGridLayout,     # 그리드 형태의 레이아웃
)
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, Signal # Qt.DisplayRole, Qt.Horizontal, QAbstractTableModel, QModelIndex, Signal 등을 위해 사용
from PySide6.QtGui import QFont, QMouseEvent # 폰트 설정, 마우스 이벤트 처리를 위해 사용

# 프로젝트의 다른 부분에서 정의된 클래스들을 임포트합니다.
from model.exchange_rate_model import ExchangeRate # 환율 데이터 모델
from viewmodel.exchange_rate_viewmodel import ExchangeRateViewModel # 뷰와 모델을 연결하는 뷰모델


class ExchangeRateTableModel(QAbstractTableModel):
    """
    환율 데이터를 QTableView에 표시하기 위한 모델 클래스입니다.
    QAbstractTableModel을 상속받아 데이터 제공 방식을 정의합니다.
    """
    def __init__(self, data: list[ExchangeRate]):
        """
        ExchangeRateTableModel의 생성자입니다.

        Args:
            data (list[ExchangeRate]): 테이블에 표시할 ExchangeRate 객체 리스트.
        """
        super().__init__() # QAbstractTableModel의 생성자 호출
        self._data = data # 테이블에 표시할 실제 데이터
        # 테이블 헤더에 표시될 컬럼 이름들을 정의합니다.
        self._headers = [
            "통화코드", "통화명", "전신환(송금) 받으실 때", "전신환(송금) 보내실 때",
            "매매 기준율", "장부가격", "년환가료율", "10일환가료율",
            "서울외국환중개장부가격", "서울외국환중개매매기준율"
        ]

    def rowCount(self, parent=QModelIndex()) -> int:
        """
        테이블의 행(row) 개수를 반환합니다.
        """
        return len(self._data)

    def columnCount(self, parent=QModelIndex()) -> int:
        """
        테이블의 열(column) 개수를 반환합니다.
        """
        return len(self._headers)

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        """
        테이블의 특정 셀에 표시될 데이터를 반환합니다.

        Args:
            index (QModelIndex): 데이터를 요청하는 셀의 인덱스.
            role (int, optional): 요청하는 데이터의 역할. 기본값은 Qt.DisplayRole (표시될 텍스트).

        Returns:
            any: 요청된 역할에 해당하는 데이터.
        """
        if role == Qt.DisplayRole: # 셀에 표시될 텍스트를 요청할 때
            rate = self._data[index.row()] # 해당 행의 ExchangeRate 객체 가져오기
            column = index.column() # 해당 열의 인덱스 가져오기
            # 열 인덱스에 따라 ExchangeRate 객체의 해당 속성 값을 반환
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
        return None # 다른 역할의 데이터는 처리하지 않음

    def headerData(self, section: int, orientation: Qt.Orientation, role=Qt.DisplayRole):
        """
        테이블의 헤더에 표시될 데이터를 반환합니다.

        Args:
            section (int): 헤더의 섹션 인덱스 (행 또는 열).
            orientation (Qt.Orientation): 헤더의 방향 (수평 또는 수직).
            role (int, optional): 요청하는 데이터의 역할. 기본값은 Qt.DisplayRole.

        Returns:
            any: 요청된 역할에 해당하는 헤더 데이터.
        """
        if role == Qt.DisplayRole and orientation == Qt.Horizontal: # 수평 헤더의 표시 텍스트를 요청할 때
            return self._headers[section] # 정의된 헤더 이름 반환
        return None # 다른 역할의 데이터는 처리하지 않음


class ExchangeRateDetailDialog(QDialog):
    """
    특정 환율 정보의 상세 내용을 테이블 형태로 표시하는 다이얼로그 클래스입니다.
    """
    def __init__(self, exchange_rates: list[ExchangeRate], parent=None):
        """
        ExchangeRateDetailDialog의 생성자입니다.

        Args:
            exchange_rates (list[ExchangeRate]): 상세 정보를 표시할 ExchangeRate 객체 리스트.
            parent (QWidget, optional): 부모 위젯. 기본값은 None.
        """
        super().__init__(parent) # QDialog의 생성자 호출
        self.setWindowTitle("환율 정보") # 다이얼로그 제목 설정
        self.setGeometry(100, 100, 800, 600) # 다이얼로그 위치와 크기 설정

        layout = QVBoxLayout(self) # 다이얼로그의 메인 레이아웃을 수직 레이아웃으로 설정

        self.table_view = QTableView() # QTableView 인스턴스 생성
        self.table_model = ExchangeRateTableModel(exchange_rates) # ExchangeRateTableModel 인스턴스 생성
        self.table_view.setModel(self.table_model) # 테이블 뷰에 모델 설정

        # 테이블 헤더 크기 조정: 내용에 맞게 자동으로 크기 조절
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        layout.addWidget(self.table_view) # 레이아웃에 테이블 뷰 추가

        close_button = QPushButton("닫기") # "닫기" 버튼 생성
        close_button.clicked.connect(self.accept) # 버튼 클릭 시 다이얼로그 닫기
        layout.addWidget(close_button) # 레이아웃에 닫기 버튼 추가


class CurrencyRateWidget(QWidget):
    """
    개별 통화의 환율 정보를 시각적으로 표시하는 작은 위젯입니다.
    그리드 레이아웃에 배치되어 주요 환율 정보를 한눈에 볼 수 있도록 합니다.
    """
    clicked = Signal(str) # 위젯이 클릭될 때 통화 코드를 전달하는 시그널

    def __init__(self, currency_code: str, currency_name: str, deal_bas_r: str, parent=None):
        """
        CurrencyRateWidget의 생성자입니다.

        Args:
            currency_code (str): 통화 코드 (예: "USD").
            currency_name (str): 통화명 (예: "미국 달러").
            deal_bas_r (str): 매매 기준율.
            parent (QWidget, optional): 부모 위젯. 기본값은 None.
        """
        super().__init__(parent) # QWidget의 생성자 호출
        self.currency_code = currency_code # 통화 코드 저장
        self.currency_name = currency_name # 통화명 저장
        self.deal_bas_r = deal_bas_r # 매매 기준율 저장

        self.setFixedSize(180, 120) # 위젯의 고정 크기 설정
        # 위젯의 스타일 시트 설정 (배경색, 테두리, 모서리 둥글게)
        self.setStyleSheet("background-color: white; border: 1px solid #ccc; border-radius: 5px;")

        layout = QVBoxLayout(self) # 위젯의 메인 레이아웃을 수직 레이아웃으로 설정
        layout.setAlignment(Qt.AlignCenter) # 레이아웃 내용을 중앙 정렬
        layout.setContentsMargins(0, 0, 0, 0) # 내용 마진 제거
        layout.setSpacing(0) # 위젯 간 간격 제거

        # 모든 정보를 담을 단일 QLabel 생성
        self.info_label = QLabel() 
        self.info_label.setAlignment(Qt.AlignCenter) # 라벨 텍스트 중앙 정렬
        self.info_label.setWordWrap(False) # 자동 줄바꿈 비활성화
        self.info_label.setFixedSize(178, 118) # 라벨의 고정 크기 설정 (위젯 테두리 1px 고려)

        # 폰트 설정
        font_code = QFont() # 통화 코드용 폰트
        font_code.setPointSize(12)
        font_code.setBold(True)

        font_rate = QFont() # 환율 값용 폰트
        font_rate.setPointSize(28)
        font_rate.setBold(True)

        font_name = QFont() # 통화명용 폰트
        font_name.setPointSize(10)

        # HTML을 사용하여 라벨에 텍스트와 스타일을 적용
        # 매매 기준율은 큰 글씨, 통화 코드는 작게, 통화명은 더 작게 표시
        html_text = f"""
        <div style="text-align:center;">
            <div style="font-size:{font_code.pointSize()}pt; font-weight:bold;">{self.currency_code}</div>
            <div style="font-size:{font_rate.pointSize()}pt; font-weight:bold;">{self.deal_bas_r}</div>
            <div style="font-size:{font_name.pointSize()}pt;">{self.currency_name}</div>
        </div>
        """

        self.info_label.setTextFormat(Qt.RichText) # HTML 렌더링 모드로 설정
        self.info_label.setText(html_text) # HTML 내용 적용

        layout.addWidget(self.info_label) # 레이아웃에 정보 라벨 추가

    def mousePressEvent(self, event: QMouseEvent):
        """
        위젯에 마우스 클릭 이벤트가 발생했을 때 호출됩니다.
        좌클릭 시 clicked 시그널을 발생시켜 통화 코드를 전달합니다.

        Args:
            event (QMouseEvent): 마우스 이벤트 객체.
        """
        if event.button() == Qt.LeftButton: # 마우스 좌클릭인 경우
            self.clicked.emit(self.currency_code) # clicked 시그널 발생 및 통화 코드 전달
        super().mousePressEvent(event) # 부모 클래스의 mousePressEvent 호출


class DataViewWidget(QWidget):
    """
    환율 정보를 그리드 형태로 표시하는 메인 데이터 뷰 위젯입니다.
    MVVM 아키텍처에서 View의 역할을 담당하며, ViewModel로부터 데이터를 받아 UI를 업데이트합니다.
    """
    def __init__(self, viewmodel: ExchangeRateViewModel, parent=None):
        """
        DataViewWidget의 생성자입니다.

        Args:
            viewmodel (ExchangeRateViewModel): 연결할 뷰모델 인스턴스.
            parent (QWidget, optional): 부모 위젯. 기본값은 None.
        """
        super().__init__(parent) # QWidget의 생성자 호출
        self.viewmodel = viewmodel # 뷰모델 인스턴스 저장
        self._updating_ui = False # UI 업데이트 중인지 나타내는 플래그 (불필요한 다이얼로그 열림 방지)

        main_layout = QVBoxLayout(self) # 위젯의 메인 레이아웃을 수직 레이아웃으로 설정

        # 환율 정보 표시 그리드 레이아웃
        self.rates_grid_layout = QGridLayout() # QGridLayout 인스턴스 생성
        self.rates_grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft) # 그리드 내용을 상단 왼쪽으로 정렬
        main_layout.addLayout(self.rates_grid_layout) # 메인 레이아웃에 그리드 레이아웃 추가

        main_layout.addStretch() # 그리드 위젯들이 상단에 모이도록 공간 확장

        # 하단 상태 및 새로고침 영역
        bottom_layout = QHBoxLayout() # 하단 위젯들을 수평으로 배치할 레이아웃 생성
        self.status_label = QLabel("준비") # 상태 메시지를 표시할 라벨
        self.refresh_button = QPushButton("새로고침") # 새로고침 버튼
        bottom_layout.addWidget(self.status_label) # 레이아웃에 상태 라벨 추가
        bottom_layout.addStretch() # 상태 라벨과 버튼 사이에 공간 확장
        bottom_layout.addWidget(self.refresh_button) # 레이아웃에 새로고침 버튼 추가

        main_layout.addLayout(bottom_layout) # 메인 레이아웃에 하단 레이아웃 추가

        # --- ViewModel과 View 연결 (데이터 바인딩) ---
        # ViewModel의 exchange_rates_changed 시그널이 발생하면 update_exchange_rates 슬롯 호출
        self.viewmodel.exchange_rates_changed.connect(self.update_exchange_rates)
        # ViewModel의 status_changed 시그널이 발생하면 status_label의 텍스트 업데이트
        self.viewmodel.status_changed.connect(self.status_label.setText)
        # 새로고침 버튼 클릭 시 ViewModel의 fetch_exchange_rates 슬롯 호출
        self.refresh_button.clicked.connect(self.viewmodel.fetch_exchange_rates)

    def update_exchange_rates(self, rates: list[ExchangeRate]):
        """
        ViewModel로부터 업데이트된 환율 데이터를 받아 UI를 갱신합니다.
        기존의 CurrencyRateWidget들을 제거하고 새로운 데이터로 다시 그립니다.

        Args:
            rates (list[ExchangeRate]): 표시할 ExchangeRate 객체 리스트.
        """
        self._updating_ui = True # UI 업데이트 시작 플래그 설정
        # 기존 그리드 레이아웃의 모든 위젯을 역순으로 제거
        for i in reversed(range(self.rates_grid_layout.count())):
            widget_to_remove = self.rates_grid_layout.itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.setParent(None) # 부모 위젯에서 분리
                widget_to_remove.deleteLater() # 위젯 삭제 예약

        if rates: # 환율 데이터가 있을 경우
            row, col = 0, 0 # 그리드 레이아웃의 시작 위치
            for rate in rates:
                if rate.result == 1: # 결과 코드가 1 (성공)인 경우에만 표시
                    currency_widget = CurrencyRateWidget(
                        currency_code=rate.cur_unit,
                        currency_name=rate.cur_nm,
                        deal_bas_r=rate.deal_bas_r
                    ) # CurrencyRateWidget 인스턴스 생성
                    # CurrencyRateWidget 클릭 시 _show_detail_dialog_for_currency 슬롯 호출
                    currency_widget.clicked.connect(self._show_detail_dialog_for_currency)
                    self.rates_grid_layout.addWidget(currency_widget, row, col) # 그리드 레이아웃에 위젯 추가
                    col += 1 # 다음 열로 이동
                    if col >= 4: # 한 줄에 4개씩 표시
                        col = 0 # 열 초기화
                        row += 1 # 다음 행으로 이동
        self._updating_ui = False # UI 업데이트 종료 플래그 설정

    def _show_detail_dialog_for_currency(self, currency_code: str):
        """
        특정 통화 위젯이 클릭되었을 때 해당 통화의 상세 정보를 다이얼로그로 표시합니다.
        UI 업데이트 중에는 다이얼로그가 열리지 않도록 방지합니다.

        Args:
            currency_code (str): 클릭된 통화의 코드.
        """
        if self._updating_ui: # UI 업데이트 중이면 다이얼로그를 열지 않고 반환
            return
        # ViewModel의 _all_exchange_rates에서 클릭된 통화 코드에 해당하는 환율 정보 찾기
        selected_rate = next((r for r in self.viewmodel._all_exchange_rates if r.cur_unit == currency_code), None)
        if selected_rate: # 해당 환율 정보가 존재하면
            dialog = ExchangeRateDetailDialog([selected_rate], self) # 상세 다이얼로그 생성 (단일 통화 정보 전달)
            dialog.exec() # 다이얼로그 실행 (모달)
        else:
            # 환율 정보를 찾을 수 없을 경우 상태 라벨에 메시지 표시
            self.status_label.setText(f"{currency_code} 환율 정보를 찾을 수 없습니다.")