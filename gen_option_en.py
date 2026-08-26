#!/usr/bin/env python3
"""선택지 영문 생성 — 영문 모드에서 선택지가 100% 한국어로 나오는 문제를 없앤다.

`question_options.json`의 선택지는 전부 한국어로 생성돼 있고, 영문 원문이 어디에도 없다
(2026-08-26 확인: gloss.json 역방향 0/176, 서빙 gloss에도 0건). 그래서 UI에서 고칠 수 있는
문제가 아니다 — 번역문을 만들어 사이드카로 두고, 영문 모드일 때 그걸 먼저 보여줘야 한다.

산출물: `question_options_en.json` — {한국어 선택지: 영문} 사전. 원본은 건드리지 않는다.

**비용이 드는 스크립트다.** 챌린지 지원 키(ANTHROPIC_AI_HEALTHCARE_API_KEY)로 실제 호출이
나가므로 그의 승인 없이는 실행하지 않는다. 기본은 --dry-run이고, 실제 실행은 --run 명시가
필요하다.

    python3 gen_option_en.py                 # 규모·비용만 계산, 호출 없음
    python3 gen_option_en.py --run           # 실제 생성 (승인 후)

임상 용어는 원문 뜻을 그대로 옮기고 의역하지 않는다 — 선택지 하나가 곧 기준 판정을 바꾸므로,
번역이 의미를 좁히거나 넓히면 판정이 달라진다.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

SRC = os.path.join(HERE, "question_options.json")
OUT = os.path.join(HERE, "question_options_en.json")
BATCH = 20

PROMPT = (
    "Translate each Korean clinical trial screening answer option into English.\n"
    "Rules:\n"
    "- Preserve clinical meaning exactly. Do not broaden or narrow scope.\n"
    "- Keep parenthetical detail, abbreviations (ERCP, HbA1c, CrCl) and numbers as-is.\n"
    "- Use terminology a clinical research coordinator would write.\n"
    "- No commentary. Return JSON only: an array of strings, same order and length as input.\n\n"
    "Input array:\n{items}"
)


def all_options():
    with open(SRC, encoding="utf-8") as f:
        data = json.load(f)
    seen, out = set(), []
    for opts in data.values():
        for o in opts:
            if o not in seen:
                seen.add(o)
                out.append(o)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", action="store_true", help="실제 API 호출 (승인 필요)")
    args = ap.parse_args()

    opts = all_options()
    chars = sum(len(o) for o in opts)
    batches = (len(opts) + BATCH - 1) // BATCH
    print(f"고유 선택지 {len(opts)}개 · 총 {chars:,}자 · 배치 {batches}회 (배치당 {BATCH}개)")
    print(f"출력 예정: {OUT}")

    if not args.run:
        print("\nDRY RUN — 호출 없음. 실제 생성하려면 --run 을 붙여 실행 (지원 키 과금).")
        return

    from anthropic_client import complete  # noqa: E402  승인된 경우에만 임포트

    result = {}
    for i in range(0, len(opts), BATCH):
        chunk = opts[i:i + BATCH]
        raw = complete(PROMPT.format(items=json.dumps(chunk, ensure_ascii=False, indent=1)))
        text = raw[raw.find("["):raw.rfind("]") + 1]
        en = json.loads(text)
        if len(en) != len(chunk):
            sys.exit(f"배치 {i // BATCH + 1}: 개수 불일치 {len(en)} != {len(chunk)} — 중단")
        result.update(dict(zip(chunk, en)))
        print(f"  배치 {i // BATCH + 1}/{batches} 완료 ({len(result)}/{len(opts)})")

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print(f"작성: {OUT} ({len(result)}개)")


if __name__ == "__main__":
    main()
