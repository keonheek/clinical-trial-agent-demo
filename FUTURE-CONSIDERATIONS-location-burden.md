# 위치·이동가능성·참여 부담 — 향후 고려사항 (스코프 판단 포함)

지우님 문의: "위치, 기간, 이동 가능 여부 등 임상시험 참여에 실제로 필요한 요소도 넣어야
하지 않을까?" — 리서치로 근거를 확인한 뒤 스코프를 정리함.

## ⚠️ 6인 패널 검증에서 나온 핵심 발견 (2026-08-09) — 이분법 자체가 흔들림

김도현/박서연/정재훈 각각의 반대파 버전 + 규제담당자/PM/경쟁팀시각, 총 6개 적대적
페르소나로 이 문서를 재검증함. **가장 중요한 지적(반대파 김도현)을 실제로 grep/원문
대조로 검증한 결과, 사실로 확인됨:**

> 실제 프로토콜 exclusion/inclusion criteria에는 "투자자 판단상 연구 요구사항(방문
> 일정 포함) 준수 가능 여부"를 묻는 포괄적 조항이 흔히 존재한다. 이게 있으면
> "의학적으로는 맞는데 접근성 때문에 못 옴"이라는 케이스 구분 자체가 성립하지 않는다
> — 못 오면 그 자체로 exclusion이다.

**실제 확인**: 정답지 5개 trial 원문 중 최소 2개에 이 조항이 존재함:
- **T003 (NCT07214727, 알츠하이머) inclusion #1**: "Is able and willing to meet all
  study requirements in the opinion of the Investigator"
- **T001 (NCT05879653, 방광암) exclusion #30**: "Participation considered
  inappropriate per investigator judgment"

**그런데 51개 정답 라벨을 grep한 결과, 이 조항을 다루는 라벨은 0개.** 즉 "위치/부담은
eligibility와 완전히 별개 축"이라는 이 문서의 핵심 전제는, 최소한 이런 포괄적 조항에
대해서는 성립하지 않습니다 — 이 조항 자체가 이미 프로토콜 eligibility criteria
안에 있고, CLINICAL_JUDGMENT 카테고리(투자자 판단 필요)로 분류돼야 하는데 지금
정답지에 아예 빠져 있습니다.

**처리 방향 (2026-08-09 결정)**: 지금 당장 51개 라벨에 이 조항을 추가하지는 않고,
이 문서에만 기록해둠 — 스코프 판단은 보류 상태. 나중에 이 조항을 라벨화할 때는
verdict는 "환자가 이 요구사항을 준수할 수 있는가"를 판정하는 게 아니라, 원문 자체가
"투자자 판단"을 요구하므로 거의 항상 CLINICAL_JUDGMENT/ESCALATE가 될 가능성이 높음.

### 4명이 수렴한 구조적 지적: "판정 안 함" ≠ "판정 효과 없음"

김도현(exclusion 문구를 놓칠 위험), 박서연(정보 노출이 실은 판정을 CRC에게 몰래
재위임), 정재훈("명시 안 됨" 자체가 이미 암묵적 이진 판정), 규제담당자(정보 배치가
사실상 권고로 기능해 규제상 판정으로 간주될 수 있음) — **네 개의 다른 도메인 언어가
같은 구조적 허점을 가리킴**: "판정 로직을 안 만든다"고 해서 "판정 효과가 없어지는
것"은 아니라는 것. 나중에 이 기능을 실제로 만든다면, "명시 안 됨"과 "파서가 못 찾음"을
구분하는 최소한의 신뢰도 표시(예: `explicitly_stated: true/false/parse_failed`)
없이는 이 프로젝트가 이미 한 번 겪은 verdict/effect 혼동 버그(EVAL-NOTES.md)가
재발할 위험이 있음 — 이건 "나중에 넣는다면" 섹션의 필수 설계 요건으로 못박아 둠.

