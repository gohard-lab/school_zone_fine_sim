# 🚦 스쿨존 과태료 시뮬레이터 (School Zone Fine Simulator)

본 프로젝트는 어린이 보호구역(School Zone) 내 교통법규 위반 시 발생하는 과태료와 벌점을 시뮬레이션하고, 실시간 접속 통계를 히트맵으로 시각화하는 **Python & Streamlit** 기반 오픈소스 애플리케이션입니다.

[![YouTube Badge](https://img.shields.io/badge/YouTube-잡학다식_개발자-red?style=flat-square&logo=youtube)](https://www.youtube.com/@PolymathDev_KR)
[![GitHub Star](https://img.shields.io/github/stars/gohard-lab/school_zone_fine_sim?style=social)](https://github.com/gohard-lab/school_zone_fine_sim)

---

## ✨ 주요 기능 (Key Features)

* **과태료 시뮬레이션**: 속도 위반(초과 속도별), 주정차 위반 등 상황별 과태료 및 벌점 즉시 확인
* **실시간 접속 히트맵**: 전국 유입 데이터를 Plotly를 활용해 직관적인 열지도로 시각화
* **데이터 트래킹**: Supabase(PostgreSQL) 연동을 통해 각 기능별 사용 패턴 데이터 분석
* **반응형 레이아웃**: 데스크탑과 모바일 환경에 최적화된 Streamlit UI 제공

---

## 🛠️ 기술 스택 (Tech Stack)

* **Language**: Python 3.12+
* **Framework**: Streamlit
* **Visualization**: Plotly (Density Mapbox)
* **Database**: Supabase (PostgreSQL)
* **Package Manager**: **uv** (Next-generation Python bundler)

---

## 🚀 시작하기 (Quick Start)

본 프로젝트는 최신 파이썬 생태계의 표준인 **uv**를 사용하여 의존성을 관리합니다.

### 1. 저장소 클론
```bash
git clone https://github.com/gohard-lab/school_zone_fine_sim.git
cd school_zone_fine_sim
```

### 2. 의존성 설치 및 가상환경 구성
```bash
uv sync
```

### 3. 애플리케이션 실행
```bash
uv run streamlit run src/school_zone_fine_sim.py
```

---

## 🔗 실행 및 다운로드 (Execution)
코드를 직접 실행하기 어려운 분들을 위해 실행 링크를 제공합니다. 제공되는 실행 파일은 엄격한 보안 검토를 거쳤으므로 안심하고 내려받으셔도 됩니다.

* **웹 서비스 실행**: [https://schoolzonefinesim.streamlit.app/](https://schoolzonefinesim.streamlit.app/)

---

## 📢 데이터 수집 안내 (Data Policy)
※ 본 프로그램은 더 나은 서비스 제공과 에러 수정을 위해 익명화된 최소한의 사용 통계(기능 클릭 수 등)를 수집합니다. 개인 식별 정보는 일절 수집하지 않으니 안심하고 실행하셔도 됩니다.

---

## ⭐ 체리피커분들께 드리는 말씀 (Message to Developers)
[KR] 코드가 당신의 공부나 프로젝트에 도움이 되었나요? 누군가의 소중한 시간과 고민이 녹아있는 결과물입니다. 단순히 코드만 가져가는 '체리피커'가 되기보다, 개발자의 최소한의 열정을 응원하는 의미로 Star ⭐ 버튼을 한 번만 클릭해 주세요. 당신의 양심적인 클릭 한 번이 더 나은 오픈소스 문화를 만듭니다.

---

## 👨‍💻 Author
* **YouTube**: [잡학다식 개발자 PolymathDev](https://www.youtube.com/@PolymathDev_KR)
* **GitHub**: @gohard-lab