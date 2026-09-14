from langsmith import traceable
from app.skills.summarizer import summarize_text
from app.skills.translator import translate_text

@traceable(name="plugin_executor")
async def execute_plugins(text: str, plugins: list):
    results = {}
    if "summarize" in plugins:
        results["summary"] = await summarize_text(text)
    if "translate" in plugins:
        results["translation"] = await translate_text(text, target_lang="en")
    return results
