import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

class SettingsManager:
    def __init__(self, file_path='settings.xml'):
        self.file_path = file_path

    def save_settings(self, settings: dict):
        root = ET.Element('settings')
        for key, value in settings.items():
            currency_elem = ET.SubElement(root, 'currency')
            currency_elem.set('id', key)
            currency_elem.set('visible', str(value).lower())
        
        # 예쁘게 포맷팅된 XML 생성
        xml_str = ET.tostring(root, 'utf-8')
        pretty_xml_str = minidom.parseString(xml_str).toprettyxml(indent="    ")

        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(pretty_xml_str)

    def load_settings(self) -> dict:
        if not os.path.exists(self.file_path):
            return {}
        
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
            settings = {}
            for currency_elem in root.findall('currency'):
                currency_id = currency_elem.get('id')
                is_visible = currency_elem.get('visible') == 'true'
                if currency_id:
                    settings[currency_id] = is_visible
            return settings
        except ET.ParseError:
            return {}
