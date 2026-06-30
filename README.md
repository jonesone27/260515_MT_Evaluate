# Machine Translation Evaluation API

A **FastAPI-based backend service** for machine translation and
translation quality evaluation.

The application integrates external machine translation providers
(**Azure Translator** and **DeepL**) and supports automatic evaluation
of translation quality using established machine translation metrics.

The project is containerized with **Docker** and orchestrated using
**Docker Compose**. It also exposes runtime metrics that are collected
by **Prometheus**.

------------------------------------------------------------------------

## Features

### Translation

-   Translate text using **Azure Translator**
-   Translate text using **DeepL**

### Evaluation

Evaluate machine translation output using:

-   **BLEU**
-   **chrF**
-   **TER**

### Monitoring

-   Prometheus metrics endpoint
-   Prometheus monitoring
-   Docker Compose orchestration

### Engineering Features

-   FastAPI REST API
-   Docker image
-   Docker Compose
-   Prometheus monitoring
-   Environment variable-based secret management
-   Unit tests
-   Integration tests
-   Mock tests for external API calls
-   Failure-path testing (timeouts, connection errors)
-   Test coverage reporting
-   GitHub Actions CI

------------------------------------------------------------------------

## Architecture

``` text
                    Docker Compose

+--------------------------------------------------+
|                                                  |
|  FastAPI (8000)                                  |
|       |                                          |
|       | /metrics                                 |
|       v                                          |
|  Prometheus (9090)                               |
|                                                  |
+--------------------------------------------------+
          |                           |
          |                           |
    Azure Translator              DeepL API
```

------------------------------------------------------------------------

## Project Structure

``` text
.
├── app/
├── clients/
├── data/
├── models/
├── routers/
├── services/
├── tests/
├── Dockerfile
├── compose.yaml
├── prometheus.yml
├── requirements.txt
├── requirements-dev.txt
├── .dockerignore
└── README.md
```

------------------------------------------------------------------------

## Technology Stack

-   Python 3
-   FastAPI
-   Uvicorn
-   Requests
-   DeepL SDK
-   Azure Translator API
-   SacreBLEU
-   Pytest
-   Pytest-Cov
-   Docker
-   Docker Compose
-   Prometheus

------------------------------------------------------------------------

## Installation

Clone the repository:

``` bash
git clone https://github.com/jonesone27/260515_MT_Evaluate.git
cd 260515_MT_Evaluate
```

### Local Python Environment

Linux:

``` bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows:

``` powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

------------------------------------------------------------------------

## Environment Variables

Create a `.env` file (recommended) or export the variables manually.

Required variables:

``` text
AZURE_TRANSLATOR_KEY
DEEPL_API_KEY
```

Example:

``` text
AZURE_TRANSLATOR_KEY=your_azure_key
DEEPL_API_KEY=your_deepl_key
```

------------------------------------------------------------------------

## Running with Docker Compose

Build and start the complete stack:

``` bash
docker compose up -d --build
```

Services:

  Service              URL
  -------------------- ----------------------------
  FastAPI Swagger UI   http://localhost:8000/docs
  Prometheus           http://localhost:9090

Stop the stack:

``` bash
docker compose down
```

------------------------------------------------------------------------

## Running Locally

``` bash
uvicorn app.main:app --reload
```

------------------------------------------------------------------------

## Running Tests

Run all tests:

``` bash
pytest
```

Run tests with coverage:

``` bash
pytest --cov --cov-report term-missing
```

Current coverage: **98%**

------------------------------------------------------------------------

## Future Improvements

-   Grafana dashboards
-   PostgreSQL persistence for evaluation results
-   Custom Prometheus business metrics
-   Authentication and authorization
-   OpenTelemetry tracing
-   Kubernetes deployment

------------------------------------------------------------------------

## License

MIT License
