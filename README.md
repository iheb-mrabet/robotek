# Robot DevSecOps Template

This repository is a DevSecOps CI/CD template for robotic software.

The goal is to build and test a complete pipeline before using it on a real robot software repository.

Since the real robot code is not available yet, this project uses a small mock robot application as a safe testing target.

---

## Project Goal

This project helps us build a CI/CD pipeline that can continuously check:

* code quality
* formatting
* unit tests
* test coverage
* robot configuration safety
* GitHub workflow behavior

---

## Phase 1 — Done

Phase 1 prepared the base project.

We created:

* the repository structure
* a mock robot application
* robot configuration files
* safety validation rules
* unit tests
* coverage checks
* Makefile commands
* basic documentation
* security and governance files

The mock robot is used as a safe target to test the pipeline.

It does not control real hardware, sensors, actuators, ROS 2 nodes, or production robots.

---

## Mock Robot Purpose

The mock robot allows us to test the pipeline before connecting it to real robot software.

It includes:

* health/status logic
* mission start/status logic
* safety rules
* configuration validation
* a small FastAPI interface
* unit tests

---

## Phase 2 — In Progress

Phase 2 is mostly done.

The main goal of Phase 2 is local/CI parity:

> What passes locally should also pass in GitHub Actions.

The CI pipeline currently runs the same Makefile targets that developers can run locally.

---

## CI Checks

The GitHub Actions pipeline runs these checks:

```bash
make lint
```

Checks Python code quality using Ruff.

It catches common style issues, bad imports, and simple code problems.

```bash
make format-check
```

Checks if the code is correctly formatted.

It does not modify files. It only fails if formatting is wrong.

```bash
make coverage
```

Runs the unit tests with pytest and measures test coverage.

This is the main testing gate of the pipeline. It checks that the mock robot logic, mission behavior, safety logic, and API behavior work correctly.

The pipeline fails if tests fail or if coverage is below the required threshold.

```bash
make validate-config
```

Validates the mock robot configuration against the safety rules.

This is the custom robot-safety gate of the project.

Example: if `robot_profile.yaml` sets a robot speed higher than the allowed safety limit, this check must fail.

---

## Configuration

Robot configuration files are in:

```text
robot_mock/configs/
```

Main files:

* `robot_profile.yaml`
* `safety_rules.yaml`

Example safety check:

If `robot_profile.yaml` has:

```yaml
max_speed_mps: 5.0
```

but `safety_rules.yaml` allows only:

```yaml
max_allowed_speed_mps: 1.5
```

then the pipeline must fail.

This proves the CI can block unsafe robot configuration before it reaches `main`.

---

## Branch Model

`main` is the protected branch.

The expected workflow is:

```text
create branch → open pull request → CI passes → merge to main
```

Direct pushes to `main` should be blocked.

---

## Not Implemented Yet

Planned for later phases:

* Docker build
* SBOM generation
* vulnerability scanning
* artifact signing
* deployment
* ROS 2 integration
* real robot integration
* stronger supply-chain hardening

---

## Current Status

Phase 1 is complete.

Phase 2 is mostly complete.

Current work is focused on improving:

* CI failure messages
* diagnostic artifacts
* branch protection
* workflow stability
