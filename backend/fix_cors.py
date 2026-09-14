content = """import os
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

app = FastAPI(title=settings.PROJECT_NAME, redirect_slashes=False)

# Explizite CORS-Erlaubnis für deine VPS-IP und localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://31.97.158.220:5173",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
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

with open("app/main.py", "w") as f:
    f.write(content)
print("✅ CORS ist jetzt wasserdicht konfiguriert!")
