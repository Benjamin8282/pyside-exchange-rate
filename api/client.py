import requests
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일에서 환경 변수 로드

class ExchangeRateClient:
    BASE_URL = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"

    def __init__(self, authkey):
        self.authkey = authkey

    def get_exchange_rates(self, searchdate, data="AP01"):
        params = {
            "authkey": self.authkey,
            "searchdate": searchdate,
            "data": data,
        }
        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API 요청 중 오류 발생: {e}")
            return None

