


# 🎙️ STT AI Platform (Speech-to-Text)

Eine produktionsreife, Full-Stack Speech-to-Text-Anwendung mit CPU-optimierten Hugging Face Modellen, asynchroner FastAPI-Architektur und moderner MLOps-Pipeline.

**Live Demo:** http://31.97.158.220:5173/

---

## 📋 Inhaltsverzeichnis
- [Über das Projekt](#-über-das-projekt)
- [Architektur](#️-architektur)
- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [Installation](#-installation)
- [Debugging Journey](#-debugging-journey)
- [Deployment](#-deployment)
- [Warum dieses Projekt?](#-warum-dieses-projekt)

---

## 🎯 Über das Projekt

Diese Anwendung demonstriert meine Fähigkeiten als Junior AI Engineer im Bereich:
- **AI Engineering**: Integration von Hugging Face Whisper mit Fallback-Mechanismen
- **Backend Development**: Asynchrone FastAPI-Architektur mit CPU-Optimierung
- **MLOps**: Docker-Containerisierung, CI/CD mit GitHub Actions, AWS ECR
- **Observability**: LangSmith Tracing für AI-Pipelines
- **Protokolle**: Model Context Protocol (MCP) für Agenten-Integration

---

## 🏗️ Architektur

```mermaid
graph TB
    subgraph "Client Layer"
        A[React Frontend<br/>Vite + Axios]
    end

    subgraph "Reverse Proxy"
        B[Vite Dev Server<br/>Port 5173]
    end

    subgraph "Backend Layer"
        C[FastAPI Server<br/>Port 8002]
        D[STT Engine<br/>Whisper Base/Tiny]
        E[Plugin Manager]
        F[Skills<br/>Summarize/Translate]
    end

    subgraph "AI/ML Layer"
        G[Hugging Face<br/>Transformers]
        H[Whisper Models<br/>CPU Optimized]
    end

    subgraph "Observability"
        I[LangSmith<br/>Tracing]
    end

    subgraph "External Services"
        J[MCP Server<br/>Metadata Tools]
        K[AWS ECR<br/>Container Registry]
    end

    A -->|"HTTP POST /api/v1/transcribe"| B
    B -->|"Proxy"| C
    C --> D
    C --> E
    E --> F
    D --> G
    G --> H
    C --> I
    C --> J
    
    subgraph "CI/CD Pipeline"
        L[GitHub Actions]
        L -->|"Build & Push"| K
    end

    style A fill:#e1f5ff
    style B fill:#fff4e1
    style C fill:#e8f5e9
    style D fill:#f3e5f5
    style I fill:#fff9c4
    style J fill:#fce4ec
    style K fill:#e0f2f1
