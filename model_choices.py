"""Models offerable per backend for the local UI picker (live_server.py and serve_local.py
both serve GET/POST /api/meta from this table). Shared here so the two local servers cannot drift."""

# Models offerable per backend, for the local UI's picker. IDs are the exact strings the
# provider expects -- Anthropic aliases carry no date suffix. Local only: the deployed
# endpoint stays pinned to its configured model so a visitor can't select a costlier one.
MODEL_CHOICES = {
    "anthropic": [
        {"id": "claude-opus-5", "label": "Opus 5 (기본)"},
        {"id": "claude-fable-5", "label": "Fable 5 (최상위, 가장 비쌈)"},
        {"id": "claude-sonnet-5", "label": "Sonnet 5 (균형)"},
        {"id": "claude-haiku-4-5", "label": "Haiku 4.5 (가장 저렴)"},
    ],
    "claude": [
        {"id": "claude-opus-5", "label": "Opus 5 (기본)"},
        {"id": "claude-fable-5", "label": "Fable 5 (최상위, 가장 느림)"},
        {"id": "claude-sonnet-5", "label": "Sonnet 5 (균형)"},
        {"id": "claude-haiku-4-5", "label": "Haiku 4.5 (가장 빠름)"},
    ],
# Fable 5 is offered on Keonhee's call (2026-08-30). Caveat: its safety classifiers screen
# clinical/bio content and can return stop_reason=refusal on some prompts -- the call then
# raises and the criterion stays UNKNOWN. If that bites during a demo, switch to Opus 5.
    "groq": [
        {"id": "llama-3.3-70b-versatile", "label": "Llama 3.3 70B (무료)"},
    ],
    "ollama": [
        {"id": "qwen3.6:35b", "label": "Qwen3.6 35B (로컬)"},
    ],
}
