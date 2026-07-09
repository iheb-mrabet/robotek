# Robot DevSecOps Template

This repository is a generic DevSecOps CI/CD template for robotic software. It establishes the Phase 1 repository skeleton, governance documentation, security rules, local tooling, and a small mock robot application that future pipeline work can validate.

## Why the Mock Robot Exists

The real robot repositories are not available yet. The mock robot gives future CI/CD and DevSecOps stages something safe and realistic to test:

- robot profile validation
- safety rules
- mission state transitions
- health/status output
- a minimal FastAPI interface
- unit tests and coverage

The mock does not control hardware, run ROS 2 nodes, read sensors, move actuators, or deploy to a real robot.

## Branch Model

Use trunk-based development. `main` is the only long-lived branch, and changes should merge through pull requests.

## Implemented Now

- repository skeleton
- governance files
- documentation
- threat model
- security rules and exception register
- pre-commit configuration
- Makefile commands
- mock Python robot package
- YAML robot configuration
- configuration validation script
- unit tests

## Intentionally Not Implemented Yet

- GitHub Actions workflows
- Dockerfile or container build
- SBOM generation
- image scanning
- artifact signing
- staging deployment
- production deployment
- real robot hardware integration
- ROS 2 runtime integration

GitHub Actions CI is intentionally not created in Phase 1. Planned workflows are documented in `docs/github_actions_mapping.md`.

## Local Setup

```bash
make bootstrap
```
k
## Local Commands

```bash
make help
make lint
make format
make test
make coverage
make validate-config
make phase1-check
make precommit
```
kl;
...
test rule set 
## Run the API Locally

```bash
make run-api
```

The API is served at `http://127.0.0.1:8000`.

Endpoints:

- `GET /health`
- `GET /mission`
- `POST /mission/start`

## Configuration

Default configuration files live in `robot_mock/configs/`:

- `robot_profile.yaml`
- `safety_rules.yaml`
- `staging.env.example`

Validate them locally:

```bash
make validate-config
```

## Phase 1 Check

Run the local Phase 1 quality gate:

```bash
make phase1-check
```

This runs linting, tests, and configuration validation. Later GitHub Actions workflows can call the same commands. (testing ci first time )
