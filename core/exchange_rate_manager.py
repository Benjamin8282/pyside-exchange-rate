from api.client import ExchangeRateClient
from core.exchange_rate_model import ExchangeRate
import datetime

class ExchangeRateManager:
    def __init__(self, authkey: str):
        self.client = ExchangeRateClient(authkey)
        self.exchange_rates: list[ExchangeRate] = []

    def fetch_exchange_rates(self, searchdate: str = None) -> list[ExchangeRate]:
        if searchdate is None:
            current_date = datetime.date.today()
        else:
            current_date = datetime.datetime.strptime(searchdate, "%Y%m%d").date()

        max_retries = 7  # 최대 7일까지 이전 날짜를 시도 (주말 포함)
        for _ in range(max_retries):
            search_date_str = current_date.strftime("%Y%m%d")
            raw_rates = self.client.get_exchange_rates(search_date_str)
            
            # API 응답이 유효한 경우 (None이 아니고 빈 리스트가 아닌 경우)
            if raw_rates and not (len(raw_rates) == 1 and raw_rates[0].get('result') == 4): # result 4는 조회 결과 없음을 의미
                self.exchange_rates = []
                for rate_data in raw_rates:
                    result = rate_data.get('result', 1)
                    if result != 1:
                        print(f"API 응답 오류: {rate_data.get('cur_nm', 'Unknown Currency')} - Result Code: {result}")
                        continue
                    try:
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
                        print(f"환율 데이터 파싱 오류: {e} - Data: {rate_data}")
                if self.exchange_rates: # 파싱된 데이터가 있으면 반환
                    return self.exchange_rates
            
            # 데이터가 없거나 오류 응답인 경우, 하루 전으로 날짜 변경
            current_date -= datetime.timedelta(days=1)
            print(f"데이터를 찾을 수 없습니다. 이전 날짜 {current_date.strftime('%Y%m%d')}로 재시도합니다.")

        print("최대 재시도 횟수를 초과했습니다. 환율 정보를 가져오지 못했습니다.")
        return []

    def get_exchange_rate_by_currency(self, currency_code: str) -> ExchangeRate | None:
        for rate in self.exchange_rates:
            if rate.cur_unit == currency_code:
                return rate
        return None

    def get_all_exchange_rates(self) -> list[ExchangeRate]:
        return self.exchange_rates