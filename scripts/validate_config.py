"""Validate the default mock robot configuration."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
repo_root = str(REPO_ROOT)
if repo_root in sys.path:
    sys.path.remove(repo_root)
sys.path.insert(0, repo_root)

from robot_mock.app.safety import (  # noqa: E402
    DEFAULT_PROFILE_PATH,
    DEFAULT_RULES_PATH,
    SafetyValidationError,
    assert_safe_robot_profile,
    load_yaml_config,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate mock robot configuration.")
    parser.add_argument(
        "--profile",
        type=Path,
        default=DEFAULT_PROFILE_PATH,
        help="Path to robot profile YAML.",
    )
    parser.add_argument(
        "--rules",
        type=Path,
        default=DEFAULT_RULES_PATH,
        help="Path to safety rules YAML.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        profile = load_yaml_config(args.profile)
        rules = load_yaml_config(args.rules)
        assert_safe_robot_profile(profile, rules)
    except SafetyValidationError as exc:
        print(f"Configuration invalid: {exc}", file=sys.stderr)
        return 1

    print(f"Configuration valid: {args.profile} satisfies {args.rules}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
