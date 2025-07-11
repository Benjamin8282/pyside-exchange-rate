import sys
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget, QVBoxLayout,
)

from ui.data_view import DataViewWidget
from core.exchange_rate_manager import ExchangeRateManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("환율 정보 뷰어")
        self.resize(1000, 700) # 창 크기 조정

        # ExchangeRateManager 초기화
        # 실제 사용 시에는 발급받은 인증키를 사용하세요.
        AUTH_KEY = "qxf4jMteliYvRPID4ELzuARpeFIJUuha"  # 발급받은 인증키
        self.exchange_manager = ExchangeRateManager(AUTH_KEY)

        # 메뉴바 생성
        self._create_menu_bar()

        # 메인 레이아웃 생성
        main_layout = QVBoxLayout() # QHBoxLayout 대신 QVBoxLayout 사용

        # 데이터 뷰 위젯 생성
        self.data_view = DataViewWidget()

        # 메인 레이아웃에 위젯 추가
        
        main_layout.addWidget(self.data_view)

        # 중앙 위젯 설정
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # 새로고침 버튼 연결
        self.data_view.refresh_button.clicked.connect(self._refresh_exchange_rates)

        # 초기 환율 정보 로드
        self._refresh_exchange_rates()

    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("파일")

        exit_action = QAction("종료", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def _refresh_exchange_rates(self):
        self.data_view.status_label.setText("환율 정보를 가져오는 중...")
        rates = self.exchange_manager.fetch_exchange_rates()
        self.data_view.update_exchange_rates(rates)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())