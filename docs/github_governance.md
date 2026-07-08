# GitHub Governance

This document describes the intended repository settings. These settings are documented only; they are not automatically enforced by code in Phase 1.

## Branch Protection Target

Protect the `main` branch.

Recommended branch protection:

- require pull requests before merging
- require at least one approving reviewer
- require review from CODEOWNERS for owned paths
- require conversation resolution before merge
- require status checks after workflows are implemented
- block force pushes
- block branch deletion

## Branch Model

Use trunk-based development with `main` as the only long-lived branch. Short-lived feature branches should be merged through pull requests.

## Pull Requests

All changes should be introduced through pull requests. Pull requests should include:

- summary of intent
- validation evidence
- security checklist confirmation
- documentation updates when behavior or process changes

## Required Reviewers

The default target is at least one reviewer. Security-sensitive changes should include a reviewer from the security owner group.

## CODEOWNERS

The `.github/CODEOWNERS` file identifies owner groups for security content, robot mock code, scripts, and documentation.

## Planned Required Status Checks

Future required checks may include:

- lint
- format check
- tests
- coverage
- configuration validation
- secret scanning
- dependency scanning
- static analysis
- SBOM generation
- container image scan
- signing verification

## Environments

Planned GitHub environments:

- `staging` for automated deployment validation
- `production` for future protected promotion

Production should require stronger review and deployment approval than staging.

## Secrets Policy

Secrets must not be committed to the repository. Use GitHub Actions secrets or environment-scoped secrets when workflows are added. Local `.env` files must remain untracked.

## Phase 1 Limitation

No GitHub Actions workflows exist yet. Required status checks cannot be enforced until the workflows are implemented in later phases.
