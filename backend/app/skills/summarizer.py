from langsmith import traceable

@traceable(name="skill_summarize")
async def summarize_text(text: str) -> str:
    sentences = text.split('.')
    return ". ".join(sentences[:3]) + "." if len(sentences) > 3 else text
