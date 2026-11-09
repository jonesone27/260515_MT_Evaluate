# Machine Translation Evaluation Platform

A **FastAPI-based platform for machine translation and translation quality evaluation**.

The platform integrates external machine translation providers and automated evaluation metrics to assess the quality of machine-generated translations. It provides a REST API for translation and evaluation workflows and uses Prometheus and Grafana for monitoring and visualization.

The application is containerized with Docker and orchestrated using Docker Compose.

## Features

### Machine Translation

- Integration with **Azure Translator**
- Integration with **DeepL**
- REST API endpoints for translation workflows

### Machine Translation Evaluation

The platform currently integrates two evaluation metrics:

- **BARTScore** – reference-based evaluation using a pretrained sequence-to-sequence model
- **COMETKiwi** – reference-free evaluation using source text and machine translation output

The evaluation API supports the following input combinations:

| Input | Evaluation |
|---|---|
| Translation (hypothesis) + reference | BARTScore |
| Translation (hypothesis) + source | COMETKiwi |
| Translation (hypothesis) + reference + source | BARTScore and COMETKiwi |
| Translation only | Rejected because the required evaluation context is missing |

Evaluation results include aggregate metric scores and segment-level results where supported.

### Monitoring and Observability

- FastAPI application metrics exposed through `/metrics`
- Prometheus metrics collection
- Prometheus recording rules
- Grafana dashboards for metric visualization
- Docker Compose orchestration of the application and monitoring services

### Engineering

- FastAPI REST API
- Pydantic request and response models
- Separation of API routers, application services, external clients and evaluation metric implementations
- Environment-variable-based configuration and secret management
- Docker image and Docker Compose deployment
- Automated tests for application components and external service integrations

## Architecture

The current architecture consists of the FastAPI application and a monitoring stack.

```text
                       Docker Compose
                              |
             +----------------+----------------+
             |                |                |
             v                v                v
          FastAPI         Prometheus         Grafana
          :8000             :9090             :3000
             |                ^                |
             |                |                |
             +-- /metrics ----+                |
                              |                |
                              +----------------+
                                 Data source

          FastAPI
             |
             +-- Translation services
             |      +-- Azure Translator
             |      +-- DeepL
             |
             +-- Evaluation services
                    +-- BARTScore
                    +-- COMETKiwi
```

Prometheus collects runtime and application metrics exposed by FastAPI. Grafana uses Prometheus as its data source to query and visualize the collected metrics.

## Technology Stack

| Area | Technologies |
|---|---|
| Programming language | Python 3.11 |
| API framework | FastAPI |
| ASGI server | Uvicorn |
| Data validation | Pydantic |
| Machine translation | Azure Translator, DeepL |
| Evaluation metrics | BARTScore, COMETKiwi |
| Model integration | Hugging Face, COMET |
| Testing | Pytest |
| Containerization | Docker, Docker Compose |
| Monitoring | Prometheus |
| Visualization | Grafana |
| Version control | Git, GitHub |

## Project Structure

The project separates API routing, application services, external provider clients, evaluation metrics and monitoring.

```text
.
├── .github/
├── app/
│   ├── __init__.py
│   └── main.py
├── clients/
│   ├── __init__.py
│   ├── aztr_client.py
│   └── deepl_client.py
├── data/    # For storage of source and translation files
├── docs/
│   ├── Architecture/
│   └── Requirements/
├── evaluation_metrics/
│   ├── __init__.py
│   ├── bartscore.py
│   └── cometkiwi22.py
├── models/
│   ├── __init__.py
│   ├── evaluation_model.py
│   └── translation_model.py
├── monitoring/
│   └── metrics.py
├── routers/
│   ├── __init__.py
│   ├── evaluation_router.py
│   └── translation_router.py
├── services/
│   ├── __init__.py
│   ├── evaluation_service.py
│   ├── file_service.py
│   └── translation_service.py
├── tests/
├── BARTScore/                  # External dependency; excluded from Git
├── Dockerfile
├── compose.yml
├── prometheus.yml
├── prometheus_mt_evaluate_rules.rules
├── pytest.ini
├── requirements.txt
├── .dockerignore
├── .gitignore
└── README.md
```

