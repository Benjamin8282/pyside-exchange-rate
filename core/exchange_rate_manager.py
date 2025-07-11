from api.client import ExchangeRateClient
from core.exchange_rate_model import ExchangeRate
import datetime

class ExchangeRateManager:
    def __init__(self, authkey: str):
        self.client = ExchangeRateClient(authkey)
        self.exchange_rates: list[ExchangeRate] = []

    def fetch_exchange_rates(self, searchdate: str = None) -> list[ExchangeRate]:
        if searchdate is None:
            searchdate = datetime.date.today().strftime("%Y%m%d")

        raw_rates = self.client.get_exchange_rates(searchdate)
        self.exchange_rates = []

        if raw_rates:
            for rate_data in raw_rates:
                # API 응답에서 'result' 필드가 없는 경우 기본값 1 (성공)으로 처리
                result = rate_data.get('result', 1)
                # 'result'가 1이 아닌 경우 (오류) 해당 데이터는 파싱하지 않음
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
        return self.exchange_rates

    def get_exchange_rate_by_currency(self, currency_code: str) -> ExchangeRate | None:
        for rate in self.exchange_rates:
            if rate.cur_unit == currency_code:
                return rate
        return None

    def get_all_exchange_rates(self) -> list[ExchangeRate]:
        return self.exchange_rates