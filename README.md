# PySide6 환율 정보 뷰어

이 프로젝트는 PySide6를 사용하여 OpenAPI에서 환율 정보를 가져와 사용자에게 보여주는 간단한 데스크톱 애플리케이션입니다. PySide6의 기본적인 사용법과 외부 API 연동 방법을 학습하는 것을 목표로 합니다.

## 주요 기능
- 지정된 OpenAPI를 통해 최신 환율 정보 조회
- 조회된 데이터를 테이블 형태로 사용자에게 표시
- 새로고침 기능

## 설치 및 실행

1. **저장소 복제**
   ```bash
   git clone https://github.com/Benjamin8282/pyside-exchange-rate.git
   cd pyside-exchange-rate
   ```

2. **가상환경 생성 및 활성화 (권장)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # venv\Scripts\activate  # Windows
   ```

3. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

4. **애플리케이션 실행**
   ```bash
   python main.py
   ```

## 사용된 라이브러리
- **PySide6**: GUI 프레임워크
- **requests**: HTTP 통신을 위한 라이브러리
