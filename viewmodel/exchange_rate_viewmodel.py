from PySide6.QtCore import QObject, Signal, Slot
from service.exchange_rate_service import ExchangeRateService
from service.settings_manager import SettingsManager
from model.exchange_rate_model import ExchangeRate

class ExchangeRateViewModel(QObject):
    exchange_rates_changed = Signal(list)
    status_changed = Signal(str)
    available_currencies_changed = Signal(list, dict)

    def __init__(self, service: ExchangeRateService, settings_manager: SettingsManager):
        super().__init__()
        self._service = service
        self._settings_manager = settings_manager
        self._all_exchange_rates: list[ExchangeRate] = []
        self._visible_currencies: dict[str, bool] = self._settings_manager.load_settings()

    @property
    def exchange_rates(self) -> list[ExchangeRate]:
        return [rate for rate in self._all_exchange_rates if self._visible_currencies.get(rate.cur_unit, True)]

    @Slot()
    def fetch_exchange_rates(self):
        self.status_changed.emit("환율 정보를 가져오는 중...")
        rates = self._service.fetch_exchange_rates()
        self._all_exchange_rates = rates

        # 최초 로드 시, visible_currencies에 없는 통화는 기본적으로 True로 설정
        if not self._visible_currencies:
            for rate in rates:
                self._visible_currencies[rate.cur_unit] = True
            self._settings_manager.save_settings(self._visible_currencies)

        self._emit_filtered_rates()
        self._emit_available_currencies()

        if rates:
            self.status_changed.emit(f"총 {len(rates)}개 환율 정보 로드 완료")
        else:
            self.status_changed.emit("환율 정보를 가져오지 못했습니다.")

    @Slot(str, bool)
    def set_currency_visibility(self, currency_code: str, is_visible: bool):
        self._visible_currencies[currency_code] = is_visible
        self._settings_manager.save_settings(self._visible_currencies)
        self._emit_filtered_rates()

    @Slot()
    def select_all_currencies(self):
        for rate in self._all_exchange_rates:
            self._visible_currencies[rate.cur_unit] = True
        self._settings_manager.save_settings(self._visible_currencies)
        self._emit_filtered_rates()
        self._emit_available_currencies()

    @Slot()
    def deselect_all_currencies(self):
        for rate in self._all_exchange_rates:
            self._visible_currencies[rate.cur_unit] = False
        self._settings_manager.save_settings(self._visible_currencies)
        self._emit_filtered_rates()
        self._emit_available_currencies()

    def _emit_filtered_rates():
        self.exchange_rates_changed.emit(self.exchange_rates)

    def _emit_available_currencies(self):
        # 현재 로드된 모든 통화 목록과 가시성 설정을 전달
        currencies_list = [(rate.cur_unit, rate.cur_nm) for rate in self._all_exchange_rates if rate.result == 1]
        self.available_currencies_changed.emit(currencies_list, self._visible_currencies)
