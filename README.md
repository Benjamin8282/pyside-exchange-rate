# 환율 정보 뷰어 (PySide6)

## 프로젝트 소개

이 프로젝트는 PySide6 프레임워크를 사용하여 개발된 간단한 데스크톱 애플리케이션으로, 한국수출입은행에서 제공하는 공공 API를 통해 실시간 환율 정보를 조회하고 표시합니다. PySide6 학습 및 포트폴리오 목적으로 개발되었으며, MVC(Model-View-Controller)와 유사한 구조로 설계되어 각 기능의 역할을 명확히 분리하고 유지보수성을 높였습니다.

## 주요 기능

*   **실시간 환율 조회:** 한국수출입은행 API를 통해 다양한 통화의 환율 정보를 가져옵니다.
*   **비영업일/특정 시간 조회 처리:** 비영업일이거나 영업일 오전 11시 이전에 데이터를 요청할 경우, 유효한 데이터를 찾을 때까지 자동으로 이전 영업일의 데이터를 조회하여 안정적인 정보 제공을 보장합니다.
*   **직관적인 UI:** PySide6를 활용하여 사용자 친화적인 인터페이스를 제공합니다.

## 사용 기술

*   **Python 3.11:** 프로젝트의 주 개발 언어.
*   **PySide6:** Qt 프레임워크의 Python 바인딩으로, 데스크톱 GUI 개발에 사용되었습니다.
*   **requests:** HTTP 요청을 처리하여 외부 API와 통신합니다.
*   **python-dotenv:** `.env` 파일에서 환경 변수를 로드하여 API 키와 같은 민감 정보를 안전하게 관리합니다.
*   **한국수출입은행 환율 정보 API:** 실제 환율 데이터를 제공하는 공공 API.

## 프로젝트 구조

```
pyside-exchange-rate/
├── api/
│   └── client.py           # 한국수출입은행 API와 통신하는 클라이언트 로직
├── core/
│   ├── exchange_rate_manager.py # 환율 데이터 조회 및 관리 비즈니스 로직
│   └── exchange_rate_model.py   # 환율 데이터 모델 정의
├── ui/
│   ├── control_panel.py    # 사용자 입력 및 제어 관련 UI (예: 새로고침 버튼)
│   └── data_view.py        # 환율 데이터를 표시하는 UI
├── main.py                 # 애플리케이션의 진입점 및 메인 윈도우
├── requirements.txt        # 프로젝트 의존성 목록
├── .env.example            # 환경 변수 설정 예시 파일
└── README.md               # 프로젝트 설명 (현재 파일)
```

*   **`api/`**: 외부 API와의 통신을 담당합니다. `client.py`는 한국수출입은행 환율 API에 요청을 보내고 응답을 처리합니다.
*   **`core/`**: 애플리케이션의 핵심 비즈니스 로직을 포함합니다. `exchange_rate_manager.py`는 환율 데이터를 관리하고, `exchange_rate_model.py`는 환율 데이터의 구조를 정의합니다.
*   **`ui/`**: 사용자 인터페이스 관련 코드를 포함합니다. `control_panel.py`와 `data_view.py`는 각각 애플리케이션의 특정 UI 부분을 구성합니다.
*   **`main.py`**: 애플리케이션의 시작점이며, 메인 윈도우와 각 컴포넌트를 연결하는 역할을 합니다.

## 설치 및 실행 방법

1.  **저장소 클론:**
    ```bash
    git clone https://github.com/Benjamin8282/pyside-exchange-rate.git
    cd pyside-exchange-rate
    ```

2.  **가상 환경 설정 및 활성화:**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```

3.  **의존성 설치:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **환경 변수 설정:**
    *   한국수출입은행 환율 정보 API에서 [인증키](https://www.koreaexim.go.kr/ir/HPHKIR020M01?apino=2&viewtype=C&searchselect=&searchword=)를 발급받습니다.
    *   프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 발급받은 인증키를 다음과 같이 추가합니다:
        ```
        AUTH_KEY="YOUR_API_KEY_HERE"
        ```
        (`YOUR_API_KEY_HERE` 부분을 실제 인증키로 교체하세요.)

5.  **애플리케이션 실행:**
    ```bash
    python main.py
    ```

## 기여 방법

버그 보고, 기능 제안 등 모든 기여를 환영합니다. Pull Request를 보내기 전에 이슈를 통해 먼저 논의해 주시면 감사하겠습니다.

## 라이선스

이 프로젝트는 MIT 라이선스에 따라 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하십시오.