### PM/경쟁팀 관점의 메타 지적 (수용)

이 스코프 논의 자체에 리서치+페르소나 3~4회전을 쓴 게 대회 타임라인 대비 과했다는
지적은 타당함. **이 문서에 대한 추가 검증 사이클은 여기서 멈추고**, 팀 리소스는
51개 라벨 정확도와 데모로 돌림. "나중에 넣는다면" 섹션은 실제 구현 없이 계획 단계에
머물러 있으며, 지금 프로토타입을 만들 필요는 없음.

### 독립 모델(Llama 3.2 3B, 로컬 Ollama) 교차검증 (2026-08-11)

지금까지의 검증(협조·적대 페르소나 6인 + 종합)이 전부 같은 모델(Claude) 안에서
이뤄진 것이라 자기강화 위험이 남아있다는 지적에 따라, 완전히 다른 학습 데이터를 가진
외부 모델(Meta Llama 3.2 3B, 로컬 실행)에게 별개로 반박시킴.

**1차 반박** (CLINICAL_JUDGMENT 카테고리 도입 없이 이 문서의 분리 원칙만 제시하고
검증 요청): "경계가 항상 명확한 건 아니다(the boundaries between these domains are
not always clear-cut)"라며 더 유연한 프레임워크를 요구 — **이건 새 지적이 아니라
문서가 이미 알고 있던 결론(김도현 반대파 지적, 6-27행)과 독립적으로 수렴한 것**.
완전히 다른 모델이 같은 결론에 도달했다는 건 그 결론이 임의가 아니라 실제로 견고하다는
신호로 해석함.

**2차 반박** (CLINICAL_JUDGMENT 카테고리를 도입한 해법을 제시하고 재반박 요청):
"이 카테고리가 실제로는 catch-all이 되어 진짜 문제(경계의 모호함)를 다른 이름으로
회피(shift)하는 것뿐"이라고 주장. **이건 실제 데이터로 검증해서 기각함** —
`eval_labels_stress.json`의 uncertainty_type 분포를 실측한 결과 CLINICAL_JUDGMENT는
22개 중 1개(5%)로 가장 적게 쓰이는 카테고리였음(MISSING 41%, AMBIGUOUS/STALE/
CONFLICTING 각 14%). Llama의 우려는 실제 코드/데이터를 열어보지 않고 나온 추측이었고,
이번 프로젝트 규모에서는 근거가 없음. 다만 이 우려 자체는 "라벨링 규모가 커질 때
CLINICAL_JUDGMENT가 실제로 catch-all화되는지"를 감시할 지표로는 유효 — 향후 라벨을
늘릴 때 이 카테고리 비율이 급증하면 재검토할 것.

## 정직성 고지 (2026-08-09, 적대적 검증 후 추가)

아래 결론은 (1) 문헌 리서치 (2) 협조적 CRC 페르소나 검토 (3) **반대 입장 적대적
페르소나 검증**, 세 단계를 거쳤습니다. 3단계에서 실제로 **2번 검토의 신뢰성 표현이
과장이었다는 것과, 위치 관련 "낮은 비용" 판단이 이 코드베이스를 실제로 확인 안 하고
내린 미검증 낙관이었다는 것이 드러나 정정했습니다.** 구체적으로:

- **"CRC 페르소나가 실무를 검증했다"는 표현은 부정확했습니다.** 이건 AI가 "8년차
  CRC라면 이렇게 말할 것"이라고 생성한 텍스트이지, 실제 임상 현장의 목소리가 아닙니다.
  이 검토에서 실제로 검증 가능했던 건 단 하나 — **`EVAL-NOTES.md`에 verdict/effect
  혼동 버그가 실제로 기록되어 있다는 사실**뿐입니다(grep으로 직접 확인함). "판정하지
  말되 숨기지도 말라"는 문장 자체는 그럴듯한 **의견**이지 검증된 사실이 아닙니다 —
  다른 CRC라면 다르게 답했을 수 있고, 이 팀이 원했던 답과 정확히 일치하는 지점에서
  멈춘 하나의 샘플일 뿐입니다.
