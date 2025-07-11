import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QTableView,
    QPushButton,
    QLabel,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("환율 정보 뷰어")
        self.resize(800, 600)

        # 전체 레이아웃 설정
        layout = QVBoxLayout()

        # 환율 정보를 표시할 테이블 뷰
        self.table_view = QTableView()
        layout.addWidget(self.table_view)

        # 새로고침 버튼
        self.refresh_button = QPushButton("새로고침")
        layout.addWidget(self.refresh_button)

        # 상태 표시 레이블
        self.status_label = QLabel("준비")
        layout.addWidget(self.status_label)

        # 중앙 위젯 설정
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
