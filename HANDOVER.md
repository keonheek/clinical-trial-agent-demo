# 인수인계 안내 — 임상시험 스크리닝 에이전트 (SKKU Healthcare Agentic AI Challenge 2026)

Windows 사용자 기준. 프로그래밍 지식 없이 결과 파일을 여는 방법부터 적습니다. 영문 안내는 아래 English 절.

## 1. 받는 것

| 항목 | 위치 |
|---|---|
| 실행 중인 서비스 | https://sdic-trial-demo.vercel.app |
| 전체 코드 (공개 저장소) | https://github.com/keonheek/clinical-trial-agent-demo — 초록색 **Code ▾ → Download ZIP** |
| 데모 영상 | 별도 전달 (`demo_captions.mp4`) |

## 2. 결과 파일 두 종류 — 무엇이 다른가

| 버튼 (최종 순위 추천 탭) | 파일 | 내용 | 용도 |
|---|---|---|---|
| **스크리닝 기록(xlsx)** | `screening_record_환자ID.xlsx` | 시트 6장: 메타 · 스크리닝 로그 · 적격성 체크리스트 · 질의응답 이력 · 정정 로그 · 근거 원문 | 보관·서명용 문서. **이 파일을 쓰십시오.** |
| CSV 내보내기 | `screening_환자ID.csv` | 기준별 판정 한 표 + 답변 이력 + 판정 변경 | 다른 프로그램에 붙여 넣을 때 |

## 3. 여는 방법 (Windows)

**xlsx** — 파일을 두 번 클릭하면 Excel이 열립니다. 아래쪽 시트 탭(메타, 스크리닝 로그, …)을 눌러 이동합니다. Excel이 없으면 Google 드라이브에 올려 Google 스프레드시트로 여십시오.

**csv** — 파일을 두 번 클릭하면 Excel이 엽니다. 파일에 UTF-8 서명(BOM)이 들어 있어 한글이 그대로 보입니다.
한글이 깨져 보이면(◆◆◆ 또는 물음표): Excel에서 빈 통합문서를 연 뒤 **데이터 → 텍스트/CSV에서** → 파일 선택 → 파일 원본을 **65001: 유니코드(UTF-8)** 로 지정 → 로드.
CSV는 탭이 하나뿐이고 서식이 없습니다. 열 너비는 열 머리글 경계를 두 번 클릭하면 맞춰집니다. 저장할 때는 xlsx로 "다른 이름으로 저장"해야 서식이 남습니다.

**영상처럼 보기(브라우저 화면)** — 선택 사항. Python이 설치된 PC에서:
```
py -m pip install openpyxl
py xlsx_view.py screening_record_S002.xlsx
```
같은 이름의 `.html` 파일이 생기고, 두 번 클릭하면 브라우저에서 시트가 위쪽 탭으로 보입니다.

## 4. 서비스 사용 순서

1. 왼쪽 위 환자 선택(또는 **+ 새 환자**에 기록 붙여 넣기 → 실행).
2. **환자 & 임상시험 보드** — 적격 / 미확정 / 부적격 열로 정렬된 후보 시험. 카드를 누르면 기준별 판정.
3. **확인 질문** — 기록에 없는 항목. 선택지마다 `체크 시 → 적격 방향` / `제외 사유 방향` 표시. 고른 뒤 **선택한 답변 모두 반영**.
4. 반영 결과 — 판정 변화와 시험별 상태(적격 / 미확정 계속 / 탈락).
5. **최종 순위 추천** — 순위와 근거. 여기서 **스크리닝 기록(xlsx)** 내려받기.

## 5. 직접 실행하려면 (개발자용)

- Python 3.12 이상, `pip install openpyxl`.
- Anthropic API 키를 환경 변수 `ANTHROPIC_API_KEY`로 두고 `python serve_local.py` 를 `LLM_BACKEND=anthropic` 으로 실행 → http://127.0.0.1:8930 (Windows PowerShell: `$env:LLM_BACKEND="anthropic"; py serve_local.py`).
- 기본값 `LLM_BACKEND=claude` 는 Claude Code CLI 구독 경로이며 Windows에는 보통 없습니다.
- 파이프라인 재실행·평가·문서 생성은 README의 *How to re-run* 절.

주의: 본 시스템의 모든 환자 기록은 챌린지 제공 합성 시나리오입니다. 의료 판단에 사용할 수 없습니다.

---

# English

**What you receive** — the running service (https://sdic-trial-demo.vercel.app), the full public source (https://github.com/keonheek/clinical-trial-agent-demo → Code ▾ → Download ZIP), and the demo video.

**Two export files** (최종 순위 추천 tab): **스크리닝 기록(xlsx)** is the six-sheet signed screening record — use this one. CSV 내보내기 is a single flat table plus the answer log and verdict changes, for pasting elsewhere.

**Opening on Windows** — double-click the xlsx; sheet tabs are at the bottom. Double-click the CSV; it carries a UTF-8 BOM so Korean renders. If Korean is garbled, open Excel → Data → From Text/CSV → file origin 65001 UTF-8 → Load. A CSV has one tab and no formatting; save as xlsx to keep formatting. Optional browser view like the video: `py -m pip install openpyxl` then `py xlsx_view.py screening_record_S002.xlsx` and open the resulting `.html`.

**Running it yourself** — Python 3.12+, `pip install openpyxl`, set `ANTHROPIC_API_KEY`, run `serve_local.py` with `LLM_BACKEND=anthropic`, open http://127.0.0.1:8930. The default `LLM_BACKEND=claude` needs the Claude Code CLI subscription and is not typical on Windows.

All patient records are challenge-provided synthetic scenarios; not for clinical decisions.
