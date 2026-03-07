# GEMINI.md - Project Context

## Overview
`learning-rag` is a project dedicated to learning how to create Retrieval-Augmented Generation (RAG) applications with a strong focus on observability using OpenTelemetry (OTel).

Currently, it provides a foundational FastAPI application instrumented with OTel traces, integrated with a monitoring stack (Grafana, Tempo, OTel Collector).

## Tech Stack
- **Language**: Python 3.14+
- **Framework**: FastAPI
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Task Runner**: [just](https://github.com/casey/just)
- **Observability**: OpenTelemetry (Python SDK), Grafana Tempo (Tracing backend), OTel Collector, Grafana.
- **Infrastructure**: Docker Compose (for the monitoring stack).

## Key Directories
- `src/learning_rag/`: Main source code.
  - `app.py`: FastAPI application entry point with OTel instrumentation.
- `deployment/`: Configuration files for infrastructure services.
  - `otel-collector/`: OpenTelemetry Collector configuration.
  - `tempo/`: Grafana Tempo configuration.
- `docker-compose.yaml`: Orchestrates the monitoring stack (Grafana, Tempo, OTel Collector).

## Building and Running

### Prerequisites
- Install `uv` and `just`.
- Docker and Docker Compose installed for monitoring.
- We are using Windows and Powershell.

### Commands
- **Install Dependencies**: `uv sync`
- **Start Monitoring Stack**: `just monitoring` (Starts Tempo, OTel Collector, and Grafana).
- **Run Application (Dev Mode)**: `uv run fastapi dev src/learning_rag/app.py`
- **Build/Package**: `uv build`

## Architecture & Observability
The application is instrumented with OpenTelemetry to export traces via OTLP (HTTP) to a local OTel Collector (port 4318). The Collector then forwards these traces to Grafana Tempo (port 3200) for storage. Traces can be visualized and queried in Grafana (port 3000).

## Development Conventions
- **Observability First**: All new features should be instrumented with OpenTelemetry spans where appropriate.
- **Task Runner**: Use `just` for infrastructure and lifecycle management tasks.
- **Type Safety**: Leverage Python's type hints and FastAPI's Pydantic models for request/response validation.
