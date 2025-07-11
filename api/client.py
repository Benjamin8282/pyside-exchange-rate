import requests

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


if __name__ == "__main__":
    AUTH_KEY = "qxf4jMteliYvRPID4ELzuARpeFIJUuha"  # 발급받은 인증키
    client = ExchangeRateClient(AUTH_KEY)

    # 오늘 날짜로 테스트 (예: 2025-07-11)
    import datetime
    today = datetime.date.today().strftime("%Y%m%d")

    print(f"오늘 날짜 ({today}) 환율 정보 요청...")
    rates = client.get_exchange_rates(searchdate=today)

    if rates:
        print("API 응답:")
        import json
        print(json.dumps(rates, indent=4, ensure_ascii=False))
    else:
        print("환율 정보를 가져오지 못했습니다.")
