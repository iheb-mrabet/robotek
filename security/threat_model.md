# Threat Model

## Assets

- source code
- robot configuration files
- future CI/CD credentials
- future build artifacts
- future container images
- future deployment environments
- safety rules and exception records

## Trust Boundaries

- developer workstation to repository
- repository to CI/CD runner
- CI/CD runner to artifact registry
- artifact registry to staging environment
- staging environment to future robot-adjacent systems

## Threats

- secrets committed to source control
- unsafe robot configuration merged without review
- dependency compromise
- malicious or vulnerable build artifact
- bypassed pull request review
- unreviewed security exception
- incorrect deployment promotion
- drift between documented process and actual automation

## Mitigations

- pre-commit hooks for basic hygiene and secret detection
- documented branch protection and CODEOWNERS
- safety validation for robot configuration
- unit tests for mission, safety, and health logic
- planned CI and security workflows
- planned SBOM, scanning, and signing for artifacts
- explicit security exception register

## Assumptions

- No real robot hardware is connected in Phase 1.
- No ROS 2 runtime, device drivers, sensors, or actuators are used in Phase 1.
- GitHub governance settings are documented but not enforced by repository code.
- Future CI/CD credentials will be stored outside the repository.

## Limitations

The mock robot cannot model every real robotic threat. Physical safety, network segmentation, field operations, firmware integrity, and live robot telemetry will need a new threat model when the real system exists.
