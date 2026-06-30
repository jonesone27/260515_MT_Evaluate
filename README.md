# Machine Translation Evaluation API

A **FastAPI-based backend service** for machine translation and translation quality evaluation.

The application integrates external machine translation providers (**Azure Translator** and **DeepL**) and supports automatic evaluation of translation quality using established machine translation metrics.

---

## Features

### Translation

- Translate text using **Azure Translator**
- Translate text using **DeepL**

### Evaluation

Evaluate machine translation output using:

- **BLEU**
- **chrF**
- **TER**

### Engineering Features

- **FastAPI** REST API
- Environment variable-based secret management
- Unit tests
- Integration tests
- Mock tests for external API calls
- Failure-path testing (timeouts, connection errors)
- Test coverage reporting

---

## Architecture

```text
Client
   |
FastAPI Routers
   |
Service Layer
   |
External APIs (Azure / DeepL)
```

Project structure:

```text
.
├── app/
├── clients/
├── data/
├── models/
├── routers/
├── services/
├── tests/
├── requirements.txt
└── README.md
```

---

## Technology Stack

- Python 3
- FastAPI
- Uvicorn
- Requests
- DeepL SDK
- Azure Translator API
- SacreBLEU
- Pytest
- Pytest-Cov

---

## Installation

Clone the repository:

```bash
git clone https://github.com/jonesone27/260515_MT_Evaluate.git

```

Create and activate a virtual environment.

### Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

The application requires the following environment API keys (available from the respective machine translation providers):

```text
AZURE_TRANSLATOR_KEY
DEEPL_API_KEY
```

Example (Linux):

```bash
export AZURE_TRANSLATOR_KEY="your_azure_key"
export DEEPL_API_KEY="your_deepl_key"
```

---

## Running the Application

Start the API server:

```bash
uvicorn app.main:app --reload
```

Swagger documentation is available at:

```text
http://localhost:8000/docs
```

---

## Running Tests

Run all tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov --cov-report term-missing
```

Current coverage: **98%**

---

## Future Improvements

- GitHub Actions CI/CD pipeline
- Prometheus metrics endpoint
- Structured logging and observability
- Docker support
- Persistent storage of evaluation results

---

## License

MIT License
