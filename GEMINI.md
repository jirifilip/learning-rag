# GEMINI.md - Project Context

## Overview
`learning-rag` is a project dedicated to learning how to create Retrieval-Augmented Generation (RAG) applications with a strong focus on observability using OpenTelemetry (OTel).

Currently, it provides a foundational FastAPI application instrumented with OTel traces, integrated with a monitoring stack (Grafana, Jaeger, OTel Collector).

## Tech Stack
- **Language**: Python 3.14+
- **Framework**: FastAPI
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Task Runner**: [just](https://github.com/casey/just)
- **Observability**: OpenTelemetry (Python SDK), Jaeger (Tracing backend), OTel Collector, Grafana, Prometheus.
- **Infrastructure**: Docker Compose (for the monitoring stack).

## Key Directories
...
- `deployment/`: Configuration files for infrastructure services.
  - `monitoring/`: Monitoring stack configuration.
    - `otel-collector/`: OpenTelemetry Collector configuration.
    - `jaeger/`: Jaeger tracing backend configuration.
    - `prometheus/`: Prometheus metrics configuration.
    - `grafana/`: Grafana dashboards and data sources.
    - `monitoring.docker-compose.yaml`: Orchestrates the monitoring stack.

## Building and Running

### Prerequisites
- Install `uv` and `just`.
- Docker and Docker Compose installed for monitoring.

### Commands
- **Install Dependencies**: `uv sync`
- **Start Monitoring Stack**: `just monitoring` (Starts Jaeger, Prometheus, OTel Collector, and Grafana).
- **Run Application (Dev Mode)**: `uv run fastapi dev src/learning_rag/app.py`
- **Build/Package**: `uv build`

## Architecture & Observability
The application is instrumented with OpenTelemetry to export traces via OTLP (HTTP) to a local OTel Collector (port 4318). The Collector then forwards these traces to Jaeger (port 16686) for storage. Traces can be visualized and queried in Grafana (port 3000).


## Development Conventions
- **Observability First**: All new features should be instrumented with OpenTelemetry spans where appropriate.
- **Task Runner**: Use `just` for infrastructure and lifecycle management tasks.
- **Type Safety**: Leverage Python's type hints and FastAPI's Pydantic models for request/response validation.
