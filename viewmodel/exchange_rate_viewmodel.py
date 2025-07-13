from PySide6.QtCore import QObject, Signal, Slot
from service.exchange_rate_service import ExchangeRateService
from model.exchange_rate_model import ExchangeRate

class ExchangeRateViewModel(QObject):
    exchange_rates_changed = Signal(list)
    status_changed = Signal(str)

    def __init__(self, service: ExchangeRateService):
        super().__init__()
        self._service = service
        self._exchange_rates: list[ExchangeRate] = []

    @property
    def exchange_rates(self) -> list[ExchangeRate]:
        return self._exchange_rates

    @Slot()
    def fetch_exchange_rates(self):
        self.status_changed.emit("환율 정보를 가져오는 중...")
        rates = self._service.fetch_exchange_rates()
        self._exchange_rates = rates
        self.exchange_rates_changed.emit(self._exchange_rates)
        if rates:
            self.status_changed.emit(f"총 {len(rates)}개 환율 정보 로드 완료")
        else:
            self.status_changed.emit("환율 정보를 가져오지 못했습니다.")
