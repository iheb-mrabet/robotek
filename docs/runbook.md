# Runbook

## Local Validation

Run the Phase 1 check before opening a pull request:

```bash
make phase1-check
```

This command runs linting, tests, and robot configuration validation.

## API Smoke Test

Start the API:

```bash
make run-api
```

In another terminal, check:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/mission
curl -X POST http://127.0.0.1:8000/mission/start
```

## Invalid Robot Configuration

If configuration validation fails:

1. Review the error message from `make validate-config`.
2. Check `robot_mock/configs/robot_profile.yaml`.
3. Check `robot_mock/configs/safety_rules.yaml`.
4. Correct the profile so it satisfies the safety rules.

Common failures:

- emergency stop disabled
- debug enabled in staging or production
- max speed above safety limit
- missing required field

## Secret Handling

If a secret is found in the repository:

1. Stop using the secret immediately.
2. Rotate the secret in the source system.
3. Remove the value from the repository.
4. Record follow-up work if history cleanup is required.

## Deployment

There is no real deployment in Phase 1. Staging and production deployment procedures will be added in later phases.
