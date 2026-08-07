# Criterion 종속관계 노드 뷰 — 설계안

**목적 재정의**: 이건 발표용 장식이 아니라 **실무 감사(audit) 도구**입니다. 코디네이터가
"왜 이 환자가 이 시험에서 이 상태가 됐는지"를 3초 안에 추적할 수 있어야 합니다.

---

## 왜 필요한가 (3가지 실무 근거)

1. **일 처리 속도**: 코디네이터는 매일 여러 환자·criterion을 본다. 텍스트 rationale을
   매번 읽을 시간이 없다. 노드 그래프는 한눈에 스캔 가능한 상태 기록이어야 한다.
2. **감사 가능성(auditability)**: 판정이 틀렸을 때 "왜 틀렸는지" 역추적이 가능해야 한다.
   텍스트 설명은 LLM이 사후에 지어낸 것일 수 있다는 의심에서 못 벗어나지만, 노드-엣지는
   실제 로직 실행 경로 그 자체다.
3. **연구팀 협업**: 코디네이터가 PI에게 "이 환자 이 시험 UNCERTAIN인데 확인해주세요"라고
   가져갈 때, PI가 근거를 몇 초 안에 파악해야 한다.

**설계 원칙**: 예쁜 애니메이션보다 정확하고 추적 가능한 상태 기록이 우선.

---

## 기존 코드에서 이미 있는 재료 (새 백엔드 로직 불필요)

`live_server.py`의 `handle_answer()`가 이미 다음을 계산해서 갖고 있음:

```python
verdict_changes = [
    {"nct_id": ..., "criterion": ..., "before": "UNCERTAIN", "after": "MET"},
    ...
]
```

`find_affected()`가 질문 답변 시 어떤 criterion이 재평가 대상인지도 이미 계산함.

**즉 노드 그래프는 새 계산을 요구하지 않고, 이미 존재하는 `verdict_changes` /
`find_affected` 결과를 그대로 시각화하면 됨.**

---

## 주의: 기존 취약점이 그래프에 그대로 노출됨

`find_affected()`는 현재 stable ID가 아니라 텍스트 매칭(`field` 이름, token overlap)으로
영향받는 criterion을 찾음 (어제 전달한 BACKEND-LOGIC-BRIEF의 P0-5 항목). 이 상태로 노드
그래프를 만들면:

- 워딩이 조금만 달라도 엣지가 잘못 그려질 수 있음
- "질문 하나가 무관한 criterion까지 흔든다"는 문제가 오히려 **시각적으로 더 잘 드러남**
  (이건 나쁜 게 아니라, 그래프가 이 버그를 찾는 데 유용한 도구가 된다는 뜻)

**권장**: 그래프를 만들기 전에, 최소한 `criterion_id`(stable ID) 도입을 먼저 하거나,
그래프 자체를 "이 취약점을 검증하는 디버그 도구"로 먼저 쓰고 나중에 프로덕션 UI로 승격.

### 실제로 재현/디버깅한 결과 (2026-07-20)

`find_affected()` (`live_server.py:191-222`)를 직접 재현해봤다. 핵심 로직:

```python
target_texts = set()
if field and field in gaps_by_field:
    target_texts.update(gaps_by_field[field].get("related_criteria", []))
if not target_texts:
    # fallback: token overlap
    ...
for t_idx, t in enumerate(trials_out):
    for c_idx, c in enumerate(t["criteria"]):
        ...
        if target_texts and c["text"] not in target_texts:
            continue   # <- 여기가 문제
        affected.append(...)
```

**두 가지를 실제로 시뮬레이션해서 증명함:**

1. **exact-match 실패 재현**: gap-detector(LLM)가 `related_criteria`에 넣는 텍스트가
   실제 `criterion.text`와 한 글자만 달라도(`"DAS28 <= 5.1"` vs `"DAS28 <=5.1"` 공백 하나)
   `c["text"] not in target_texts`가 실패해 매칭이 깨짐. LLM은 자유 생성 텍스트이므로
   이런 미세한 워딩 차이는 실제 운영에서 충분히 발생 가능.

