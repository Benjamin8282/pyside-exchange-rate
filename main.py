# -*- coding: utf-8 -*-

# 필요한 모듈들을 임포트합니다.
import os # 환경 변수 접근을 위해 사용
import sys # 시스템 관련 기능 (예: 애플리케이션 종료)을 위해 사용
from PySide6.QtGui import QAction # 메뉴바 액션 생성을 위해 사용
from PySide6.QtWidgets import (
    QApplication, # PySide6 애플리케이션 객체
    QMainWindow,  # 메인 윈도우 클래스
    QWidget,      # 기본 위젯 클래스
    QVBoxLayout,  # 수직 레이아웃
    QHBoxLayout   # 수평 레이아웃
)

# 프로젝트의 다른 부분에서 정의된 클래스들을 임포트합니다.
from ui.data_view import DataViewWidget         # 환율 데이터를 표시하는 뷰 위젯
from ui.control_panel import ControlPanelWidget # 통화 선택 및 제어 패널 위젯
from service.exchange_rate_service import ExchangeRateService # 환율 데이터를 가져오는 서비스
from service.settings_manager import SettingsManager         # 애플리케이션 설정을 저장/로드하는 매니저
from viewmodel.exchange_rate_viewmodel import ExchangeRateViewModel # 뷰와 모델을 연결하는 뷰모델


class MainWindow(QMainWindow):
    """
    애플리케이션의 메인 윈도우를 정의하는 클래스입니다.
    MVVM 아키텍처에서 View의 역할을 담당하며, ViewModel과 상호작용하여 UI를 업데이트합니다.
    """
    def __init__(self):
        """
        MainWindow의 생성자입니다.
        UI 초기화, 서비스/뷰모델 설정, 시그널/슬롯 연결 등을 수행합니다.
        """
        super().__init__() # QMainWindow의 생성자 호출
        self.setWindowTitle("환율 정보 뷰어") # 윈도우 제목 설정
        self.resize(1200, 700) # 윈도우 초기 크기 설정

        # --- MVVM 아키텍처 컴포넌트 초기화 ---
        # 1. Service 초기화: 외부 API와 통신하여 실제 데이터를 가져오는 역할
        AUTH_KEY = os.getenv("AUTH_KEY") # .env 파일에서 AUTH_KEY 환경 변수 로드
        if not AUTH_KEY:
            # AUTH_KEY가 설정되지 않았다면 오류 메시지 출력 후 애플리케이션 종료
            print("AUTH_KEY 환경 변수가 설정되지 않았습니다. .env 파일을 확인해주세요.")
            sys.exit(1)

        self.exchange_service = ExchangeRateService(AUTH_KEY) # ExchangeRateService 인스턴스 생성
        self.settings_manager = SettingsManager()             # SettingsManager 인스턴스 생성 (설정 저장/로드)
        # 2. ViewModel 초기화: View와 Service(Model) 사이의 중재자 역할
        self.exchange_viewmodel = ExchangeRateViewModel(self.exchange_service, self.settings_manager)

        # --- UI 컴포넌트 설정 ---
        self._create_menu_bar() # 메뉴바 생성

        # 메인 레이아웃 설정: 좌측 제어 패널과 우측 데이터 뷰를 수평으로 배치
        main_horizontal_layout = QHBoxLayout()

        # 좌측 제어 패널 위젯 생성 및 레이아웃에 추가
        self.control_panel = ControlPanelWidget() # ControlPanelWidget 인스턴스 생성
        main_horizontal_layout.addWidget(self.control_panel) # 레이아웃에 추가

        # 우측 데이터 뷰 위젯 생성 및 레이아웃에 추가
        self.data_view = DataViewWidget(self.exchange_viewmodel) # DataViewWidget 인스턴스 생성 (뷰모델 전달)
        main_horizontal_layout.addWidget(self.data_view) # 레이아웃에 추가

        # 중앙 위젯 설정: 생성된 레이아웃을 메인 윈도우의 중앙 위젯으로 설정
        central_widget = QWidget() # 빈 QWidget 생성
        central_widget.setLayout(main_horizontal_layout) # 레이아웃 설정
        self.setCentralWidget(central_widget) # 메인 윈도우의 중앙 위젯으로 설정

        # --- ViewModel과 View 간의 데이터 바인딩 및 이벤트 연결 ---
        # ViewModel의 exchange_rates_changed 시그널이 발생하면 DataViewWidget의 update_exchange_rates 슬롯 호출
        self.exchange_viewmodel.exchange_rates_changed.connect(self.data_view.update_exchange_rates)
        # ViewModel의 status_changed 시그널이 발생하면 DataViewWidget의 status_label 텍스트 업데이트
        self.exchange_viewmodel.status_changed.connect(self.data_view.status_label.setText)
        # ViewModel의 available_currencies_changed 시그널이 발생하면 ControlPanel의 populate_currencies 슬롯 호출
        self.exchange_viewmodel.available_currencies_changed.connect(self.control_panel.populate_currencies)

        # ControlPanel의 visibility_changed 시그널이 발생하면 ViewModel의 set_currency_visibility 슬롯 호출
        self.control_panel.visibility_changed.connect(self.exchange_viewmodel.set_currency_visibility)
        # ControlPanel의 select_all_requested 시그널이 발생하면 ViewModel의 select_all_currencies 슬롯 호출
        self.control_panel.select_all_requested.connect(self.exchange_viewmodel.select_all_currencies)
        # ControlPanel의 deselect_all_requested 시그널이 발생하면 ViewModel의 deselect_all_currencies 슬롯 호출
        self.control_panel.deselect_all_requested.connect(self.exchange_viewmodel.deselect_all_currencies)

        # DataViewWidget 내부에 있는 새로고침 버튼의 clicked 시그널을 ViewModel의 fetch_exchange_rates 슬롯에 연결
        self.data_view.refresh_button.clicked.connect(self.exchange_viewmodel.fetch_exchange_rates)

        # 애플리케이션 시작 시 초기 환율 정보 로드 요청
        self.exchange_viewmodel.fetch_exchange_rates()

    def _create_menu_bar(self):
        """
        메인 윈도우의 메뉴바를 생성하는 메서드입니다.
        """
        menu_bar = self.menuBar() # 메인 윈도우의 메뉴바 객체 가져오기
        file_menu = menu_bar.addMenu("파일") # '파일' 메뉴 추가

        # '종료' 액션 생성 및 메뉴에 추가
        exit_action = QAction("종료", self) # '종료'라는 텍스트를 가진 QAction 생성
        exit_action.triggered.connect(self.close) # 액션이 트리거되면 윈도우 닫기 메서드 연결
        file_menu.addAction(exit_action) # '파일' 메뉴에 '종료' 액션 추가


if __name__ == "__main__":
    """
    애플리케이션의 메인 실행 블록입니다.
    """
    app = QApplication(sys.argv) # QApplication 인스턴스 생성 (모든 PySide6 애플리케이션의 시작점)
    window = MainWindow() # MainWindow 인스턴스 생성
    window.show() # 메인 윈도우를 화면에 표시
    sys.exit(app.exec()) # 애플리케이션 이벤트 루프 시작 및 종료 시 반환 코드 전달