- **"위치는 나중에 낮은 비용으로 추가 가능"이라는 판단은 검증 없이 내려졌습니다.**
  실제로 `fetch_trials.py`를 열어 확인한 결과, **이 코드베이스는 ClinicalTrials.gov
  API를 호출할 때 `eligibilityModule`만 가져오고 `contactsLocationsModule`(위치
  데이터)은 아예 요청하지 않습니다.** "API에 위치 데이터가 존재한다"는 사실과 "이
  프로젝트에 붙이기 쉽다"는 판단은 다른 문제인데, 후자를 검증 없이 전자에서
  끌어냈습니다. 실제 구현에는 지오코딩, 실거리/실이동시간 계산, 사이트별 접근성
  차이, 그리고 "의학적 적합도 vs 접근성" 사이의 순위 가중치 문제까지 필요해
  "낮은 비용"이라 부를 근거가 없었습니다.

이 정정 자체가 검증 방법론에 대한 답이기도 합니다 — 협조적 페르소나 3인(김도현,
박서연, 정재훈) 검토만으로는 이 두 오류를 못 잡았고, **반대 입장에서 반박하도록
지시한 적대적 페르소나가 실제로 오류를 찾아냈습니다.** 다만 적대적 페르소나의
지적 전부가 유효했던 건 아닙니다 — "판정 안 하는 게 책임 회피"라는 지적은 원칙
자체를 무너뜨리지 못했고(구현을 신중히 하라는 경고로만 유효), "스코프 크리프"
지적도 시급성 비교 없이 판단을 보류함. 즉 적대적 검토도 무비판적으로 다 받아들이면
안 되고, 각 반박이 실제로 근거로 무너뜨리는지 하나씩 확인해야 합니다.

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
| **위치/거리** | 개념상 별도 축으로 두는 게 맞지만, 구현 비용은 **미검증 — "낮음"이라 단정할 근거 없음** (아래 정직성 고지 참조) | ClinicalTrials.gov API에 위치 데이터(`contactsLocationsModule`)가 존재하는 건 사실이나, **이 코드베이스(`fetch_trials.py`)는 그 필드를 아예 요청하지 않음** — 지오코딩·거리계산·사이트별 접근성·순위 가중치까지 실제로 필요해 "낮은 비용"은 검증 안 된 낙관이었음. **51개 eligibility 라벨 재작업이 불필요하다는 것만은 여전히 유효** (완전히 별도 파이프라인 단계라는 구조적 판단 자체는 안 흔들림) |
| **방문 빈도/기간(trial burden), 재정 부담, 동반자 필요성** | 판정 로직은 아웃, 정보 노출은 인 — 다만 이 판단의 근거였던 "CRC 실무 검증"은 실제로는 AI가 생성한 의견이지 사실 확인이 아니었음 (아래 참조) | 프로토콜 원문에 이미 명시된 조항(예: "교통비 지원", "동반자 필수 동행")이 있으면 그대로 보여주기만 함 — 판정하지 않음. 없는 정보를 추정/계산하지 않음 |

### CRC 페르소나 검토 (2026-08-09) — "실무 검증"이 아니라 "의견 참고"로 재분류

리서치 결론(업계 아키텍처가 이렇게 분리한다)이 실제 임상 현장 감각과 맞는지 확인하기 위해
CRC 페르소나에게 검토를 받음. **두 가지가 수정됨:**

**1. 방향은 맞지만 "언제 걸러지는지"가 문제.** 실무에서도 의학적 적격성과 접근성은
다른 레이어로 다뤄지지만, 완전히 분리된 시점에 처리되는 게 아니라 **스크리닝 후반부
(동의서 설명·첫 방문 스케줄 단계)까지 뭉쳐서 방치되다 뒤늦게 터지는 경우가 많음**.
"초반에 구조적으로 안 걸러지고, 후반에 사람이 우연히 물어봐야 걸러진다"는 게 실무
비효율의 원인이라는 지적 — 68%라는 수치가 체감상으로도 크다고 확인됨.

