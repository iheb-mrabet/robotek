# ADR-002: Trunk-Based Development

## Status

Accepted

## Context

The repository should model a simple delivery process that supports frequent review, fast validation, and clear branch protection.

## Decision

Use trunk-based development with `main` as the only long-lived branch. Work should happen on short-lived branches and merge through pull requests.

## Consequences

The model reduces branch drift and fits automated pull request gates. It requires reliable validation before merge, which will be implemented in later CI phases.
