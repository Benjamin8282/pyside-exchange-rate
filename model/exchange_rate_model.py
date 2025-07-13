# -*- coding: utf-8 -*-

# dataclasses 모듈을 임포트합니다. 데이터 클래스를 쉽게 생성할 수 있도록 돕습니다.
from dataclasses import dataclass


@dataclass
class ExchangeRate:
    """
    환율 정보를 담는 데이터 클래스입니다.
    한국수출입은행 API 응답의 각 필드에 대응하는 속성들을 정의합니다.
    """
    result: int          # 결과 코드 (1: 성공, 4: 조회 결과 없음 등)
    cur_unit: str        # 통화 코드 (예: USD, JPY)
    ttb: str             # 전신환(송금) 받으실 때 (매입률)
    tts: str             # 전신환(송금) 보내실 때 (매도율)
    deal_bas_r: str      # 매매 기준율
    bkpr: str            # 장부가격
    yy_efee_r: str       # 년환가료율
    ten_dd_efee_r: str   # 10일환가료율
    kftc_bkpr: str       # 서울외국환중개 장부가격
    kftc_deal_bas_r: str # 서울외국환중개 매매기준율
    cur_nm: str          # 통화명 (예: 미국 달러, 일본 옌)