**2. 재정/동반자를 "완전히 스코프 아웃"한 판단은 수정.** 인용: *"코디네이터도 이걸
판정 안 합니다, 그냥 정보를 드릴 뿐이에요. '이 시험은 교통비 지원이 있다/없다',
'이 시험은 보호자 필수 동행 조항이 있다'는 팩트를 전달하고, 참여 여부는 환자가
결정합니다. 재정/동반자를 판정 축으로 넣지 말라는 데는 전적으로 동의하는데, 최소한
이 프로토콜에 그런 요구조건이 명시되어 있는지 여부는 순수 정보성 필드로라도 노출해야
한다고 봅니다. **판정하지 말되, 숨기지도 말라**가 제 입장입니다."*

즉 "데이터가 표준 필드로 없으니 스코프 아웃"이라는 원래 판단은 반만 맞았음 — **판정
로직이 필요 없다는 건 맞지만, 원문에 이미 있는 조항을 그대로 노출하는 것(추가
추론/추정 없이)은 다른 문제이고 이건 스코프에 넣어야 함.**

**3. 가장 위험한 설계 실수 (강조됨).** *"eligibility 판정에 접근성을 섞어서
'의학적으로 맞는데 못 옴'을 그냥 INELIGIBLE 한 덩어리로 찍어버리는 것 — 이건 예전에
지적했던 MISSING/ASK 라벨 문제와 완전히 같은 종류의 실수입니다. 접근성 때문에
못 오는 케이스는 ELIGIBLE(의학적)이라는 값과 별도로 'ACCESS_BARRIER' 같은 완전히
다른 축의 플래그로 남아야 합니다. 절대 하나의 최종 라벨로 합치면 안 됩니다."* —
이건 이 프로젝트가 이미 한 번 겪은 verdict/effect 혼동 버그(EVAL-NOTES.md)와 정확히
같은 실패 패턴이므로 특히 주의.

## 만약 나중에 실제로 넣는다면 (수정된 범위)

- **위치/거리**: 추천/순위(recommendation) 로직에 별도 축으로 추가 — eligibility 판정
  로직은 건드리지 않음. 데이터 소스: `contactsLocationsModule.locations[].{city, state,
  country, geoPoint}`. 환자 거주지 ↔ 사이트 최단거리 계산.
- **방문부담/재정/동반자 조항**: **판정 로직 없이, 순수 정보 표시 필드로 추가**.
  프로토콜 원문에 그 조항이 실제로 있을 때만 그대로 노출(있으면 보여주고, 없으면
  "명시 안 됨" — 추정하지 않음). 이건 eligibility criteria 파싱과 비슷한 방식(원문
  발췌)으로 다루되, MET/NOT_MET 같은 판정값은 절대 부여하지 않음.
- **공통 원칙**: eligibility 판정과는 절대 같은 최종 배지/라벨로 합치지 않음 —
  "이 환자에게 의학적으로 맞는 시험"과 "이 환자가 실제로 갈 수 있는 시험"은 서로
  다른 축의 정보로 나란히 보여주되 하나로 뭉개면 안 됨 (TrialGPT의 아키텍처 분리,
  박서연의 "ACCESS_BARRIER는 별도 플래그" 지적 둘 다 같은 방향을 가리킴)
- **스크리닝 타이밍 개선(박서연 지적 반영)**: 위치/부담 정보 노출을 최종 순위 단계가
  아니라 **가급적 초반(환자 프로필 확인 직후)에 함께 보여줘서**, 실무에서 반복되는
  "말기에 가서야 발견"하는 비효율을 시스템이 구조적으로 줄이는 방향 고려

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
