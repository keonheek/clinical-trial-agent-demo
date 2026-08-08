# 위치·이동가능성·참여 부담 — 향후 고려사항 (스코프 판단 포함)

지우님 문의: "위치, 기간, 이동 가능 여부 등 임상시험 참여에 실제로 필요한 요소도 넣어야
하지 않을까?" — 리서치로 근거를 확인한 뒤 스코프를 정리함.

## 결론 먼저

이건 **eligibility criteria 판정(지금 정답지가 다루는 영역)에 속하지 않습니다.**
세 방향에서 일관되게 확인됨:

1. ClinicalTrials.gov API 자체가 `eligibilityModule`(의학적 자격)과
   `contactsLocationsModule`(사이트 위치)을 처음부터 별개 모듈로 분리해둠
2. TrialGPT 논문(Nature Communications 2024)이 원문에서 지리적 위치(geolocation)를
   명시적으로 스코프 밖이라 밝히고 "traditional structured query"로 별도 처리 가능하다고 서술
3. 실제 서비스(Cancer.gov, TrialFinder 등)도 위치는 eligibility 판정과 별개인
   검색 필터로 제공

즉 "이 환자가 이 시험에 의학적으로 맞는가"(자연어 이해가 필요한 어려운 문제)와
"이 환자가 이 시험에 실제로 갈 수 있는가"(구조화된 필드 간 단순 비교)는 본질이 다른
문제라는 게 업계 표준 아키텍처입니다.

## 실제로 얼마나 큰 장벽인가 (수치로 확인됨)

- 임상시험 미참여 환자의 **68%가 사이트까지 이동이 어려웠다**고 응답
  ([Clinical Leader](https://www.clinicalleader.com/doc/clinical-trials-and-travel-tribulations-overcoming-logistical-and-financial-challenges-for-improved-access-and-outcomes-0001))
- 암 임상시험 참여자의 **47%가 재정적 어려움**(그중 71%가 여행 관련 비용), 이 중
  **51%가 향후 참여 의향이 낮아짐**
  ([Cancer Medicine 2024](https://onlinelibrary.wiley.com/doi/full/10.1002/cam4.7185))
- 종양학은 대형 암센터에 시험이 집중되는 "clinical trial deserts" 문제가 특히 큼
  ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10982574/)) — 정확히 우리 T001(종양학)에
  해당하는 구조적 문제
- 분산형 임상시험(DCT)이 부분적 해법이지만 만능은 아님: 미국 인구 약 20%가 초고속
  인터넷/스마트폰이 없고, 이 비율이 고령층·저소득층·시골 거주자에서 더 높아 "디지털
  격차가 오히려 격차를 심화시킬 위험"이 지적됨
  ([npj Digital Medicine](https://www.nature.com/articles/s41746-022-00603-y))

## 세부 카테고리별 스코프 판단

| 요소 | 판단 | 근거 |
|---|---|---|
| **위치/거리** | 낮은 비용으로 지금 스코프에 편입 가능 | ClinicalTrials.gov가 이미 구조화된 위치 데이터(`contactsLocationsModule`)를 제공 → 기존 eligibility 판정 결과 위에 "거리 필터/정렬"만 후처리로 얹으면 됨. **51개 eligibility 라벨 재작업 불필요** — 완전히 별도 파이프라인 단계 |
| **방문 빈도/기간(trial burden)** | 스코프 아웃 권장 | ClinicalTrials.gov가 이를 구조화된 필드로 안 주고 프로토콜 원문에만 자연어로 존재. 별도 추출/정규화 작업 필요 |
| **재정 부담/동반자 필요성** | 스코프 아웃 권장 | 애초에 trial 데이터 자체에 이 정보가 거의 없음(비용 보전 여부, 동반자 필요 여부가 표준 필드가 아님) — 시스템이 다룰 "데이터"가 부재 |

방문 부담·재정·동반자를 아웃하는 이유를 더 명확히 하면:
- "적절한 부담 수준"은 환자마다 주관적 판단(소득, 직업 유연성, 보호자 가용성)이 커서
  40명 페르소나만으로 일반화된 판정 로직을 검증하기 어려움
- 51개 라벨 스킴(MET/NOT_MET/UNCERTAIN/UNKNOWN)과 근본적으로 다른 데이터 축이라
  별도의 라벨링·검증 설계가 필요해 현재 리서치 규모를 벗어남

## 만약 나중에 위치 필터를 실제로 넣는다면

- **추천/순위(recommendation) 로직에 별도 축으로 추가** — eligibility 판정 로직은 건드리지 않음
- 데이터 소스: ClinicalTrials.gov API의 `contactsLocationsModule.locations[].{city, state, country, geoPoint}`
- 계산: 환자 거주지(위경도) ↔ 각 trial 사이트 목록 간 최단 거리
- 표시: eligibility 판정과는 별개 배지/필터로 — "이 환자에게 의학적으로 맞는 시험"과
  "이 환자가 실제로 갈 수 있는 시험"을 같은 뱃지에 섞지 않는 게 중요 (TrialGPT 등이
  이 둘을 아키텍처 레벨에서 분리한 이유와 동일)

## 참고 문헌 전체

- [ASCO Educational Book — barriers to trial participation](https://ascopubs.org/doi/10.1200/EDBK-25-100052)
- [Barriers to Clinical Trial Participation: Rural vs Urban](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9073606/)
- [Clinical Leader — travel tribulations](https://www.clinicalleader.com/doc/clinical-trials-and-travel-tribulations-overcoming-logistical-and-financial-challenges-for-improved-access-and-outcomes-0001)
- [Cancer Medicine 2024 — financial cost of trial participation](https://onlinelibrary.wiley.com/doi/full/10.1002/cam4.7185)
- [Assessing Patient Participation Burden, 2019](https://journals.sagepub.com/doi/10.1177/2168479019867284)
- [Mayo Clinic — DCT expands access](https://newsnetwork.mayoclinic.org/discussion/study-finds-bringing-clinical-trials-closer-to-patients-expands-access-to-research/)
- [npj Digital Medicine — DCT digital divide risk](https://www.nature.com/articles/s41746-022-00603-y)
- [TrialGPT, Nature Communications 2024](https://www.nature.com/articles/s41467-024-53081-z) / [PMC 전문](https://pmc.ncbi.nlm.nih.gov/articles/PMC11574183/)
- [Geographic disparity in cancer clinical trials, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10982574/)
- [Improving Rural Clinical Trial Enrollment, JCO](https://ascopubs.org/doi/10.1200/JCO.23.01667)
- [Geographic accessibility, clinical trial deserts, JCO](https://ascopubs.org/doi/10.1200/JCO.2026.44.16_suppl.1540)
- [Cancer.gov 검색 필터 예시](https://www.cancer.gov/clinicaltrials/search-form-help/page3)
