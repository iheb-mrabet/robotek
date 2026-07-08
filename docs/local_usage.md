# Local Usage

## Requirements

- Python 3.11 or newer
- `make`
- internet access for the first dependency installation

## Setup

```bash
make bootstrap
```

## Common Commands

```bash
make lint
make format
make test
make coverage
make validate-config
make phase1-check
```

## Run the API

```bash
make run-api
```

The API starts with Uvicorn at `http://127.0.0.1:8000`.

Useful endpoints:

- `GET /health`
- `GET /mission`
- `POST /mission/start`

## Configuration Validation

The default robot profile is validated against the default safety rules:

```bash
python scripts/validate_config.py
```

The script exits with status `0` for valid configuration and non-zero for invalid configuration.

## Phase 1 Note

GitHub Actions CI is intentionally not created yet. The Makefile commands are the local equivalents that future workflows can call.
