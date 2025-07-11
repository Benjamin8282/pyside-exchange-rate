import sys
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QWidget,
)

from ui.control_panel import ControlPanelWidget
from ui.data_view import DataViewWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("환율 정보 뷰어")
        self.resize(800, 600)

        # 메뉴바 생성
        self._create_menu_bar()

        # 메인 레이아웃 생성
        main_layout = QHBoxLayout()

        # 컨트롤 패널과 데이터 뷰 위젯 생성
        self.control_panel = ControlPanelWidget()
        self.data_view = DataViewWidget()

        # 메인 레이아웃에 위젯 추가
        main_layout.addWidget(self.control_panel)
        main_layout.addWidget(self.data_view)

        # 중앙 위젯 설정
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

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
