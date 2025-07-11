import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QTableView,
    QPushButton,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QComboBox,
    QLineEdit,
    QMenuBar,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("환율 정보 뷰어")
        self.resize(800, 600)

        # 메뉴바 생성
        self._create_menu_bar()

        # 메인 레이아웃 생성 (좌: 컨트롤 패널, 우: 데이터 뷰)
        main_layout = QHBoxLayout()

        # --- 좌측 컨트롤 패널 ---
        control_panel_layout = QVBoxLayout()

        # 기준 통화 선택
        control_panel_layout.addWidget(QLabel("기준 통화:"))
        self.base_currency_combo = QComboBox()
        control_panel_layout.addWidget(self.base_currency_combo)

        # 통화 검색
        control_panel_layout.addWidget(QLabel("통화 검색:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("예: USD, 유로")
        control_panel_layout.addWidget(self.search_input)

        # 표시할 통화 선택 리스트
        control_panel_layout.addWidget(QLabel("표시할 통화:"))
        self.currency_list_widget = QListWidget()
        self.currency_list_widget.setSelectionMode(QListWidget.MultiSelection)
        control_panel_layout.addWidget(self.currency_list_widget)

        # 컨트롤 패널을 담을 위젯
        control_panel_widget = QWidget()
        control_panel_widget.setLayout(control_panel_layout)
        control_panel_widget.setMaximumWidth(250)

        # --- 우측 데이터 뷰 ---
        data_view_layout = QVBoxLayout()

        # 환율 정보 표시 테이블
        self.table_view = QTableView()
        data_view_layout.addWidget(self.table_view)

        # 하단 상태 및 새로고침 영역
        bottom_layout = QHBoxLayout()
        self.status_label = QLabel("준비")
        self.refresh_button = QPushButton("새로고침")
        bottom_layout.addWidget(self.status_label)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.refresh_button)
        data_view_layout.addLayout(bottom_layout)

        # 데이터 뷰를 담을 위젯
        data_view_widget = QWidget()
        data_view_widget.setLayout(data_view_layout)

        # 메인 레이아웃에 컨트롤 패널과 데이터 뷰 추가
        main_layout.addWidget(control_panel_widget)
        main_layout.addWidget(data_view_widget)

        # 중앙 위젯 설정
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # 임시 데이터 추가 (테스트용)
        self._add_temp_data()

    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("파일")

        exit_action = QAction("종료", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def _add_temp_data(self):
        # 임시 기준 통화
        self.base_currency_combo.addItems(["KRW", "USD", "EUR", "JPY"])

        # 임시 통화 목록
        currencies = ["USD (미국 달러)", "EUR (유로)", "JPY (일본 옌)", "CNY (중국 위안)", "GBP (영국 파운드)"]
        for currency in currencies:
            item = QListWidgetItem(currency)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.currency_list_widget.addItem(item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
