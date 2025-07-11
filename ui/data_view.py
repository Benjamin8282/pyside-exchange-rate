from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableView,
    QPushButton,
    QLabel,
)


class DataViewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        # 환율 정보 표시 테이블
        self.table_view = QTableView()
        layout.addWidget(self.table_view)

        # 하단 상태 및 새로고침 영역
        bottom_layout = QHBoxLayout()
        self.status_label = QLabel("준비")
        self.refresh_button = QPushButton("새로고침")
        bottom_layout.addWidget(self.status_label)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.refresh_button)
        layout.addLayout(bottom_layout)
