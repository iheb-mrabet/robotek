# ADR-004: Container Image as Future Delivery Artifact

## Status

Accepted

## Context

Future deployment needs a portable, inspectable artifact that can be scanned, signed, and promoted through environments.

## Decision

Use a container image as the future delivery artifact. Docker implementation is deferred to a later phase.

## Consequences

Later phases can add SBOM generation, image scanning, signing, and deployment promotion. Phase 1 keeps only placeholder directories and documentation.
