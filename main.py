import os
import sys
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget, QVBoxLayout,
)

from ui.data_view import DataViewWidget
from service.exchange_rate_service import ExchangeRateService
from viewmodel.exchange_rate_viewmodel import ExchangeRateViewModel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("환율 정보 뷰어")
        self.resize(1000, 700)

        # Service와 ViewModel 초기화
        AUTH_KEY = os.getenv("AUTH_KEY")
        if not AUTH_KEY:
            print("AUTH_KEY 환경 변수가 설정되지 않았습니다. .env 파일을 확인해주세요.")
            sys.exit(1)

        self.exchange_service = ExchangeRateService(AUTH_KEY)
        self.exchange_viewmodel = ExchangeRateViewModel(self.exchange_service)

        # 메뉴바 생성
        self._create_menu_bar()

        # 메인 레이아웃 생성
        main_layout = QVBoxLayout()

        # 데이터 뷰 위젯 생성
        self.data_view = DataViewWidget(self.exchange_viewmodel)

        # 메인 레이아웃에 위젯 추가
        main_layout.addWidget(self.data_view)

        # 중앙 위젯 설정
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

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