# -*- coding: utf-8 -*-

# 필요한 모듈들을 임포트합니다.
from PySide6.QtCore import QObject, Signal, Slot # PySide6의 시그널/슬롯 메커니즘을 위해 사용
from service.exchange_rate_service import ExchangeRateService # 환율 데이터를 가져오는 서비스
from service.settings_manager import SettingsManager         # 애플리케이션 설정을 저장/로드하는 매니저
from model.exchange_rate_model import ExchangeRate # 환율 데이터 모델


class ExchangeRateViewModel(QObject):
    """
    MVVM 아키텍처에서 ViewModel의 역할을 담당하는 클래스입니다.
    View와 Model(Service) 사이의 중재자 역할을 하며, UI의 상태를 관리하고 비즈니스 로직을 View에 노출합니다.
    """
    # --- 시그널 정의 ---
    # 필터링된 환율 데이터가 변경될 때 View에 알리는 시그널
    exchange_rates_changed = Signal(list)
    # 애플리케이션 상태 메시지가 변경될 때 View에 알리는 시그널
    status_changed = Signal(str)
    # 사용 가능한 통화 목록 및 현재 가시성 설정이 변경될 때 View에 알리는 시그널
    available_currencies_changed = Signal(list, dict)

    def __init__(self, service: ExchangeRateService, settings_manager: SettingsManager):
        """
        ExchangeRateViewModel의 생성자입니다.

        Args:
            service (ExchangeRateService): 환율 데이터를 제공하는 서비스 인스턴스.
            settings_manager (SettingsManager): 설정을 저장하고 로드하는 매니저 인스턴스.
        """
        super().__init__() # QObject의 생성자 호출
        self._service = service # 환율 서비스 인스턴스 저장
        self._settings_manager = settings_manager # 설정 매니저 인스턴스 저장
        self._all_exchange_rates: list[ExchangeRate] = [] # API로부터 가져온 모든 환율 데이터를 저장
        # settings.xml에서 이전에 저장된 통화 가시성 설정을 로드합니다.
        # 키: 통화 코드 (str), 값: 표시 여부 (bool)
        self._visible_currencies: dict[str, bool] = self._settings_manager.load_settings()

    @property
    def exchange_rates(self) -> list[ExchangeRate]:
        """
        현재 표시 설정에 따라 필터링된 환율 데이터 리스트를 반환하는 속성입니다.
        View는 이 속성을 통해 표시할 데이터를 가져옵니다.
        """
        # _all_exchange_rates에서 _visible_currencies에 따라 필터링된 환율만 반환
        # _visible_currencies에 해당 통화 코드가 없으면 기본적으로 True (표시)로 간주
        return [rate for rate in self._all_exchange_rates if self._visible_currencies.get(rate.cur_unit, True)]

    @Slot() # PySide6 슬롯으로 등록하여 시그널과 연결 가능하게 함
    def fetch_exchange_rates(self):
        """
        환율 데이터를 비동기적으로 가져오는 메서드입니다.
        Service를 통해 데이터를 요청하고, 가져온 데이터를 처리하여 View에 업데이트를 알립니다.
        """
        self.status_changed.emit("환율 정보를 가져오는 중...") # View에 상태 메시지 업데이트 요청
        rates = self._service.fetch_exchange_rates() # Service를 통해 환율 데이터 가져오기
        self._all_exchange_rates = rates # 가져온 모든 환율 데이터를 저장

        # 애플리케이션 최초 로드 시, _visible_currencies가 비어있다면
        # 현재 가져온 모든 통화를 기본적으로 표시(True)하도록 설정하고 저장
        if not self._visible_currencies:
            for rate in rates:
                self._visible_currencies[rate.cur_unit] = True
            self._settings_manager.save_settings(self._visible_currencies)

        self._emit_filtered_rates() # 필터링된 환율 데이터 변경 시그널 발생
        self._emit_available_currencies() # 사용 가능한 통화 목록 변경 시그널 발생

        if rates:
            self.status_changed.emit(f"총 {len(rates)}개 환율 정보 로드 완료") # 성공 메시지
        else:
            self.status_changed.emit("환율 정보를 가져오지 못했습니다.") # 실패 메시지

    @Slot(str, bool) # PySide6 슬롯으로 등록
    def set_currency_visibility(self, currency_code: str, is_visible: bool):
        """
        특정 통화의 표시 여부를 설정하고, 변경된 설정을 저장하며 View를 업데이트합니다.

        Args:
            currency_code (str): 표시 여부를 변경할 통화의 코드.
            is_visible (bool): 해당 통화를 표시할지(True) 숨길지(False).
        """
        self._visible_currencies[currency_code] = is_visible # 통화의 가시성 설정 업데이트
        self._settings_manager.save_settings(self._visible_currencies) # 변경된 설정 저장
        self._emit_filtered_rates() # 필터링된 환율 데이터 변경 시그널 발생 (UI 업데이트)

    @Slot() # PySide6 슬롯으로 등록
    def select_all_currencies(self):
        """
        모든 통화를 표시하도록 설정하고, 변경된 설정을 저장하며 View를 업데이트합니다.
        """
        for rate in self._all_exchange_rates:
            self._visible_currencies[rate.cur_unit] = True # 모든 통화를 표시로 설정
        self._settings_manager.save_settings(self._visible_currencies) # 변경된 설정 저장
        self._emit_filtered_rates() # 필터링된 환율 데이터 변경 시그널 발생
        self._emit_available_currencies() # 사용 가능한 통화 목록 변경 시그널 발생 (UI 업데이트)

    @Slot() # PySide6 슬롯으로 등록
    def deselect_all_currencies(self):
        """
        모든 통화를 숨기도록 설정하고, 변경된 설정을 저장하며 View를 업데이트합니다.
        """
        for rate in self._all_exchange_rates:
            self._visible_currencies[rate.cur_unit] = False # 모든 통화를 숨김으로 설정
        self._settings_manager.save_settings(self._visible_currencies) # 변경된 설정 저장
        self._emit_filtered_rates() # 필터링된 환율 데이터 변경 시그널 발생
        self._emit_available_currencies() # 사용 가능한 통화 목록 변경 시그널 발생 (UI 업데이트)

    def _emit_filtered_rates(self):
        """
        현재 필터링된 환율 데이터를 View에 전달하기 위해 `exchange_rates_changed` 시그널을 발생시킵니다.
        """
        self.exchange_rates_changed.emit(self.exchange_rates)

    def _emit_available_currencies(self):
        """
        현재 로드된 모든 통화 목록과 그들의 가시성 설정을 View에 전달하기 위해
        `available_currencies_changed` 시그널을 발생시킵니다.
        """
        # API 응답 결과가 1(성공)인 통화만 목록에 포함
        currencies_list = [(rate.cur_unit, rate.cur_nm) for rate in self._all_exchange_rates if rate.result == 1]
        self.available_currencies_changed.emit(currencies_list, self._visible_currencies)