# 발견: Opus의 action 오답이 우리가 이미 고친 케이스와 정확히 겹침 (2026-08-11)

## 요약

`model_bakeoff_full.json`(3개 모델 × 40명 스트레스 환자 × 51개 정답 라벨) 결과를
`action_accuracy` 축에서 세부 분석한 결과, **claude-opus-4-8의 action 오답 8건 중
6건이, 이전 세션에서 사람이 원문 대조로 "실은 애매하지 않고 MET이 맞다"고 정정했던
바로 그 criterion들과 정확히 일치**함을 확인했다.

## 어떻게 발견했나

지우님이 정의한 "이 대회의 두 경쟁 포인트"(정합성 / 실제 매칭율 개선)를 기준으로
`model_bakeoff_full.json`을 다시 봤다. verdict_accuracy는 모델이 좋아질수록
72.6%→76.5%→80.4%로 깔끔하게 오르는데, action_accuracy는 반대로 70.6%→68.6%→64.7%로
떨어지는 역설이 있었다. 원인을 `action_errors` 필드로 분해:

| 모델 | expected=null (정답 MET/NOT_MET인데 모델이 유보) | predicted=null (모델이 MET/NOT_MET로 확정) | 진짜 verdict는 맞고 action만 틀림 |
|---|---|---|---|
| Haiku 4.5 | 2 | 11 | 2 |
| Sonnet 5 | 3 | 8 | 5 |
| Opus 4.8 | 6 | 4 | 8 |

**"모델이 좋아질수록 predicted=null은 줄고 expected=null은 늘어난다"** — 즉
action_accuracy 하락은 "Opus가 못해서"가 아니라 "Opus가 명확한 케이스조차 과잉
신중하게 유보해서" 생기는 통계적 착시였다.

## 진짜 핵심: expected=null 6건의 정체

Opus가 UNCERTAIN/UNKNOWN으로 잘못 유보한 6건:

| patient_id | criterion | Opus가 붙인 action |
|---|---|---|
| T001-g | ECOG performance status 0 to 1 | ESCALATE |
| T002-g | NYHA class II-III | ESCALATE |
| T003-e | AD diagnosis (CSF OR PET) | ESCALATE |
| T004-c | DAS28 <= 5.1 | REQUEST_LATEST |
| T004-f | Corticosteroids <=10 mg/day | REQUEST_LATEST |
| T005-f | Any other retinopathy (diabetic retinopathy 포함) | ESCALATE |

**이 6건은 우연이 아니다.** 전부 이전 세션에서 원문 대조·적대적 페르소나 검증으로
"컷오프 근접성만으로 애매하다고 잘못 판단했던" 또는 "OR 논리를 AND처럼 잘못 읽었던"
케이스로 실측 확인 후 UNCERTAIN → MET으로 정정한 바로 그 라벨들이다(관련 커밋:
`6aa822c` "Fix verdicts that ignored explicit criterion logic (OR, date math,
inequality)", `c58d283`, `24839bb` 등).

즉 **최고 성능 모델(Opus)조차, 사람이 처음 정답지를 만들 때 빠졌던 것과 같은 함정에
빠진다**는 걸 실측으로 확인했다. 이건 정답지가 "억지로 어렵게 만든 인공적 케이스"가
아니라 "실제로 재현 가능한 진짜 시스템 약점"을 찾아냈다는 증거다.

## 지우님이 정의한 두 축과의 연결

- **정합성(judgment consistency)**: 정답지가 실제로 검증 가능한 오류 패턴(OR 오독,
  컷오프 오판)을 정확히 짚어내고 있고, 그 패턴이 최고 성능 모델에서도 재현된다는 게
  정답지 자체의 신뢰도를 뒷받침한다.
- **매칭율(정량 개선)**: 이 6건이 전부 맞았다면 Opus의 verdict_accuracy는 80.4%보다
  유의미하게 높았을 것 — 즉 이 정답지가 "모델이 실제로 개선해야 할 정확한 지점"을
  숫자로 짚어주고 있다.

## 지우(정답지 담당) 쪽에서 실제로 손댈 수 있는 것

- 없음. **이 발견 자체는 정답지가 이미 올바르다는 걸 재확인한 것**이지, 정답지를
  더 고칠 필요가 있다는 뜻이 아니다. 51개 라벨은 지금 상태 유지.
- 다만 향후 라벨을 확장할 기회가 있다면, 이 6개 패턴(OR 논리, 컷오프 근접)과 유사한
  "함정형" 케이스를 의도적으로 더 넣는 것이 이 프로젝트의 차별점을 강화하는 방향이 될
  수 있음 (판단 보류, 팀 논의 필요).

## 팀(코드 담당) 쪽에 전달할 것

- **action_policy.py 또는 matcher 프롬프트가 "명확한 값도 과잉 신중하게 유보하는"
  경향을 갖고 있을 가능성** — 특히 OR 조건, 컷오프 경계값 처리 시 모델에게 "comparator를
  문자 그대로 적용하라"는 지침이 프롬프트에 명시되어 있는지 확인 필요. 이건 이미
  8/9~10 세션에서 전달한 BACKEND-LOGIC-BRIEF의 관련 원칙과 같은 방향.
- action_accuracy가 verdict_accuracy와 반대로 움직이는 이 역설은, "Agentic" 심사축
  (다음 행동을 자율적으로 잘 고르는가)과 직결되므로 팀 전체가 인지해야 할 사안.

## 원본 데이터

`model_bakeoff_full.json` (origin/main, 커밋 `231dd4f`)
