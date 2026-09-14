from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    PROJECT_NAME: str = "STT AI Platform"
    PRIMARY_MODEL: str = "openai/whisper-base"
    FALLBACK_MODEL: str = "openai/whisper-tiny"
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_PROJECT: str = "stt-ai-junior-portfolio"

settings = Settings()
