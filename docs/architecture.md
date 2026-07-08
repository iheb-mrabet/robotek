# Architecture

## Target Architecture

This repository is a generic DevSecOps template for robotic software. It provides the governance, documentation, security rules, and local validation commands that future robot repositories can reuse.

The current application is a small mock robot service. It does not connect to real robot hardware, ROS 2 nodes, sensors, actuators, or production infrastructure. Its purpose is to give future CI/CD, security scanning, packaging, and deployment stages a realistic but safe target.

## Current Repository Structure

- `.github/` contains repository governance templates, but no workflow files.
- `docs/` contains architecture, governance, local usage, runbook, backlog, and ADR documentation.
- `security/` contains the threat model, security rules, and exception register.
- `robot_mock/` contains a small Python mock robot application.
- `scripts/` contains local validation utilities.
- `docker/` and `artifacts/` are placeholders for later phases.

## Mock Robot Role

The mock robot provides:

- safety configuration validation
- simple mission state progression
- deterministic health/status reporting
- a minimal FastAPI interface
- unit tests for CI/CD proof points

It exists so future pipeline stages can validate meaningful code without needing the real robot repositories yet.

## Future PR Gate

The planned pull request gate will run local-equivalent checks such as linting, formatting, tests, coverage, configuration validation, dependency review, secret detection, and security scans.

These checks are documented now and will be implemented later. No GitHub Actions workflows are created in Phase 1.

## Future Main Delivery Pipeline

After pull request checks pass and changes merge to `main`, later phases will add packaging, container image creation, SBOM generation, image scanning, signature, staging deployment, smoke testing, and rollback procedures.

## Phase 1 Scope

Phase 1 implements:

- repository skeleton
- governance files
- documentation and ADRs
- threat model and security rules
- pre-commit configuration
- Makefile commands
- mock robot app, configuration, and tests

## Future Work

Future phases will add CI workflows, security workflows, Docker packaging, SBOM creation, image signing, staging deployment, and final template hardening. ROS 2 integration can be introduced when the real robot software shape is known.
