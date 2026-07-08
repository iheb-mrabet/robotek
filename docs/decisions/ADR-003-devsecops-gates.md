# ADR-003: Blocking DevSecOps Gates

## Status

Accepted

## Context

Robotic software can create safety and operational risk. Even this mock template should establish the expectation that quality and security checks block unsafe changes.

## Decision

Future CI/CD workflows will use blocking gates for linting, tests, coverage, configuration validation, secret scanning, dependency scanning, static analysis, artifact scanning, and deployment smoke tests.

## Consequences

Developers get fast feedback and unsafe changes are stopped before merge or deployment. The checks must be kept reliable so teams do not work around them.
