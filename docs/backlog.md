# Backlog
## Phase 1: mock app , architecure 
done; 

## Phase 2: CI Workflow

- Add pull request CI workflow.
- Run lint, format check, tests, coverage, and configuration validation.
- Configure required status checks for `main`.
status : in progress (80%)

## Phase 3: Security Workflow

- Add secret scanning workflow.
- Add dependency vulnerability scanning.
- Add static analysis.
- Add policy checks for security exceptions.
 
## Phase 4: Docker, SBOM, Scan, Signature

- Add Dockerfile and container build workflow.
- Generate SBOM.
- Scan container image.
- Sign image or publish provenance metadata.
- Store build artifacts consistently.

## Phase 5: Staging Deploy and Rollback

- Add staging environment.
- Deploy approved artifact to staging.
- Run smoke tests.
- Record rollback procedure.
- Add rollback automation.

## Phase 6: Generic Template and Final Demo

- Generalize names and variables for reuse.
- Add template usage instructions.
- Add final demo script.
- Document how real robot repositories can adopt the template.
