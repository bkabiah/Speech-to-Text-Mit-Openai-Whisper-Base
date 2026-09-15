FROM python:3.10-slim

WORKDIR /app

# System dependencies for audio processing
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app

# Pre-download models during build to speed up container startup
RUN python -c "from transformers import pipeline; pipeline('automatic-speech-recognition', model='openai/whisper-base', device=-1); pipeline('automatic-speech-recognition', model='openai/whisper-tiny', device=-1)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
