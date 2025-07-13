# -*- coding: utf-8 -*-

# 필요한 모듈들을 임포트합니다.
import xml.etree.ElementTree as ET # XML 데이터 생성 및 파싱을 위한 모듈
from xml.dom import minidom # XML 문서를 예쁘게 포맷팅하기 위한 모듈
import os # 파일 시스템 경로 확인을 위한 모듈


class SettingsManager:
    """
    애플리케이션 설정을 XML 파일로 저장하고 로드하는 클래스입니다.
    주로 통화 표시 여부와 같은 사용자 정의 설정을 관리합니다.
    """
    def __init__(self, file_path='settings.xml'):
        """
        SettingsManager의 생성자입니다.

        Args:
            file_path (str, optional): 설정을 저장하고 로드할 XML 파일의 경로. 기본값은 'settings.xml'.
        """
        self.file_path = file_path # 설정 파일 경로를 인스턴스 변수로 저장

    def save_settings(self, settings: dict):
        """
        주어진 설정을 XML 파일로 저장합니다.
        각 통화 코드와 해당 통화의 표시 여부(True/False)를 저장합니다.

        Args:
            settings (dict): 통화 코드(str)를 키로, 표시 여부(bool)를 값으로 하는 딕셔너리.
        """
        root = ET.Element('settings') # 최상위 XML 요소 'settings' 생성
        for key, value in settings.items():
            # 각 통화 설정에 대해 'currency' 요소를 생성
            currency_elem = ET.SubElement(root, 'currency')
            # 'id' 속성에 통화 코드(key)를 설정
            currency_elem.set('id', key)
            # 'visible' 속성에 표시 여부(value)를 소문자 문자열로 설정 (True -> "true", False -> "false")
            currency_elem.set('visible', str(value).lower())
        
        # ElementTree 객체를 문자열로 변환하고, minidom을 사용하여 예쁘게 포맷팅합니다.
        xml_str = ET.tostring(root, 'utf-8') # XML 트리를 UTF-8 바이트 문자열로 변환
        pretty_xml_str = minidom.parseString(xml_str).toprettyxml(indent="    ") # 들여쓰기 4칸으로 예쁘게 포맷팅

        # 포맷팅된 XML 문자열을 파일에 씁니다.
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(pretty_xml_str)

    def load_settings(self) -> dict:
        """
        XML 파일로부터 설정을 로드합니다.
        파일이 없거나 파싱 오류가 발생하면 빈 딕셔너리를 반환합니다.

        Returns:
            dict: 로드된 설정 (통화 코드: 표시 여부) 딕셔너리.
        """
        # 설정 파일이 존재하지 않으면 빈 딕셔너리 반환
        if not os.path.exists(self.file_path):
            return {}
        
        try:
            # XML 파일을 파싱하여 ElementTree 객체 생성
            tree = ET.parse(self.file_path)
            root = tree.getroot() # 최상위 요소 'settings' 가져오기
            settings = {} # 설정을 저장할 빈 딕셔너리
            # 모든 'currency' 요소를 찾아 반복
            for currency_elem in root.findall('currency'):
                currency_id = currency_elem.get('id') # 'id' 속성 (통화 코드) 가져오기
                is_visible = currency_elem.get('visible') == 'true' # 'visible' 속성 (표시 여부) 가져와 불리언으로 변환
                if currency_id:
                    settings[currency_id] = is_visible # 딕셔너리에 통화 설정 추가
            return settings # 로드된 설정 반환
        except ET.ParseError:
            # XML 파싱 중 오류가 발생하면 빈 딕셔너리 반환
            print(f"Error parsing settings.xml: {self.file_path}. Returning empty settings.")
            return {}