# -*- coding: utf-8 -*-

# 필요한 모듈들을 임포트합니다.
from api.client import ExchangeRateClient # API 통신을 위한 클라이언트
from model.exchange_rate_model import ExchangeRate # 환율 데이터 모델
import datetime # 날짜 및 시간 관련 기능


class ExchangeRateService:
    """
    환율 데이터를 관리하고 비즈니스 로직을 수행하는 서비스 클래스입니다.
    API 클라이언트를 통해 데이터를 가져오고, 필요한 경우 데이터 파싱 및 재시도 로직을 포함합니다.
    MVVM 아키텍처에서 Model의 일부 역할을 담당합니다.
    """
    def __init__(self, authkey: str):
        """
        ExchangeRateService의 생성자입니다.

        Args:
            authkey (str): 한국수출입은행 API 인증키.
        """
        self.client = ExchangeRateClient(authkey) # API 클라이언트 인스턴스 생성
        self.exchange_rates: list[ExchangeRate] = [] # 가져온 환율 정보를 저장할 리스트

    def fetch_exchange_rates(self, searchdate: str = None) -> list[ExchangeRate]:
        """
        지정된 날짜 또는 현재 날짜의 환율 정보를 API로부터 가져옵니다.
        데이터를 성공적으로 가져올 때까지 최대 7일까지 이전 날짜를 재시도합니다.

        Args:
            searchdate (str, optional): 조회할 날짜 (YYYYMMDD 형식의 문자열). 기본값은 None (오늘 날짜).

        Returns:
            list[ExchangeRate]: 가져온 환율 정보(ExchangeRate 객체 리스트)를 반환합니다.
                                데이터를 가져오지 못하면 빈 리스트를 반환합니다.
        """
        # 조회할 날짜를 결정합니다.
        if searchdate is None:
            current_date = datetime.date.today() # searchdate가 없으면 오늘 날짜 사용
        else:
            # searchdate가 있으면 해당 문자열을 datetime 객체로 변환
            current_date = datetime.datetime.strptime(searchdate, "%Y%m%d").date()

        max_retries = 7  # API 호출 재시도 최대 횟수 (주말 및 공휴일 고려)
        for _ in range(max_retries):
            search_date_str = current_date.strftime("%Y%m%d") # 현재 날짜를 YYYYMMDD 형식으로 변환
            raw_rates = self.client.get_exchange_rates(search_date_str) # API 클라이언트를 통해 환율 정보 요청
            
            # API 응답이 유효한지 확인합니다.
            # raw_rates가 None이 아니고, (결과가 1개이고 result 코드가 4인 경우)가 아닌 경우
            # result 4는 '조회 결과 없음'을 의미하며, 이 경우에도 재시도가 필요합니다.
            if raw_rates and not (len(raw_rates) == 1 and raw_rates[0].get('result') == 4):
                self.exchange_rates = [] # 기존 환율 정보 초기화
                for rate_data in raw_rates:
                    result = rate_data.get('result', 1) # 결과 코드 가져오기 (기본값 1: 성공)
                    if result != 1:
                        # 결과 코드가 1이 아니면 오류 메시지 출력 후 다음 데이터로 넘어감
                        print(f"API 응답 오류: {rate_data.get('cur_nm', 'Unknown Currency')} - Result Code: {result}")
                        continue
                    try:
                        # API 응답 데이터를 ExchangeRate 객체로 파싱하여 리스트에 추가
                        rate = ExchangeRate(
                            result=result,
                            cur_unit=rate_data.get('cur_unit', ''),
                            ttb=rate_data.get('ttb', ''),
                            tts=rate_data.get('tts', ''),
                            deal_bas_r=rate_data.get('deal_bas_r', ''),
                            bkpr=rate_data.get('bkpr', ''),
                            yy_efee_r=rate_data.get('yy_efee_r', ''),
                            ten_dd_efee_r=rate_data.get('ten_dd_efee_r', ''),
                            kftc_bkpr=rate_data.get('bkpr', ''),
                            kftc_deal_bas_r=rate_data.get('kftc_deal_bas_r', ''),
                            cur_nm=rate_data.get('cur_nm', '')
                        )
                        self.exchange_rates.append(rate)
                    except TypeError as e:
                        # 데이터 파싱 중 타입 오류 발생 시 처리
                        print(f"환율 데이터 파싱 오류: {e} - Data: {rate_data}")
                if self.exchange_rates: # 파싱된 데이터가 하나라도 있으면 반환
                    return self.exchange_rates
            
            # 데이터가 없거나 오류 응답인 경우, 하루 전으로 날짜를 변경하여 재시도
            current_date -= datetime.timedelta(days=1)
            print(f"데이터를 찾을 수 없습니다. 이전 날짜 {current_date.strftime('%Y%m%d')}로 재시도합니다.")

        # 최대 재시도 횟수를 초과하면 오류 메시지 출력 후 빈 리스트 반환
        print("최대 재시도 횟수를 초과했습니다. 환율 정보를 가져오지 못했습니다.")
        return []

    def get_exchange_rate_by_currency(self, currency_code: str) -> ExchangeRate | None:
        """
        특정 통화 코드에 해당하는 환율 정보를 반환합니다.

        Args:
            currency_code (str): 찾을 통화 코드 (예: "USD").

        Returns:
            ExchangeRate | None: 해당 통화 코드의 ExchangeRate 객체를 반환하거나, 없으면 None을 반환합니다.
        """
        for rate in self.exchange_rates:
            if rate.cur_unit == currency_code:
                return rate
        return None

    def get_all_exchange_rates(self) -> list[ExchangeRate]:
        """
        현재 서비스에 저장된 모든 환율 정보를 반환합니다.

        Returns:
            list[ExchangeRate]: 모든 ExchangeRate 객체 리스트.
        """
        return self.exchange_rates
