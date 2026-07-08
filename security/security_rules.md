# Security Rules

## No Secrets in Repository

- Do not commit passwords, tokens, private keys, certificates, or cloud credentials.
- Keep local `.env` files untracked.
- Use environment-scoped secret storage when CI/CD is added.
- Rotate any secret that is accidentally committed.

## Safe Robot Configuration

Robot profiles must satisfy the safety rules:

- emergency stop must be enabled when required
- debug mode must be disabled in staging and production
- max speed must not exceed the configured safety limit
- required fields must be present
- default mission waypoints must be explicit and non-empty

## Dependency Security

- Keep dependencies minimal.
- Prefer maintained packages.
- Review dependency additions.
- Add dependency scanning in a later security workflow.

## Container Future Rules

When container packaging is added:

- use a minimal base image
- generate an SBOM
- scan the image before deployment
- sign or attest the artifact
- avoid embedding secrets in image layers

## CI/CD Future Rules

When workflows are added:

- run blocking checks on pull requests
- restrict deployment credentials to protected environments
- require stronger approval for production
- record deployment metadata
- support rollback from staging failures
