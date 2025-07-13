import os
import sys
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget, QVBoxLayout, QHBoxLayout
)

from ui.data_view import DataViewWidget
from ui.control_panel import ControlPanelWidget
from service.exchange_rate_service import ExchangeRateService
from service.settings_manager import SettingsManager
from viewmodel.exchange_rate_viewmodel import ExchangeRateViewModel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("환율 정보 뷰어")
        self.resize(1200, 700) # 창 크기 조정

        # Service, SettingsManager, ViewModel 초기화
        AUTH_KEY = os.getenv("AUTH_KEY")
        if not AUTH_KEY:
            print("AUTH_KEY 환경 변수가 설정되지 않았습니다. .env 파일을 확인해주세요.")
            sys.exit(1)

        self.exchange_service = ExchangeRateService(AUTH_KEY)
        self.settings_manager = SettingsManager()
        self.exchange_viewmodel = ExchangeRateViewModel(self.exchange_service, self.settings_manager)

        # 메뉴바 생성
        self._create_menu_bar()

        # 메인 레이아웃 생성 (좌측 패널 + 우측 데이터 뷰)
        main_horizontal_layout = QHBoxLayout()

        # 좌측 제어 패널 위젯 생성
        self.control_panel = ControlPanelWidget()
        main_horizontal_layout.addWidget(self.control_panel)

        # 우측 데이터 뷰 위젯 생성
        self.data_view = DataViewWidget(self.exchange_viewmodel)
        main_horizontal_layout.addWidget(self.data_view)

        # 중앙 위젯 설정
        central_widget = QWidget()
        central_widget.setLayout(main_horizontal_layout)
        self.setCentralWidget(central_widget)

        # ViewModel과 View 연결
        self.exchange_viewmodel.exchange_rates_changed.connect(self.data_view.update_exchange_rates)
        self.exchange_viewmodel.status_changed.connect(self.data_view.status_label.setText)
        self.exchange_viewmodel.available_currencies_changed.connect(self.control_panel.populate_currencies)

        # ControlPanel의 시그널을 ViewModel의 슬롯에 연결
        self.control_panel.visibility_changed.connect(self.exchange_viewmodel.set_currency_visibility)

        # 새로고침 버튼 연결 (DataViewWidget 내부에 있으므로 DataViewWidget에서 연결)
        self.data_view.refresh_button.clicked.connect(self.exchange_viewmodel.fetch_exchange_rates)

        # 초기 환율 정보 로드
        self.exchange_viewmodel.fetch_exchange_rates()

    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("파일")

        exit_action = QAction("종료", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())