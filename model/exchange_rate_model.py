from dataclasses import dataclass

@dataclass
class ExchangeRate:
    result: int
    cur_unit: str
    ttb: str
    tts: str
    deal_bas_r: str
    bkpr: str
    yy_efee_r: str
    ten_dd_efee_r: str
    kftc_bkpr: str
    kftc_deal_bas_r: str
    cur_nm: str
