from langsmith import traceable

@traceable(name="skill_translate")
async def translate_text(text: str, target_lang: str) -> str:
    return f"[Translated to {target_lang}]: {text[:50]}..."
