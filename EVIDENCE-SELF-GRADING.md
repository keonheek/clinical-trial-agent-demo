# 근거 자가 채점 문제 (2026-07-22 발견, 팀 논의 필요)

## 무슨 일이 있었나

3개 모델(Haiku 4.5 / Sonnet 5 / Opus 4.8)로 T001-b/c/d를 돌려 정답지와 대조하다가 발견.

T001-d 환자 기록: `"Organ function is reported as adequate by the treating team, with no
specific lab values on file."` (검사 수치 없음, 의료진 진술만 있음)

기준: `"Demonstrates adequate organ function"` (NCT05879653, 포함기준)

Haiku와 Sonnet이 낸 판정과 근거 메타데이터:

```json
{"verdict": "MET",
 "evidence": "Organ function is reported as adequate by the treating team, with no specific lab values on file.",
 "evidence_meta": {"source_type": "clinical_judgment",
                   "confirmation_level": "confirmed",
                   "directness": "direct"},
 "reasoning": "Treating team explicitly documented adequate organ function."}
```

정답지(지우): `expected_verdict: UNCERTAIN`, `uncertainty_type: MISSING`.

## 왜 evidence.py가 못 걸렀나

`assess_evidence()`에 위 메타데이터를 그대로 넣어 확인:

```
{'sufficient': True, 'reason': 'meets required confirmation and directness',
 'suggested_action': None}
```

계층 자체는 규칙대로 동작했다. 문제는 **입력**이다. 같은 모델이 (1) 판정을 내리고
(2) 그 판정의 근거 등급까지 스스로 매긴다. 모델이 자기 근거를 `confirmed` / `direct`로
매기면, 근거 충분성 계층은 그 자가 채점을 신뢰할 수밖에 없다. 즉 **maker와 checker가
같은 호출 안에 있다.**

Opus는 같은 케이스에서 UNCERTAIN을 냈지만 원인을 `INSUFFICIENT_EVIDENCE`로 분류했다
(정답지는 `MISSING`). 이것도 논의거리 — 정보가 "없는" 것인지, "있으나 뒷받침이 안 되는"
것인지의 경계.

## 왜 지금 코드를 안 고쳤나

가장 먼저 떠오르는 수정은 "source_type이 `clinical_judgment`나 `patient_report`면
confirmation을 provisional로 강등"이다. **이건 위험하다.** ECOG 수행능력 점수처럼
임상의 판단이 곧 표준 측정인 기준들이 있다. 일괄 강등하면 정당한 MET 판정까지 무너진다
(07-19에 "무조건 신중 모드"를 넣었다가 ILD 판정이 퇴행한 것과 같은 실패 유형).

정답지에 맞춰 급히 규칙을 넣는 것 자체도 label-fitting에 가깝다. 그래서 수정 대신 기록.

## 논의할 선택지 (팀 결정 필요)

1. **기준별 요구 수준을 선언한다** (백엔드 리뷰 #3과 같은 방향). 지금은 모든 기준에
   `required_confirmation="confirmed"` 고정. "adequate organ function"은 검사 수치를
   요구한다고 기준 쪽에서 선언하면, 의료진 진술만으로는 자동으로 미달이 된다.
   ECOG처럼 임상 판단이 표준인 기준은 요구 수준을 낮게 선언하면 되므로 퇴행이 없다.
2. **근거 채점을 판정과 분리한다.** 판정하는 호출과 근거 등급을 매기는 호출을 나눈다.
   호출 1회가 늘어 비용·지연이 증가하지만, 자가 채점 구조 자체가 사라진다.
3. **원인 분류 경계 정리** — `MISSING`(기록에 없음) vs `INSUFFICIENT_EVIDENCE`(있으나
   결론을 못 뒷받침함). "의료진이 적절하다고 했으나 수치 없음"은 어느 쪽인가. 지우 결정 사항.

## 발표에서의 값어치

이건 숨길 결함이 아니라 정성평가에서 쓸 재료다. "우리 시스템의 근거 검증 계층이 어떤
조건에서 무력화되는지 우리가 직접 찾아냈고, 성급히 규칙을 덧대는 대신 원인을 규정했다"는
서사는 자가 채점 문제를 인지조차 못한 팀과 확실히 구분된다.
