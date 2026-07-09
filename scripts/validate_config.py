from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml


DEFAULT_ROBOT_PROFILE = Path("robot_mock/configs/robot_profile.yaml")
DEFAULT_SAFETY_RULES = Path("robot_mock/configs/safety_rules.yaml")
DEFAULT_REPORT_DIR = Path("artifacts/ci")


def read_yaml(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}
    except FileNotFoundError:
        raise ValueError(f"Required config file not found: {path}") from None
    except yaml.YAMLError as error:
        raise ValueError(f"Invalid YAML in {path}: {error}") from None

    if not isinstance(data, dict):
        raise ValueError(f"Expected YAML mapping/object in {path}, got {type(data).__name__}")

    return data


def find_line_number(path: Path, key: str) -> int:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return 1

    for index, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith(f"{key}:"):
            return index

    return 1


def as_number(value: Any, field_name: str, file_path: Path) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{file_path}: field '{field_name}' must be a number, got boolean")

    if not isinstance(value, int | float):
        raise ValueError(
            f"{file_path}: field '{field_name}' must be a number, got {type(value).__name__}"
        )

    return float(value)


def github_escape(message: str) -> str:
    return message.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def build_markdown_report(report: dict[str, Any]) -> str:
    status = report["status"]
    icon = "✅" if status == "passed" else "❌"

    lines = [
        f"# {icon} Robot Config Validation Report",
        "",
        f"**Status:** `{status}`",
        f"**Generated UTC:** `{report['checked_at_utc']}`",
        "",
        "## Checked files",
        "",
        f"- Robot profile: `{report['inputs']['robot_profile']}`",
        f"- Safety rules: `{report['inputs']['safety_rules']}`",
        "",
    ]

    findings = report["findings"]

    if not findings:
        lines.extend(
            [
                "## Result",
                "",
                "No robot safety configuration violations were found.",
                "",
            ]
        )
        return "\n".join(lines)

    lines.extend(["## Findings", ""])

    for finding in findings:
        lines.extend(
            [
                f"### {finding['severity']}: {finding['title']}",
                "",
                f"- **Rule ID:** `{finding['rule_id']}`",
                f"- **File:** `{finding['file']}`",
                f"- **Line:** `{finding['line']}`",
                f"- **Field:** `{finding['field']}`",
                f"- **Observed value:** `{finding['observed']}`",
                f"- **Allowed value:** `{finding['allowed']}`",
                "",
                "**What happened**",
                "",
                finding["message"],
                "",
                "**How to fix**",
                "",
                finding["developer_action"],
                "",
            ]
        )

    return "\n".join(lines)


def write_reports(report: dict[str, Any], report_dir: Path) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)

    json_path = report_dir / "config_validation_report.json"
    markdown_path = report_dir / "config_validation_report.md"

    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(build_markdown_report(report) + "\n", encoding="utf-8")


def emit_github_annotations(report: dict[str, Any]) -> None:
    if os.getenv("GITHUB_ACTIONS") != "true":
        return

    for finding in report["findings"]:
        title = github_escape(finding["title"])
        message = github_escape(finding["message"])
        file_path = finding["file"]
        line = finding["line"]

        print(f"::error file={file_path},line={line},title={title}::{message}")


def append_github_summary(report: dict[str, Any]) -> None:
    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return

    markdown = build_markdown_report(report)
    with Path(summary_path).open("a", encoding="utf-8") as summary:
        summary.write(markdown)
        summary.write("\n")


def validate_config(robot_profile_path: Path, safety_rules_path: Path) -> dict[str, Any]:
    checked_at_utc = datetime.now(UTC).isoformat()

    report: dict[str, Any] = {
        "gate": "validate-config",
        "status": "passed",
        "checked_at_utc": checked_at_utc,
        "inputs": {
            "robot_profile": str(robot_profile_path),
            "safety_rules": str(safety_rules_path),
        },
        "findings": [],
    }

    try:
        robot_profile = read_yaml(robot_profile_path)
        safety_rules = read_yaml(safety_rules_path)

        if "max_speed_mps" not in robot_profile:
            raise ValueError(f"{robot_profile_path}: missing required field 'max_speed_mps'")

        if "max_allowed_speed_mps" not in safety_rules:
            raise ValueError(f"{safety_rules_path}: missing required field 'max_allowed_speed_mps'")

        max_speed_mps = as_number(
            robot_profile["max_speed_mps"],
            "max_speed_mps",
            robot_profile_path,
        )
        max_allowed_speed_mps = as_number(
            safety_rules["max_allowed_speed_mps"],
            "max_allowed_speed_mps",
            safety_rules_path,
        )

        if max_speed_mps > max_allowed_speed_mps:
            line = find_line_number(robot_profile_path, "max_speed_mps")

            report["findings"].append(
                {
                    "severity": "ERROR",
                    "rule_id": "SAFETY_SPEED_LIMIT",
                    "title": "Robot profile speed exceeds safety limit",
                    "file": str(robot_profile_path),
                    "line": line,
                    "field": "max_speed_mps",
                    "observed": max_speed_mps,
                    "allowed": f"<= {max_allowed_speed_mps}",
                    "message": (
                        f"{robot_profile_path} sets max_speed_mps={max_speed_mps}, "
                        f"but {safety_rules_path} allows max_allowed_speed_mps="
                        f"{max_allowed_speed_mps}."
                    ),
                    "developer_action": (
                        f"Set max_speed_mps to a value <= {max_allowed_speed_mps}, "
                        "or update safety_rules.yaml through a reviewed robot-safety change."
                    ),
                }
            )

    except ValueError as error:
        report["findings"].append(
            {
                "severity": "ERROR",
                "rule_id": "CONFIG_SCHEMA_ERROR",
                "title": "Robot configuration schema error",
                "file": str(robot_profile_path),
                "line": 1,
                "field": "config",
                "observed": "invalid",
                "allowed": "valid YAML with required robot safety fields",
                "message": str(error),
                "developer_action": "Fix the YAML file or restore the required config field.",
            }
        )

    if report["findings"]:
        report["status"] = "failed"

    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate robot profile against safety rules.")
    parser.add_argument(
        "--robot-profile",
        type=Path,
        default=DEFAULT_ROBOT_PROFILE,
        help="Path to robot_profile.yaml",
    )
    parser.add_argument(
        "--safety-rules",
        type=Path,
        default=DEFAULT_SAFETY_RULES,
        help="Path to safety_rules.yaml",
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=DEFAULT_REPORT_DIR,
        help="Directory where CI diagnostic reports will be written",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    report = validate_config(args.robot_profile, args.safety_rules)

    write_reports(report, args.report_dir)
    emit_github_annotations(report)
    append_github_summary(report)

    markdown_report = build_markdown_report(report)
    print(markdown_report)

    return 1 if report["status"] == "failed" else 0


if __name__ == "__main__":
    sys.exit(main())