2. **더 치명적인 발견 — fallback까지 실패하면 "전체 재평가"로 확대됨**: token overlap
   fallback도 실패해서 `target_texts`가 빈 셋(`set()`)으로 남으면,
   `if target_texts and c["text"] not in target_texts:` 조건에서 `target_texts`
   (빈 셋 = falsy)가 앞부분에서 이미 False가 되어 **`continue`가 아예 실행되지 않는다.**
   즉 매칭 실패 시 "아무것도 재평가 안 함"이 아니라 **"모든 UNKNOWN/UNCERTAIN criterion을
   재평가 대상으로 삼는다"**로 뒤집힘.

   실제 재현 결과 (T004 자가면역 시험, 3개 unresolved criterion 상황):
   ```
   질문: "가장 최근 DAS28 값은 언제 측정하셨나요?"
   기대: DAS28 criterion 1개만 재평가
   실제(매칭 실패 시): DAS28 + 잠복결핵 + 감염이력, 3개 전부 재평가 대상
   ```

   이건 어제 전달한 BACKEND-LOGIC-BRIEF의 P0-5("target ID가 없으면 전체 fallback을
   하지 않는다: `if not target_criterion_ids: return []`")가 실제로 지켜지지 않고
   있다는 걸 코드 실행으로 확인한 것. 이 버그가 있는 채로 노드 그래프를 만들면, 질문
   하나에 답했을 때 무관한 criterion들이 우르르 흔들리는 게 그래프에 그대로 보임 —
   이게 이 프로젝트 발표의 핵심 주장("결과를 바꾸지 않는 criterion은 재평가하지 않는다")과
   정면으로 배치되는 장면이 시연 중에 나올 수 있다는 뜻.

**결론**: 노드 그래프 작업에 들어가기 전에 `find_affected()`의 fallback 분기에
`if not target_texts: return []` 한 줄을 먼저 넣는 게 우선순위가 더 높음. 이건 그래프
UI보다 훨씬 작은 수정이고, 이 버그를 안 고치면 그래프가 오히려 시스템의 약점을
실시간으로 폭로하는 역효과를 낼 수 있음.

---

## 노드/엣지 구조안

### 노드 타입 (4종)

```
[QUESTION]   질문 카드 — question_id, 질문 텍스트, 대상(환자/의료진/기록)
[CRITERION]  criterion 상태 — criterion_id, verdict(전/후), effect(PASS/FAIL/REVIEW)
[TRIAL]      시험 전체 상태 — nct_id, eligibility(전/후)
[RANK]       추천 순위 — 순위(전/후)
```

### 엣지 (상태 전이 방향)

```
[QUESTION] --답변--> [CRITERION: verdict 변경]
[CRITERION] --effect 재계산--> [TRIAL: eligibility 변경]
[TRIAL] --재정렬--> [RANK: 순위 변경]
```

### 예시 (실제 데이터 기반: T004-b, DAS28 STALE 케이스)

```
[Q: "마지막 DAS28 측정은 언제였나요?"]
        │ 답변: "2주 전, 4.3"
        ▼
[C: DAS28 <= 5.1 | before=UNCERTAIN(STALE) → after=MET]
        │ effect: REVIEW → PASS
        ▼
[T: NCT06906549 | before=UNCERTAIN → after=ELIGIBLE]
        │
        ▼
[R: 순위 3위 → 1위]
```

각 노드는 클릭하면 다음을 보여줌 (감사 목적):
- CRITERION 노드: criterion_text 원문, evidence(근거 문장), reasoning
- QUESTION 노드: 질문이 생성된 이유(uncertainty_type), 대상(patient_answerable 여부)
- TRIAL 노드: 이 판정에 영향을 준 모든 criterion 목록 (FAIL 원인 추적)

---

## 최소 구현 범위 (MVP)

1. 질문에 답변한 **직후** 그 라운드에 대해서만 그래프 렌더링 (전체 세션 히스토리 그래프는 P1)
2. `verdict_changes`가 있는 것만 노드로 그림 (변화 없는 criterion은 그래프에 안 나타남 —
   "무관한 건 안 흔들렸다"를 시각적으로 증명하는 것 자체가 핵심 가치)
3. 노드 색상은 기존 CSS 변수 재사용 (`--met`, `--not-met`, `--uncertain`, `--unknown` 이미 정의됨,
   `.badge-MET`/`.badge-NOT_MET`/`.badge-UNCERTAIN`/`.badge-UNKNOWN` 클래스가 이미 있음 — 새로 안 만듦)

---

## 라이브러리 선택 (2차 리서치로 결론 수정됨)

**1차 리서치에서는 "React Flow"를 권장했으나, 이 프로젝트가 React가 아니라 순수
vanilla JS(`live.html`)라는 걸 반영 안 한 결론이었음. 재조사 후 정정.**

| 옵션 | 판정 | 이유 |
|---|---|---|
| React Flow (CDN으로 얹기) | ❌ 기각 | xyflow 저장소에 실제로 보고된 버그(`jsx-runtime` UMD 빌드 부재로 런타임 에러) 있음. React 전체(130KB+) + ReactFlow를 노드 3~8개짜리에 얹는 건 명백한 과잉 |
| Mermaid.js | ❌ 기각 | 자동 레이아웃 엔진이 강제되어 "4단 고정 컬럼" 요구와 구조적으로 안 맞음. 색상이 SVG 내부에 갇혀 기존 `.badge-*` CSS 재사용 불가 |
| leader-line.js | ❌ 기각 | 기능은 동작하지만 유지보수 중단(방치) 프로젝트, 원저자도 후속 프로젝트로 이전 권고 |
| **순수 SVG 오버레이 + 기존 카드 재사용** | ✅ 채택 | 추가 의존성 거의 0, 기존 CSS/배지 그대로 사용, 좌표 계산은 `getBoundingClientRect()`(표준 API)만으로 충분 |

**최종 선택: 커스텀 카드(기존 HTML/CSS 재사용) + CSS Grid 4단 컬럼 배치 + SVG 오버레이로 화살표만 그리기.**

---

## 실제 구현 코드 (바로 붙여넣기 가능, `live.html`에 추가할 것)

### 1. HTML 구조 — 4단 컬럼 + SVG 오버레이

```html
<div id="dagView" style="position:relative;">
  <svg id="dagEdges" style="position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;">
    <defs>
      <marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
        <path d="M0,0 L8,4 L0,8 Z" fill="var(--ink-soft)"/>
      </marker>
    </defs>
  </svg>
  <div id="dagGrid" style="display:grid;grid-template-columns:repeat(4,1fr);gap:24px;position:relative;z-index:1;">
    <div class="dag-col" data-col="question"></div>
    <div class="dag-col" data-col="criterion"></div>
    <div class="dag-col" data-col="trial"></div>
    <div class="dag-col" data-col="rank"></div>
  </div>
</div>
```

### 2. 노드 렌더링 — 기존 `.badge-*` 클래스 그대로 재사용

**별도 에이전트 코드 리뷰로 실데이터 기반 버그 2건을 확정 발견해 아래 코드에 이미 반영함**
(자세한 내용은 이 섹션 끝의 "코드 리뷰에서 발견된 문제" 참조):
- `escapeHtml` 없이 `innerHTML`에 criterion 텍스트를 직접 넣으면, 실제 데이터에 있는
  `"eGFR < 90 mL/min/1.73m^2"` 같은 텍스트가 HTML로 오인 파싱되어 **카드가 깨짐** (100% 재현 확인).
  `live.html`은 이미 전역적으로 `escapeHtml()`을 거쳐서만 `innerHTML`에 텍스트를 넣는 관례가
  있으므로, 그 관례를 그대로 따름(DOM API로 완전히 우회하는 방식 채택).
- verdict 값도 방어적으로 화이트리스트 검증(현재는 백엔드가 4개 enum만 보내지만, 프론트도
  방어선을 갖는 게 안전).

```javascript
const VALID_BADGE_VALUES = new Set(["MET","NOT_MET","UNCERTAIN","UNKNOWN","ELIGIBLE","INELIGIBLE","PASS","FAIL","REVIEW"]);

function renderDagRound(question, verdictChanges, trialChange, rankChange) {
  const grid = document.getElementById("dagGrid");
  grid.querySelectorAll(".dag-col").forEach(col => col.innerHTML = "");
  document.querySelectorAll("#dagEdges path.dag-edge").forEach(p => p.remove()); // 화살표도 즉시 제거(깜빡임 방지)

  const qCol = grid.querySelector('[data-col="question"]');
  qCol.appendChild(makeDagCard("q-0", question.text, null));

  const cCol = grid.querySelector('[data-col="criterion"]');
  verdictChanges.forEach((v, i) => {
    const label = `${v.criterion}\n${v.before} → ${v.after}`;
    const node = makeDagCard(`c-${i}`, label, v.after);
    node.addEventListener("click", () => showCriterionDetail(v)); // 클릭 시 원문/근거 표시
    cCol.appendChild(node);
  });

  const tCol = grid.querySelector('[data-col="trial"]');
  if (trialChange) {
    tCol.appendChild(makeDagCard("t-0", `${trialChange.nct_id}\n${trialChange.before} → ${trialChange.after}`, trialChange.after));
  }

  const rCol = grid.querySelector('[data-col="rank"]');
  if (rankChange) {
    rCol.appendChild(makeDagCard("r-0", `${rankChange.before}위 → ${rankChange.after}위`, null));
  }

  // getBoundingClientRect() 자체가 호출 시점에 pending layout을 강제로 flush하므로
  // rAF는 "다음 페인트까지 미룬다"는 의미일 뿐 -- 필수 요건은 아니지만 DOM 변경 배치 처리를
  // 피하기 위해 유지.
  requestAnimationFrame(() => drawDagEdges(verdictChanges, trialChange, rankChange));
}

// innerHTML/이스케이핑 없이 DOM API로만 구성 -- criterion_text에 "<", ">" 등이 있어도 안전
// (live.html의 escapeHtml() 관례를 텍스트 노드 생성으로 대체)
function makeDagCard(id, text, verdict) {
  const div = document.createElement("div");
  div.id = id;
  div.className = "dag-card";

  const textDiv = document.createElement("div");
  textDiv.className = "dag-card-text";
  text.split("\n").forEach((line, i) => {
    if (i > 0) textDiv.appendChild(document.createElement("br"));
    textDiv.appendChild(document.createTextNode(line));
  });
  div.appendChild(textDiv);

  const safeVerdict = VALID_BADGE_VALUES.has(verdict) ? verdict : null;
  if (safeVerdict) {
    const span = document.createElement("span");
    span.className = "badge badge-" + safeVerdict;
    span.textContent = safeVerdict;
    div.appendChild(span);
  }
  return div;
}
```

### 3. 화살표 그리기 — `getBoundingClientRect()` + SVG path (표준 API만 사용, 외부 의존성 없음)

**코드 리뷰에서 발견된 추가 수정**: SVG presentation attribute(`stroke`, `fill`)에
`var(--ink-soft)`를 문자열로 직접 넣으면 브라우저마다 지원이 갈림 (Firefox/Safari는
일부 지원하나 **Chrome은 SVG2 스펙상 이 방식의 `var()` 치환을 지원하지 않는 케이스가
있음** — 실제로 화살표가 안 보이는 상태로 배포될 위험). 색상은 attribute가 아니라
CSS 클래스로 옮김. 그리고 여러 criterion이 하나의 trial로 수렴할 때 화살표 종점이
전부 같은 좌표에 겹쳐 구분이 안 되는 문제(다대일 fan-in)도 종점 y좌표를 살짝 분산시켜 해결.

```javascript
function drawDagEdges(verdictChanges, trialChange, rankChange) {
  const svg = document.getElementById("dagEdges");
  const container = document.getElementById("dagView").getBoundingClientRect();

  // 여러 엣지가 같은 target으로 모일 때 종점을 세로로 분산(fan-in) -- 안 그러면 겹쳐서 구분 불가
  function connect(fromEl, toEl, fanIndex = 0, fanTotal = 1) {
    if (!fromEl || !toEl) return;
    const a = fromEl.getBoundingClientRect();
    const b = toEl.getBoundingClientRect();
    const x1 = a.right - container.left, y1 = a.top + a.height / 2 - container.top;
    const spread = 10; // px, 엣지 사이 최소 간격
    const offset = fanTotal > 1 ? (fanIndex - (fanTotal - 1) / 2) * spread : 0;
    const x2 = b.left - container.left, y2 = (b.top + b.height / 2 - container.top) + offset;
    const midX = (x1 + x2) / 2;
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("class", "dag-edge"); // stroke 색상은 CSS .dag-edge 규칙에서 처리 (var() 안전)
    path.setAttribute("d", `M${x1},${y1} C${midX},${y1} ${midX},${y2} ${x2},${y2}`);
    path.setAttribute("fill", "none");
    path.setAttribute("marker-end", "url(#arrow)");
    svg.appendChild(path);
  }

  const qNode = document.getElementById("q-0");
  verdictChanges.forEach((v, i) => connect(qNode, document.getElementById(`c-${i}`)));
  if (trialChange) {
    verdictChanges.forEach((v, i) =>
      connect(document.getElementById(`c-${i}`), document.getElementById("t-0"), i, verdictChanges.length)
    );
  }
  if (rankChange) connect(document.getElementById("t-0"), document.getElementById("r-0"));
}
```

### 4. 최소 CSS 추가 (기존 `--line`, `--bg-alt`, `--ink-soft` 변수 재사용)

```css
.dag-card{
  background:var(--bg-alt);border:1px solid var(--line);border-radius:8px;
  padding:10px 12px;margin-bottom:12px;font-size:0.85rem;cursor:pointer;
}
.dag-card:hover{border-color:var(--accent);}
.dag-card-text{margin-bottom:6px;}

/* SVG stroke/fill 색상은 반드시 CSS에서 지정 (attribute로 var() 넣으면 Chrome에서 깨짐) */
.dag-edge{ stroke:var(--ink-soft); stroke-width:1.5px; }
#dagEdges marker path{ fill:var(--ink-soft); }
```

```html
<!-- marker 정의도 fill을 attribute가 아니라 CSS class로 -->
<marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
  <path d="M0,0 L8,4 L0,8 Z"/>
</marker>
```

이 코드는 **새 의존성이 0개**입니다 (perfect-arrows 같은 좌표계산 라이브러리조차 안 씀 —
노드가 4단 컬럼에 세로로만 쌓이는 단순한 구조라 직접 계산이 더 간단함). 정원님이 이 스니펫을
`live.html`에 그대로 붙이고, `verdictChanges`/`trialChange`/`rankChange`를 실제
`handle_answer()` 응답 형태에 맞게만 연결하면 됨.

---

### 코드 리뷰에서 발견된 문제 (별도 에이전트로 교차 검증, 2026-07-20)

`live.html`의 실제 관례(전역적으로 `escapeHtml()` 사용)와 실제 정답지 데이터
(`"eGFR < 90 mL/min/1.73m^2"`, `"DAS28 <= 5.1"` 등)를 대조해서 검증한 결과:

| # | 문제 | 심각도 | 확정 여부 |
|---|---|---|---|
| 1 | `innerHTML`에 criterion 텍스트 직접 삽입 → 실데이터(`eGFR < 90`)로 HTML 파손 | 높음 | **실데이터로 재현 확정**, 위 코드에 수정 반영 |
| 2 | SVG attribute에 `var()` 색상 → Chrome 등에서 화살표 안 보일 위험 | 높음 | 브라우저 스펙 차이로 확정, 위 코드에 수정 반영 |
| 3 | 다대일 수렴 시 화살표 종점이 겹쳐 구분 불가 (감사 도구 목적 훼손) | 중간 | 기하학적으로 필연, 위 코드에 fan-in 수정 반영 |
| 4 | badge 클래스명 자체는 백엔드 enum 검증(`VALID_VERDICTS`)에 의존해 현재는 안전하나 프론트 방어 없음 | 중간 | 위 코드에 화이트리스트 방어 추가 반영 |
| 5 | `requestAnimationFrame`이 레이아웃 완료를 보장하는지 | 낮음 | **문제 없음** — `getBoundingClientRect()` 자체가 호출 시 강제 리플로우하므로 rAF 유무와 무관하게 안전 |
| 6 | `innerHTML=""` 재호출 시 이벤트 리스너 누적 | - | **문제 없음** — DOM 표준 동작상 노드 파괴 시 리스너도 함께 제거됨 |

위 표의 1~4번은 이미 코드 스니펫에 반영 완료. 정원님은 이 문서의 코드를 그대로 가져다 쓰면 됨.

## 하지 말 것 (스코프 아님)

- 전체 파이프라인 아키텍처 다이어그램(이건 후보 A, 별도 정적 자료로 충분)
- 실시간 애니메이션/드래그 인터랙션
- 여러 환자를 한 그래프에 겹쳐 보여주는 것
- React/Mermaid/외부 그래프 라이브러리 도입 (위 리서치로 전부 기각)

---

## 추가 구현 1: 한 번에 하나씩만 보기 (가독성 문제 해결)

첫 실제 데이터(S002, verdict_changes 19건)로 렌더링해보니 4단 컬럼에 19줄이 세로로
쌓이고 화살표 19개가 겹쳐 그려져 가독성이 심하게 떨어짐 — 문서 앞부분의 "MVP 범위"에
개수 제한을 명시했어야 했는데 실제 구현에서 빠뜨렸던 부분.

**해결**: 19개를 한 화면에 다 그리는 대신, **드롭다운으로 판정 변화 하나를 선택하면
그 하나의 사슬(질문 1개 → criterion 1개 → trial 1개 → rank 0~1개)만 가로로 넓게
펼쳐서 보여줌.** 드롭다운을 바꾸면 그래프가 즉시 갱신됨. `index.html`의
`renderDag()`/`dagSelectedIndex`에 구현 완료. 컬럼도 `1fr` 균등 분할이 아니라
`minmax(220px, 1fr)`로 바꿔서 criterion 원문이 좁은 칸에 눌리지 않게 함.

## 추가 구현 2: Human-in-the-loop override (완료, 저장 범위는 미정 — 판단 필요)

사용자가 "잘못된 판정을 사람이 바꿀 수 있어야 하지 않냐"고 지적. 확인해보니
**`live.html`에 이미 이 기능이 있었다가(커밋 `d95ed00`, "AI 판정 사람 override")
이후 리팩터링 과정에서 코드가 사라진 상태**였음(커밋 로그에는 남아있지만 최신
`live.html`/`index.html` 어디에도 `humanOverrides`/`override-toggle` 등이 없음 —
grep으로 확인). 원 커밋의 로직(`humanOverrides` 딕셔너리 + `effectOf()` 재계산 +
MET/NOT_MET/UNCERTAIN/UNKNOWN 4버튼)을 그대로 가져와 DAG criterion 카드에 재구현함.

**구현 완료된 것** (`index.html`):
- `dagHumanOverrides` — `patient_id::nct_id::criterion` 키로 override verdict 저장
- `dagEffectOf()` — `pipeline.py`의 EFFECT_TABLE과 동일한 inclusion/exclusion×MET/NOT_MET
  → PASS/FAIL 매핑을 재구현 (분리된 표라 로직 불일치 위험 있음, 아래 참조)
- criterion 카드에 "AI 1차 판단" / "판정 수정" 토글 → 4버튼 패널 → "✓ 사람 확정" 배지
- override 시 trial 카드에 "사람 정정 반영 시 이 criterion effect: X (전체 시험
  재계산은 아님)" 문구로, 이게 `decide_eligibility()`를 다시 돈 결과가 아님을 명시

