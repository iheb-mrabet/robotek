# ADR-001: Single Repository

## Status

Accepted

## Context

The real robot repositories are not available yet. The project needs a simple place to define governance, security rules, documentation, and mock application behavior for future DevSecOps testing.

## Decision

Use a single repository for the Phase 1 template, documentation, mock robot application, scripts, and local tooling.

## Consequences

This keeps early development simple and makes the future pipeline easier to demonstrate. If real robot software later requires separate repositories, this template can be copied or adapted.