The BARTScore directory is obtained separately and is not included in the platform repository.

## Installation

Clone the platform repository:

```bash
git clone https://github.com/jonesone27/260515_MT_Evaluate.git
cd 260515_MT_Evaluate
```

### Local Python Environment

Python 3.11 is recommended.

**Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### External BARTScore Dependency

The platform uses the original [BARTScore implementation](https://github.com/neulab/BARTScore).

The external repository is not included in this project. Clone it into the project root:

```bash
git clone https://github.com/neulab/BARTScore.git BARTScore
```

The expected directory structure is:

```text
260515_MT_Evaluate/
├── BARTScore/
│   ├── bart_score.py
│   ├── utils.py
│   └── ...
└── evaluation_metrics/
    └── bartscore.py
```

By default, the application expects the BARTScore repository in this location.

If the repository is located elsewhere, configure the `BARTSCORE_DIR` environment variable to point to its location.

Refer to the original BARTScore repository for its installation requirements and license information.

### Model Access

COMETKiwi uses the Hugging Face model `Unbabel/wmt22-cometkiwi-da`.

Access requires a Hugging Face account, acceptance of the model's access conditions and an appropriate authentication token.

BARTScore uses the pretrained model `facebook/bart-large-cnn`.

Model weights may be downloaded when the models are initialized, depending on the local cache.

## Environment Variables

Create a local `.env` file in the project root.

The application uses credentials for external translation services and may require Hugging Face authentication for access to gated evaluation models.

Example:

```text
AZURE_TRANSLATOR_KEY=your_azure_key
DEEPL_API_KEY=your_deepl_key
HF_TOKEN=your_huggingface_token
```

The variable names above should match the actual application configuration. Additional provider-specific configuration may also be required.

If BARTScore is installed outside the default location, configure:

```text
BARTSCORE_DIR=path/to/BARTScore
```



## Running with Docker Compose

Build and start the application and monitoring stack:

```bash
docker compose up -d --build
```

### Services

| Service | URL |
|---|---|
| FastAPI Swagger UI | http://localhost:8000/docs |
| FastAPI metrics | http://localhost:8000/metrics |
| Prometheus | http://localhost:9090 |
| Prometheus targets | http://localhost:9090/targets |
| Grafana | http://localhost:3000 |

Grafana uses Prometheus as its data source. Within the Docker Compose network, Prometheus is accessible at:

```text
http://prometheus:9090
```

The external BARTScore repository must also be available inside the FastAPI container. When using the default project-root location, it must be included in the Docker build context.

Stop the services:

```bash
docker compose down
```

To stop the services and remove named volumes:

```bash
docker compose down -v
```

**Caution:** The latter command deletes persisted Docker volume data, including Grafana data.

## Running Locally

Start the FastAPI application:

```bash
uvicorn app.main:app --reload
```

Open the interactive API documentation:

http://localhost:8000/docs

## Testing

Run the test suite:

```bash
pytest
```

Run tests with coverage reporting:

```bash
pytest --cov --cov-report term-missing
```

The repository includes tests for evaluation metrics, evaluation services, evaluation API integration, translation API integration and translation unit/mock testing.

Test coverage should be verified against the current test results before publishing numerical coverage claims.

## Current Development Status

The platform currently provides:

- Azure Translator and DeepL integrations
- BARTScore and COMETKiwi evaluation
- FastAPI-based translation and evaluation workflows
- Docker Compose deployment
- Prometheus metrics collection and recording rules
- Grafana integration and an initial monitoring dashboard
- Automated tests for application components and integrations

### Planned Development

- Refinement of Prometheus and Grafana configuration to better reflect platform behaviour and evaluation workloads
- PostgreSQL integration for persistent evaluation-result storage
- Persistence and retrieval of evaluation records
- Further evaluation metrics and metric-specific result handling
- Expanded automated testing and monitoring
- Authentication and authorization

PostgreSQL is planned as the relational database for storing evaluation results. Database persistence is not yet implemented.

## License

MIT License