**미해결 — 저장 범위 결정 필요**: 지금 override는 **브라우저 메모리에만 있어 새로고침하면
사라짐**. 사용자가 "다른 사람도 볼 수 있게 traces.js/서버 데이터까지 영구 반영"을 원했는데,
이건 `index.html`(정적 페이지, GitHub Pages로 서빙)의 구조상 **브라우저가 자동으로
서버 파일을 못 고치므로 완전 자동화가 불가능**함. 실현 가능한 선택지 두 가지:

1. **다운로드 → 수동 반영**: "수정내역 다운로드" 버튼을 만들어 override 목록을
   JSON(`{patient_id, nct_id, criterion, before, after, overridden_at}[]`)으로
   다운로드하게 하고, 이 파일을 팀에 전달해 `traces.js`/정답지에 수동 반영 후 커밋.
   자동화는 아니지만 "다른 사람도 볼 수 있게" 요구를 실제로 만족시키는 유일한 경로.
2. **localStorage 영구 저장**: 새로고침해도 유지되지만 그 브라우저/PC에만 남음 —
   "다른 사람도 볼 수 있게"는 만족 못 함. 개인 작업용으로만 의미 있음.
3. **`live_server.py`와 연동**: 실시간 서버가 떠 있는 상태에서만 실제 세션에 반영
   가능 — 이건 `live.html`이 원래 하던 방식이고, 정적 `index.html`에는 적용 불가.

이 셋 중 뭘 구현할지는 정원님(live.html/데이터 흐름 담당) 판단이 필요함 — 특히
"이 override가 실제 정답지(`eval_labels_stress.json`)를 고치는 근거로 쓰이는 건지,
아니면 그냥 코디네이터의 개인 메모인지"에 따라 요구되는 신뢰 수준과 감사 로그
(누가 언제 왜 바꿨는지)가 달라짐 — 이건 기획 판단이라 지우님 확인도 필요.

**로직 중복 위험 짚어둠**: `dagEffectOf()`가 `pipeline.py`의 `EFFECT_TABLE`을
프론트엔드 JS로 재구현한 것이라, 나중에 백엔드 쪽 EFFECT_TABLE이 바뀌면 이 프론트
사본도 같이 고쳐야 함(지금 이미 `index.html`에 같은 종류의 중복이 있었을 가능성 있음 —
`getEffect()`/`badgeClass()` 확인 필요). 이상적으로는 하나의 소스에서 파생돼야 하지만
정적 페이지라 서버 호출 없이는 어려움 — 이것도 P1로 남겨둠.
