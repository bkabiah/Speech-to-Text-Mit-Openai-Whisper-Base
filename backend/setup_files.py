import os

files = {
    "app/__init__.py": "",
    "app/core/__init__.py": "",
    "app/models/__init__.py": "",
    "app/plugins/__init__.py": "",
    "app/skills/__init__.py": "",
    
    "app/core/config.py": """from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    PROJECT_NAME: str = "STT AI Platform"
    PRIMARY_MODEL: str = "openai/whisper-base"
    FALLBACK_MODEL: str = "openai/whisper-tiny"
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_PROJECT: str = "stt-ai-junior-portfolio"

settings = Settings()
""",

    "app/models/schemas.py": """from pydantic import BaseModel, Field
from typing import Optional, List

class TranscriptionResponse(BaseModel):
    text: str
    language_detected: str
    processing_time_ms: float
    model_used: str
    plugin_results: Optional[dict] = None
""",

    "app/core/stt_engine.py": """import asyncio
import time
import logging
from transformers import pipeline
from app.core.config import settings

logger = logging.getLogger(__name__)

class STTEngine:
    def __init__(self):
        self.primary_pipe = None
        self.fallback_pipe = None
        self._load_models()

    def _load_models(self):
        logger.info(f"Lade Primäres Modell: {settings.PRIMARY_MODEL}")
        self.primary_pipe = pipeline("automatic-speech-recognition", model=settings.PRIMARY_MODEL, device=-1)
        logger.info(f"Lade Fallback Modell: {settings.FALLBACK_MODEL}")
        self.fallback_pipe = pipeline("automatic-speech-recognition", model=settings.FALLBACK_MODEL, device=-1)

    async def transcribe(self, file_path: str, language: str = None):
        start_time = time.time()
        try:
            logger.info("Starte Transkription mit Primärem Modell...")
            result = await asyncio.to_thread(
                self.primary_pipe, file_path, generate_kwargs={"language": language} if language else {}
            )
            model_used = settings.PRIMARY_MODEL
        except Exception as e:
            logger.warning(f"Primäres Modell fehlgeschlagen: {e}. Nutze Fallback.")
            result = await asyncio.to_thread(
                self.fallback_pipe, file_path, generate_kwargs={"language": language} if language else {}
            )
            model_used = settings.FALLBACK_MODEL

        processing_time = (time.time() - start_time) * 1000
        return result["text"], result.get("language", language or "unknown"), processing_time, model_used

stt_engine = STTEngine()
""",

    "app/skills/summarizer.py": """from langsmith import traceable

@traceable(name="skill_summarize")
async def summarize_text(text: str) -> str:
    sentences = text.split('.')
    return ". ".join(sentences[:3]) + "." if len(sentences) > 3 else text
""",

    "app/skills/translator.py": """from langsmith import traceable

@traceable(name="skill_translate")
async def translate_text(text: str, target_lang: str) -> str:
    return f"[Translated to {target_lang}]: {text[:50]}..."
""",

    "app/plugins/manager.py": """from langsmith import traceable
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
""",

    "app/main.py": """import os
import uuid
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.stt_engine import stt_engine
from app.core.config import settings
from app.models.schemas import TranscriptionResponse
from app.plugins.manager import execute_plugins
from langsmith import traceable

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/transcribe", response_model=TranscriptionResponse)
@traceable(name="fastapi_transcribe_endpoint")
async def transcribe_audio(
    file: UploadFile = File(...),
    language: str = None,
    plugins: str = ""
):
    if not file.content_type.startswith("audio"):
        raise HTTPException(status_code=400, detail="File must be an audio file")

    file_ext = os.path.splitext(file.filename)[1]
    temp_filename = f"temp_{uuid.uuid4()}{file_ext}"
    
    try:
        with open(temp_filename, "wb") as buffer:
            buffer.write(await file.read())

        text, lang_detected, proc_time, model_used = await stt_engine.transcribe(temp_filename, language)
        
        plugin_list = [p.strip() for p in plugins.split(",") if p.strip()]
        plugin_results = await execute_plugins(text, plugin_list) if plugin_list else None

        return TranscriptionResponse(
            text=text,
            language_detected=lang_detected,
            processing_time_ms=proc_time,
            model_used=model_used,
            plugin_results=plugin_results
        )
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": settings.PRIMARY_MODEL}
"""
}

for filepath, content in files.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write(content)
    print(f"✅ Erstellt: {filepath}")

print("\\n🎉 Alle Dateien erfolgreich erstellt!")
