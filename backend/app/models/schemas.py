from pydantic import BaseModel, Field
from typing import Optional, List

class TranscriptionResponse(BaseModel):
    text: str
    language_detected: str
    processing_time_ms: float
    model_used: str
    plugin_results: Optional[dict] = None
