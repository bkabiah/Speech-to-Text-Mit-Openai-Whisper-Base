import asyncio
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
        
        # FIX: return_timestamps=True MUSS ein Top-Level-Argument der Pipeline sein!
        pipe_kwargs = {"return_timestamps": True}
        if language:
            pipe_kwargs["generate_kwargs"] = {"language": language}
        
        try:
            logger.info("Starte Transkription mit Primärem Modell...")
            result = await asyncio.to_thread(
                self.primary_pipe, file_path, **pipe_kwargs
            )
            model_used = settings.PRIMARY_MODEL
        except Exception as e:
            logger.warning(f"Primäres Modell fehlgeschlagen: {e}. Nutze Fallback.")
            result = await asyncio.to_thread(
                self.fallback_pipe, file_path, **pipe_kwargs
            )
            model_used = settings.FALLBACK_MODEL

        processing_time = (time.time() - start_time) * 1000
        
        # Whisper gibt bei return_timestamps=True ein Dict zurück: {"text": "...", "chunks": [...]}
        text = result["text"] if isinstance(result, dict) else str(result)
        lang = result.get("language", language or "unknown") if isinstance(result, dict) else "unknown"
        
        return text, lang, processing_time, model_used

stt_engine = STTEngine()
