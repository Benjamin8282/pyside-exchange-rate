# -*- coding: utf-8 -*-

# 필요한 모듈들을 임포트합니다.
import requests # HTTP 요청을 보내기 위한 라이브러리
from dotenv import load_dotenv # .env 파일에서 환경 변수를 로드하기 위한 라이브러리

load_dotenv()  # .env 파일에서 환경 변수들을 로드합니다. (예: API 키)


class ExchangeRateClient:
    """
    한국수출입은행 환율 정보 API와 통신하는 클라이언트 클래스입니다.
    API 요청을 보내고 응답을 처리하는 역할을 담당합니다.
    """
    # API의 기본 URL을 정의합니다.
    BASE_URL = "https://oapi.koreaexim.go.kr/site/program/financial/exchangeJSON"

    def __init__(self, authkey: str):
        """
        ExchangeRateClient의 생성자입니다.
        API 인증키를 초기화합니다.

        Args:
            authkey (str): 한국수출입은행 API 인증키.
        """
        self.authkey = authkey # 전달받은 인증키를 인스턴스 변수로 저장

    def get_exchange_rates(self, searchdate: str, data: str = "AP01") -> dict | None:
        """
        특정 날짜의 환율 정보를 API로부터 가져옵니다.

        Args:
            searchdate (str): 조회할 날짜 (YYYYMMDD 형식의 문자열).
            data (str, optional): 요청할 데이터 종류. 기본값은 "AP01" (환율 정보).

        Returns:
            dict | None: API 응답으로 받은 JSON 데이터를 파이썬 딕셔너리 형태로 반환하거나,
                         요청 실패 시 None을 반환합니다.
        """
        # API 요청에 필요한 파라미터들을 딕셔너리 형태로 정의합니다.
        params = {
            "authkey": self.authkey,    # 인증키
            "searchdate": searchdate, # 조회 날짜
            "data": data,             # 데이터 종류
        }
        try:
            # requests.get()을 사용하여 API에 GET 요청을 보냅니다.
            # verify=False는 SSL 인증서 검증을 비활성화합니다. (개발/테스트 환경에서 유용할 수 있으나, 프로덕션에서는 주의 필요)
            response = requests.get(self.BASE_URL, verify=False, params=params)
            # HTTP 응답 상태 코드가 200 (성공)이 아니면 예외를 발생시킵니다.
            response.raise_for_status() 
            # 응답 본문을 JSON 형태로 파싱하여 반환합니다.
            return response.json()
        except requests.exceptions.RequestException as e:
            # API 요청 중 발생한 예외(네트워크 오류, HTTP 오류 등)를 처리합니다.
            print(f"API 요청 중 오류 발생: {e}") # 오류 메시지 출력
            return None # None 반환하여 실패를 알림