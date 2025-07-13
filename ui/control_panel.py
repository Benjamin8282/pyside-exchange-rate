# -*- coding: utf-8 -*-

# 필요한 모듈들을 임포트합니다.
from PySide6.QtCore import Qt, Signal # Qt.DisplayRole, Qt.UserRole, Signal 등을 위해 사용
from PySide6.QtWidgets import (
    QWidget,         # 기본 위젯 클래스
    QVBoxLayout,     # 수직 레이아웃
    QLabel,          # 텍스트 라벨
    QListWidget,     # 리스트 형태의 위젯
    QListWidgetItem, # QListWidget의 각 항목
    QLineEdit,       # 한 줄 텍스트 입력 필드
    QPushButton,     # 버튼
    QHBoxLayout      # 수평 레이아웃
)


class ControlPanelWidget(QWidget):
    """
    애플리케이션의 좌측 제어 패널을 정의하는 위젯입니다.
    통화 검색, 표시할 통화 선택 리스트, 그리고 모두 선택/해제 버튼을 포함합니다.
    MVVM 아키텍처에서 View의 역할을 담당하며, 사용자 입력을 받아 ViewModel에 시그널을 보냅니다.
    """
    # 사용자 정의 시그널 정의
    # 통화의 표시 여부가 변경될 때 (통화 코드, 표시 여부)를 전달합니다.
    visibility_changed = Signal(str, bool)
    # 모든 통화를 선택하라는 요청이 있을 때 발생합니다.
    select_all_requested = Signal()
    # 모든 통화를 해제하라는 요청이 있을 때 발생합니다.
    deselect_all_requested = Signal()

    def __init__(self, parent=None):
        """
        ControlPanelWidget의 생성자입니다.
        UI 컴포넌트들을 초기화하고 레이아웃을 설정합니다.

        Args:
            parent (QWidget, optional): 부모 위젯. 기본값은 None.
        """
        super().__init__(parent) # QWidget의 생성자 호출

        layout = QVBoxLayout(self) # 위젯의 메인 레이아웃을 수직 레이아웃으로 설정

        # --- 통화 검색 섹션 ---
        layout.addWidget(QLabel("통화 검색:")) # "통화 검색:" 라벨 추가
        self.search_input = QLineEdit() # 검색어 입력 필드 생성
        self.search_input.setPlaceholderText("예: USD, 유로") # 플레이스홀더 텍스트 설정
        # 검색어 입력 필드의 텍스트가 변경될 때 _filter_currencies 메서드 호출
        self.search_input.textChanged.connect(self._filter_currencies)
        layout.addWidget(self.search_input) # 레이아웃에 검색 입력 필드 추가

        # --- 표시할 통화 선택 리스트 섹션 ---
        layout.addWidget(QLabel("표시할 통화:")) # "표시할 통화:" 라벨 추가
        self.currency_list_widget = QListWidget() # 통화 목록을 표시할 QListWidget 생성
        # QListWidget의 항목 체크 상태가 변경될 때 _on_item_changed 메서드 호출
        self.currency_list_widget.itemChanged.connect(self._on_item_changed)
        layout.addWidget(self.currency_list_widget) # 레이아웃에 통화 리스트 위젯 추가

        # --- 모두 선택/해제 버튼 섹션 ---
        button_layout = QHBoxLayout() # 버튼들을 수평으로 배치할 레이아웃 생성
        
        self.select_all_button = QPushButton("모두 선택") # "모두 선택" 버튼 생성
        # 버튼 클릭 시 select_all_requested 시그널 발생
        self.select_all_button.clicked.connect(self.select_all_requested.emit)
        button_layout.addWidget(self.select_all_button) # 레이아웃에 버튼 추가

        self.deselect_all_button = QPushButton("모두 해제") # "모두 해제" 버튼 생성
        # 버튼 클릭 시 deselect_all_requested 시그널 발생
        self.deselect_all_button.clicked.connect(self.deselect_all_requested.emit)
        button_layout.addWidget(self.deselect_all_button) # 레이아웃에 버튼 추가

        layout.addLayout(button_layout) # 메인 레이아웃에 버튼 레이아웃 추가

        self.setMaximumWidth(250) # 위젯의 최대 너비 설정

    def populate_currencies(self, currencies: list[tuple[str, str]], visible_currencies: dict):
        """
        API로부터 받아온 통화 목록과 현재 표시 설정에 따라 QListWidget을 채웁니다.

        Args:
            currencies (list[tuple[str, str]]): (통화 코드, 통화명) 튜플의 리스트.
            visible_currencies (dict): 통화 코드(str)를 키로, 표시 여부(bool)를 값으로 하는 딕셔너리.
        """
        # 시그널 발생을 일시적으로 차단하여 불필요한 _on_item_changed 호출 방지
        self.currency_list_widget.blockSignals(True)
        self.currency_list_widget.clear() # 기존 목록 초기화
        for code, name in currencies:
            item = QListWidgetItem(f"{code} ({name})") # "USD (미국 달러)"와 같은 형식으로 항목 생성
            item.setData(Qt.UserRole, code) # 항목에 통화 코드(숨겨진 데이터) 저장
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable) # 항목을 체크 가능하도록 설정
            # visible_currencies 딕셔너리에서 해당 통화의 표시 여부를 가져오고, 없으면 기본값 True
            is_checked = visible_currencies.get(code, True)
            # 체크 상태 설정 (True면 체크됨, False면 체크 해제됨)
            item.setCheckState(Qt.Checked if is_checked else Qt.Unchecked)
            self.currency_list_widget.addItem(item) # QListWidget에 항목 추가
        self.currency_list_widget.blockSignals(False) # 시그널 발생 차단 해제

    def _on_item_changed(self, item: QListWidgetItem):
        """
        QListWidget의 항목 체크 상태가 변경될 때 호출되는 슬롯입니다.
        변경 사항을 ViewModel에 알리기 위해 visibility_changed 시그널을 발생시킵니다.

        Args:
            item (QListWidgetItem): 체크 상태가 변경된 항목.
        """
        currency_code = item.data(Qt.UserRole) # 항목에 저장된 통화 코드 가져오기
        is_checked = item.checkState() == Qt.Checked # 현재 체크 상태 확인
        self.visibility_changed.emit(currency_code, is_checked) # 시그널 발생

    def _filter_currencies(self, text: str):
        """
        검색어 입력 필드의 텍스트에 따라 통화 목록을 필터링합니다.
        검색어와 일치하지 않는 항목은 숨깁니다.

        Args:
            text (str): 검색어.
        """
        for i in range(self.currency_list_widget.count()): # 모든 항목을 순회
            item = self.currency_list_widget.item(i) # 현재 항목 가져오기
            # 항목 텍스트에 검색어가 포함되어 있지 않으면 숨김 처리
            item.setHidden(text.lower() not in item.text().lower())