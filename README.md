# SSD Clean Commit: SSD 검증용 테스트 셸

![Python](https://img.shields.io/badge/python-%3E=3.11-blue)
---
본 프로젝트는 SSD(Solid State Drive)의 내부 동작(Read, Write, Erase)을 시뮬레이션하는 파이썬 기반 테스트 셸 애플리케이션입니다.<br>
본 프로젝트는 단순한 기능 구현을 넘어, **클린 코드 원칙**과 **철저한 코드 리뷰 문화**를 바탕으로 협업하며 소프트웨어의 품질을 점진적으로 개선해나가는 과정을 담고 있습니다. 성능보다는 코드의 안정성, 가독성, 유지보수성에 초점을 맞추어 개발되었습니다.

---

## 👨‍💻 우리 팀, CleanCommit: 역할 및 책임

| 역할 | 이름 | GitHub                                                                                                           | 주요 역할                                                 |
| :--- | :--- |:----------|:--------|
| **팀장** | 정송화 | [@jungsh83](https://github.com/jungsh83)                                                                         | 프로젝트 통합, 시나리오 및 Command Buffer 개발, <br>리팩토링, 리뷰       |
| **팀원** | 나송주 | [@rmsidgo1](https://github.com/rmsidgo1)                                                                         | Shell 및 Logger 개발, 통합테스트 준비, <br>리팩토링, 리뷰             |
| **팀원** | 설서은 | [@seoeun46](https://github.com/seoeun46)                                                                         | SSD 및 SSD Commands 개발, 리팩토링, 리뷰                       |
| **팀원** | 권구남 | [@Nueve-Code](https://github.com/Nueve-Code)<br>commit-id: jihun75.kim<br>commit-email: gnswlrla0218@naver.com   | Shell 및 SSD Commands 개발, 리팩토링, 리뷰                     |
| **팀원** | 우성경 | [@SKWOO-CRA-EDU](https://github.com/SKWOO-CRA-EDU)                                                               | SSD 개발, SSD Commands 개발, 리팩토링, 리뷰                     |
| **팀원** | 지우성 | [@jws9106](https://github.com/jws9106)                                                                           | 시나리오 개발, SSD Driver 개발, <br>SSD Commands 개발, 리팩토링, 리뷰 |

---

## 📝 우리의 개발 철학과 프로세스

이 프로젝트는 결과물만큼 과정의 학습을 중요하게 생각합니다. 우리는 아래의 원칙들을 나침반 삼아 개발을 진행했습니다.

### 1. 테스트 주도 개발 (TDD) in Action
*   **Red-Green-Refactor**: 우리는 기능 구현에 앞서 항상 실패하는 테스트(`Red`)를 먼저 작성했습니다. 이후 테스트를 통과하는 최소한의 코드(`Green`)를 구현하고, 마지막으로 코드의 구조를 개선(`Refactor`)하는 사이클을 철저히 따랐습니다. `tests/` 디렉토리의 모든 코드는 이러한 노력의 증거입니다.
*   **자신감 있는 개발**: 잘 작성된 테스트 코드는 새로운 기능 추가나 리팩토링 시 발생할 수 있는 잠재적 오류를 빠르게 감지해주는 든든한 안전망이 되어주었습니다.

### 2. 클린 코드와 지속적인 리팩토링
*   **가독성은 곧 유지보수성**: 우리는 변수명 하나, 함수 하나를 만들 때도 '이 코드를 처음 보는 동료가 쉽게 이해할 수 있는가?'를 기준으로 삼았습니다.
*   **응집도 높이고, 결합도 낮추기**: 사용자 입력을 받는 `shell.py`, 명령어 로직을 처리하는 `command_*.py`, 파일 I/O를 담당하는 `ssd_driver.py`로 역할을 명확히 나누어 코드의 복잡도를 낮추고 유지보수성을 높였습니다.
*   **점진적 개선**: 처음부터 완벽한 코드는 없다는 것을 인정하고, 코드 리뷰와 페어 프로그래밍을 통해 꾸준히 더 나은 구조로 코드를 개선해나갔습니다.
*   **객체 지향** : 이 프로젝트는 코드의 유지보수성과 확장성을 확보하기 위해 객체 지향 설계의 5가지 기본 원칙인 SOLID를 따르고자 노력했습니다.

### 3. 동시 개발을 가능하게 한 Mocking
*   **의존성 분리**: 프로젝트 초기, 우리는 shell - shell_commands - ssd_driver - ssd - ssd_commands - command_buffer / ssd_file_manager 각 모듈의 의존성을 분리했습니다. 이는 `pytest-mock` 라이브러리를 통해 가능했습니다.
*   **효율적인 협업**: 예를 들어, Shell 개발자는 아직 완성되지 않은 SSD Driver의 동작을 `mocker`로 가상(mock)하여 자신의 로직을 독립적으로 개발하고 테스트할 수 있었습니다. 이는 팀원 모두가 서로를 기다릴 필요 없이 동시에 작업을 진행할 수 있는 핵심 전략이었습니다.

### 4. 애자일 스크럼 기반의 반복적 개발
저희는 총 5회의 스크럼(Scrum) 스프린트를 통해 프로젝트를 점진적으로 완성했습니다. 이 과정은 예측 가능성을 높이고 지속적인 품질 검증을 가능하게 했습니다.

*   **1차 스크럼:** 각자 맡은 모듈(Shell, Commands, Driver)의 핵심 기능을 TDD 사이클에 맞춰 독립적으로 개발했습니다.
*   **2차 스크럼:** **최초 소스 코드 통합(Integration)** 을 진행했습니다. 각자 개발한 모듈을 처음으로 결합하고, **1차 통합 테스트**를 수행하여 이질적인 부분들이 서로 잘 맞물려 동작하는지 검증했습니다. 이 단계를 통해 통합 과정에서 발생하는 문제를 조기에 발견하고 해결할 수 있었습니다.
*   **3차 스크럼:** **1~2일차 요구사항**에 대한 모든 기능 개발을 완료하고, 최종 안정성을 확보하기 위해 **2차 통합 테스트**를 수행했습니다. 이를 통해 제품의 완성도를 최종적으로 점검하고 배포 가능한 수준의 품질을 확보했습니다.
*   **4차 스크럼:** **3~5일차 요구사항**에 대한 개발 소스 통합(Integration)을 수행했습니다. 이를 통해 남은 개발 요구사항을 도출하였고, 프로젝트 전체 디렉토리 구조를 재정리하였습니다.
*   **5차 스크럼:** **전체 요구사항**에 대한 재점검 및 통합 테스트 수행하고, 통합에 의해 발현된 버그를 수정했습니다.

---

## 📚 강의내용과 프로젝트의 연결

### 1. TDD(테스트 주도 개발)
- **`[TDD]_1_3_TDD개요`**
  - TDD의 기본 원리(Red-Green-Refactor), 테스트 코드의 작성과 실행
- **`[TDD]_2_2_PrimeFactors`**
- **`[TDD]_2_3_BaseBall`**
- **`[TDD]_2_4_유사도검사`**
  - 다양한 실습 예제를 통해 TDD 사이클을 반복
- **`[TDD]_3_1_TestDouble`**
  - Mocking을 활용한 의존성 분리, 동시 개발 지원
- **`[TDD]_3_3_DeviceDriver`**
  - Device Driver(SSD 드라이버) 개발에 TDD 적용

**프로젝트 적용:**  
실패하는 테스트를 먼저 작성(Red), 테스트 통과(Green), 코드 개선(Refactor)의 TDD 사이클을 철저히 따랐으며, pytest를 활용해 단위 및 통합 테스트를 자동화했습니다. Mocking(pytest-mock)을 통해 모든 모듈이 독립적으로 개발 및 테스트될 수 있도록 했습니다.

### 2. 리팩토링
- **`[리팩토링]_1_2_리팩토링_개요`**
  - 리팩토링의 목적과 필요성
- **`[리팩토링]_2_3_SOLID_민코딩`**
  - SOLID 원칙 적용
- **`[리팩토링]_3_1_리팩토링기법과코드스멜`**
  - 리팩토링 기법과 코드 스멜 제거

**프로젝트 적용:**  
코드 리뷰와 페어 프로그래밍을 통해 지속적으로 코드를 개선하며, 응집도 높이고 결합도 낮추는 구조로 모듈화했습니다. 변수명, 함수명, 코드 구조를 가독성과 유지보수성을 기준으로 꾸준히 리팩토링했습니다.

### 3. 클린 코드
- **`[클린코드]_1_1/3/5_클린코드`**
  - 클린 코드의 원칙과 실천 방법

**프로젝트 적용:**  
가독성, 단순성, 유지보수성을 최우선으로 하며, 코드 리뷰를 통해 집단 지성을 활용해 잠재적 결함을 최소화했습니다. 모든 변경 사항은 팀원의 리뷰를 거쳐 병합했습니다.

### 4. Git/GitHub & PyCharm
- **`[TDD]_1_1_코드리뷰어를_위한_Git`**
- **`[TDD]_2_1_Git_with_PyCharm`**
  - Git, GitHub, PyCharm을 활용한 협업 및 코드 관리

**프로젝트 적용:**  
Git을 통해 버전을 관리하고, GitHub을 통해 코드 리뷰, 이슈 관리, 협업을 진행했습니다. PyCharm을 주 개발 환경으로 사용해 효율적인 개발과 디버깅을 지원했습니다.

---

## 📐 디자인 패턴 적용

이 프로젝트는 유지보수성과 확장성을 높이기 위해 여러 디자인 패턴을 적극적으로 활용했습니다. 각 모듈에 적용된 핵심 디자인 패턴은 다음과 같습니다.

| 모듈 (Module) | 적용된 디자인 패턴 (Applied Design Pattern) | 설명 (Description) |
|---|---|---|
| `shell.py`, `src/shell_commands/` | **팩토리 메서드 (Factory Method)** & **커맨드 (Command)** | **[팩토리 메서드]** `shell.py`는 커맨드 생성을 위한 **인터페이스(Factory)**를 정의하고, 실제 어떤 커맨드 객체를 생성할지는 **서브클래스(구체적인 Factory)**에 위임합니다. 예를 들어, 기본 명령어와 테스트 스크립트는 서로 다른 팩토리에서 생성됩니다. 이를 통해 새로운 유형의 명령어(예: 네트워크 명령어) 그룹이 추가되더라도 기존 팩토리 코드를 수정하지 않고 새로운 팩토리를 추가하여 확장할 수 있습니다(OCP 원칙). **[커맨드]** 생성된 각 커맨드 객체는 `execute()` 메서드를 통해 요청을 캡슐화하고 실행합니다. |
| `ssd.py`, `src/ssd_commands/` | **팩토리 (Simple Factory)** & **커맨드 (Command)** | **[팩토리]** `ssd.py`는 SSD 하드웨어 제어를 위한 **중앙 집중적인 하나의 팩토리** 역할을 합니다. 이 팩토리는 내부 로직(예: `if/elif` 분기)을 통해 요청에 맞는 `ssd_command` 객체(Read, Write 등)를 직접 선택하고 생성하여 반환합니다. 팩토리 메서드 패턴과 달리, 객체 생성을 서브클래스에 위임하지 않고 팩토리 클래스가 직접 처리합니다. **[커맨드]** 생성된 커맨드는 SSD에 전달될 구체적인 요청을 캡슐화합니다. |
| `src/logger.py` | **싱글톤 (Singleton)** | 애플리케이션 전역에서 단 하나의 로거(Logger) 인스턴스만 생성하여 로그 출력 채널을 일관되게 관리합니다. 이를 통해 어떤 모듈에서든 동일한 설정과 파일 핸들러를 공유하며 로그를 기록할 수 있습니다. |
| `src/ssd_driver.py` | **퍼사드 (Facade)** | 복잡한 내부 파일 I/O 로직(nand.txt, result.txt 관리)을 `read()`, `write()`, `erase()`와 같은 단순하고 일관된 인터페이스로 감싸 제공합니다. 클라이언트(커맨드 객체)는 복잡한 내부 동작을 알 필요 없이 **퍼사드**가 제공하는 간결한 API만을 사용하여 SSD를 제어할 수 있습니다. |
| `src/command_buffer/command_buffer_optimizer.py` | **스트래티지 (Strategy)** | 커맨드 버퍼에 쌓인 명령어들을 최적화하는 다양한 알고리즘(예: 연속된 쓰기 명령 병합)을 **전략(Strategy)**으로 정의합니다. 각 최적화 로직을 별도의 전략 객체로 캡슐화하여, 향후 새로운 최적화 알고리즘을 추가하거나 변경할 때 기존 코드에 미치는 영향을 최소화합니다. |

---

## ✨ 주요 기능

- **인터랙티브 셸 환경**: 사용자가 직접 명령어를 입력하며 SSD 동작을 테스트할 수 있습니다.
- **기본 SSD 명령어**: write, read 등 SSD의 핵심 기능을 지원합니다.
- **고급 유틸리티 명령어**: fullwrite, fullread로 전체 LBA 영역을 손쉽게 관리합니다.
- **새로운 고급 명령어**: erase, erase_range, flush 등 추가 SSD 관리 기능을 제공합니다.
- **자동화된 테스트 시나리오**: 복잡한 테스트 케이스를 단일 명령어로 실행하여 검증을 자동화합니다.
- **견고한 유효성 검사**: 잘못된 명령어와 인자를 사전에 차단하여 런타임 에러를 방지합니다.
- **Command Buffer 시스템**: 명령어 최적화 및 버퍼링 기능을 제공합니다.

## 📂 프로젝트 구조

```
ssd_clean_commit/
├── .github/                      # GitHub 관련 파일
│   └── PULL_REQUEST_TEMPLATE.md  # PR Template
├── src/                          # 메인 소스 코드
│   ├── __init__.py              # shell_commands 모듈 임포트
│   ├── ssd_driver.py            # SSD 드라이버 (ssd 제어 담당)
│   ├── data_dict.py             # 공용 상수 모음
│   ├── decorators.py            # 로그 데코레이터
│   ├── logger.py                # 통합 로거
│   ├── ssd_file_manager.py      # SSD 파일 관리자
│   ├── shell_commands/          # 셸 명령어 구현
│   │   ├── __init__.py
│   │   ├── shell_command.py     # shell command 인터페이스
│   │   ├── data_dict.py         # 공용 상수 모음
│   │   ├── action/              # 기본 명령어들
│   │   │   ├── __init__.py
│   │   │   ├── write.py         # Write 명령어
│   │   │   ├── read.py          # Read 명령어
│   │   │   ├── full_write.py    # Full Write 명령어
│   │   │   ├── full_read.py     # Full Read 명령어
│   │   │   ├── erase.py         # Erase 명령어
│   │   │   ├── erase_range.py   # Erase Range 명령어
│   │   │   ├── flush.py         # Flush 명령어
│   │   │   ├── help.py          # Help 명령어
│   │   │   └── exit.py          # Exit 명령어
│   │   └── script/              # 테스트 시나리오들
│   │       ├── __init__.py
│   │       ├── full_write_and_read_compare.py      # 1번 시나리오
│   │       ├── partial_lba_write.py                # 2번 시나리오
│   │       ├── write_read_aging.py                 # 3번 시나리오
│   │       └── erase_and_write_aging.py            # 4번 시나리오 (추가)
│   ├── ssd_commands/            # SSD 명령어 구현
│   │   ├── __init__.py
│   │   ├── ssd_command.py       # ssd command 인터페이스
│   │   ├── data_dict.py         # 공용 상수 모음
│   │   ├── ssd_read.py          # SSD Read 명령어
│   │   └── ...
│   └── command_buffer/          # 명령어 버퍼 시스템
│       ├── __init__.py
│   │   ├── data_dict.py         # 공용 상수 모음
│       ├── command_buffer_data.py                  # 커맨드 버퍼 데이터 클래스
│       ├── command_buffer_file_manager.py          # 커맨드 버퍼 파일 관리자
│       ├── command_buffer_handler.py               # 커맨드 버퍼 핸들러
│       └── command_buffer_optimizer.py             # 커맨드 버퍼 최적화 로직(strategy 패턴)
├── tests/                       # 단위 테스트 및 통합 테스트 코드
│   ├── __init__.py
│   ├── test_*.py               # 각종 테스트 파일들
│   └── skip_test_integration.py # 통합 테스트
├── .gitignore                   # Git 무시 파일 설정
├── README.md                    # 프로젝트 문서
├── pytest.ini                  # pytest 설정 파일
├── requirements.txt             # 의존성 패키지
├── shell.py                     # 셸 실행 파일 (최상위)
└── ssd.py                      # SSD 실행 파일 (최상위)
```

## 🚀 시작하기

### 사전 요구 사항

*   Python 3.11 이상

### 의존성 패키지

```
pytest
pytest-cov
pytest-mock
radon
```

### 설치

1.  **프로젝트 클론**
    ```bash
    git clone https://github.com/jungsh83/ssd_clean_commit.git
    ```

2.  **프로젝트 디렉토리로 이동**
    ```bash
    cd ssd_clean_commit
    ```

### SSD 실행
프로젝트의 최상위 루트 디렉토리에서 아래 명령어를 실행하여 ssd를 실행합니다.
> **Note:** `-m` 옵션은 파이썬이 프로젝트 구조를 올바르게 인식하여 모듈을 임포트하게 해주는 가장 안정적인 실행 방법입니다.

| 명령어       | 형식                              | 설명                                                |
|:----------|:--------------------------------|:--------------------------------------------------|
| **Write** | `python -m ssd W <LBA> <Value>` | 지정된 LBA에 특정 데이터(VALUE)를 씁니다.                      |
| **Read**  | `python -m ssd R <LBA>`         | 지정된 LBA의 데이터를 읽어 `ssd_output.txt`에 기록합니다.         |
| **Erase** | `python -m ssd E <LBA> <SIZE>`  | LBA 부터 Size만큼의 내용을 삭제합니다.                         |
| **Flush** | `python -m ssd F`               | Command Buffer 에 있는 모든 명령어들을 수행하여 Buffer 전체 비웁니다. |



### **테스트 셸 실행**
프로젝트의 최상위 루트 디렉토리에서 아래 명령어를 실행하여 셸을 시작합니다.
```bash
python -m shell
```
> **Note:** `-m` 옵션은 파이썬이 프로젝트 구조를 올바르게 인식하여 모듈을 임포트하게 해주는 가장 안정적인 실행 방법입니다.


## 💻 Shell 명령어 가이드

셸이 실행되면 `Shell>` 프롬프트가 나타납니다. 여기에 아래 명령어를 입력하여 사용합니다. (대소문자 구분 없음)

### 기본 명령어

| 명령어 | 형식                                 | 설명 |
| :--- |:-----------------------------------| :--- |
| **write** | `write <LBA> <VALUE>`              | 지정된 LBA에 특정 데이터(VALUE)를 씁니다. |
| **read** | `read <LBA>`                       | 지정된 LBA의 데이터를 읽어 `ssd_output.txt`에 기록합니다. |
| **help** | `help`                             | 사용 가능한 모든 명령어와 사용법, 제작자 정보를 출력합니다. |
| **exit** | `exit`                             | 테스트 셸을 종료합니다. |

**인자(Argument) 규칙**
*   `<LBA>`: `0`부터 `99` 사이의 10진수 정수
*   `<VALUE>`: `0x`로 시작하는 10자리 16진수 문자열 (예: `0x1234ABCD`)

### 유틸리티 명령어

| 명령어 | 형식                  | 설명 |
| :--- |:--------------------| :--- |
| **fullwrite** | `fullwrite <VALUE>` | `0`번부터 `99`번까지 모든 LBA를 지정된 VALUE로 채웁니다. |
| **fullread** | `fullread`          | `0`번부터 `99`번까지 모든 LBA의 데이터를 순차적으로 읽습니다. |

**인자(Argument) 규칙**
*   `<VALUE>`: `0x`로 시작하는 10자리 16진수 문자열 (예: `0x1234ABCD`)

### 고급 SSD 관리 명령어

| 명령어      | 형식                                  | 설명 |
|-------------|-------------------------------------|----- |
| erase       | `erase <LBA> <SIZE>`                | 지정된 LBA부터 SIZE만큼의 영역을 삭제합니다. |
| erase_range | `erase_range <Start LBA> <End LBA>` | 시작 LBA부터 끝 LBA까지의 범위를 삭제합니다. |
| flush       | `flush`                             | 버퍼에 있는 모든 데이터를 디스크에 강제로 쓰기합니다. |

**인자(Argument) 규칙**
*   `<LBA>`: `0`부터 `99` 사이의 10진수 정수
*   `<SIZE>`: `-2,147,483,648` - `2,147,483,647` 사이의 int형 정수
*   `<Start LBA>`: `0`부터 `99` 사이의 10진수 정수
*   `<End LBA>`: `0`부터 `99` 사이의 10진수 정수

### ⛔ 에러 처리

유효하지 않은 명령어, LBA 범위 초과, 잘못된 값 형식 등 모든 오류 발생 시 `Invalid command` 메시지가 출력되며, 셸은 종료되지 않고 다음 명령을 대기합니다.

## 🧪 테스트 시나리오

미리 정의된 복잡한 테스트 시나리오를 간편하게 실행할 수 있습니다.

| 명령어                                 | 설명 |
|-------------------------------------|------|
| `1_` 또는 `1_FullWriteAndReadCompare` | 5개 LBA 단위로 쓰기와 읽기/비교를 반복하며 전체 영역을 검증합니다. |
| `2_` 또는 `2_PartialLBAWrite`         | 무작위 순서로 특정 LBA에 쓰고, 모든 데이터가 정상적으로 저장되었는지 30회 반복하여 검증합니다. |
| `3_` 또는 `3_WriteReadAging`          | 맨 앞과 맨 뒤 LBA에 랜덤 값을 쓰고 읽는 동작을 200회 반복하여 데이터 안정성을 테스트합니다. |
| `4_` 또는 `4_EraseAndWriteAging`      | 삭제 후 쓰기 동작을 반복하여 데이터 안정성을 테스트합니다. |

*시나리오 실행 중 오류가 발생하면 즉시 `FAIL`을 출력하고 중단됩니다. 모든 과정이 정상이면 `PASS`를 출력합니다.*

### runner 실행(일괄 실행)
사전 지정된 테스트 스크립트 파일(예제> shell_script.txt)에 따라 테스트 스크립트를 바로 실행합니다.
```txt
shell_script.txt
1_
2_
3_
4_
```
```bash
python -m shell shell_scripts.txt
```
> **Note:** `-m` 옵션은 파이썬이 프로젝트 구조를 올바르게 인식하여 모듈을 임포트하게 해주는 가장 안정적인 실행 방법입니다.

---

## 🔧 테스트 실행

프로젝트는 pytest를 사용하여 자동화된 테스트를 지원합니다.

```bash
# 모든 테스트 실행
pytest
```
