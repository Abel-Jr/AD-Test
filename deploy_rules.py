#!/usr/bin/env python3
"""
Deploys Sentinel scheduled analytics rules straight through the Azure REST API,
reading each .yml file in detection-rules/sentinel/.

Why this exists instead of the AzSentinel PowerShell module:
- AzSentinel silently drops entityMappings, customDetails, alertDetailsOverride
  and relevantTechniques - they're just not in its request body.
- AzSentinel hasn't been updated since Feb 2021 and has a bug where
  Import-AzSentinelAlertRule crashes on null when a previous partial deploy
  left a rule in a weird state.
- Calling the API directly means we control exactly what gets sent, and
  Azure CLI (`az rest`) is already on the GitHub Actions runner - no extra
  PowerShell modules to install.

Auth: relies on `az login` already having run (via azure/login@v2 in the
workflow) - this script just shells out to `az rest`.
"""

import glob
import json
import os
import subprocess
import sys

import yaml

SUBSCRIPTION_ID = os.environ["SUBSCRIPTION_ID"]
RESOURCE_GROUP = os.environ["RESOURCE_GROUP"]
WORKSPACE_NAME = os.environ["WORKSPACE_NAME"]
RULES_DIR = os.environ.get("RULES_DIR", "detection-rules/sentinel")
API_VERSION = "2023-02-01"

# The API wants the full PascalCase name, not the short form some tools use
TRIGGER_OPERATOR_MAP = {
    "gt": "GreaterThan",
    "lt": "LessThan",
    "eq": "Equal",
    "ne": "NotEqual",
    "greaterthan": "GreaterThan",
    "lessthan": "LessThan",
    "equal": "Equal",
    "notequal": "NotEqual",
}


def normalize_trigger_operator(value: str) -> str:
    return TRIGGER_OPERATOR_MAP.get(value.lower(), value)


def build_url(rule_id: str) -> str:
    return (
        f"https://management.azure.com/subscriptions/{SUBSCRIPTION_ID}"
        f"/resourceGroups/{RESOURCE_GROUP}"
        f"/providers/Microsoft.OperationalInsights/workspaces/{WORKSPACE_NAME}"
        f"/providers/Microsoft.SecurityInsights/alertRules/{rule_id}"
        f"?api-version={API_VERSION}"
    )


def build_body(rule: dict) -> dict:
    """Maps our YAML schema onto the actual Sentinel REST API schema."""
    return {
        "kind": "Scheduled",
        "properties": {
            "displayName": rule["name"],
            "description": rule.get("description", ""),
            "severity": rule["severity"],
            "enabled": rule.get("enabled", False),
            "query": rule["query"],
            "queryFrequency": rule["queryFrequency"],
            "queryPeriod": rule["queryPeriod"],
            "triggerOperator": normalize_trigger_operator(rule["triggerOperator"]),
            "triggerThreshold": rule["triggerThreshold"],
            "suppressionDuration": rule.get("suppressionDuration", "PT1H"),
            "suppressionEnabled": rule.get("suppressionEnabled", False),
            "tactics": rule.get("tactics", []),
            "techniques": rule.get("relevantTechniques", []),
            "entityMappings": rule.get("entityMappings", []),
            "customDetails": rule.get("customDetails", {}),
            "alertDetailsOverride": rule.get("alertDetailsOverride", {}),
            "eventGroupingSettings": rule.get(
                "eventGroupingSettings", {"aggregationKind": "SingleAlert"}
            ),
            "incidentConfiguration": rule.get(
                "incidentConfiguration", {"createIncident": True}
            ),
        },
    }


def deploy_rule(filepath: str) -> bool:
    with open(filepath) as f:
        rule = yaml.safe_load(f)

    rule_id = rule["id"]
    url = build_url(rule_id)
    body = build_body(rule)

    body_file = "body.json"
    with open(body_file, "w") as f:
        json.dump(body, f)

    print(f"Deploying {filepath} -> rule id {rule_id} ({rule['name']})")

    result = subprocess.run(
        ["az", "rest", "--method", "put", "--url", url, "--body", f"@{body_file}"],
        capture_output=True,
        text=True,
    )

    os.remove(body_file)

    if result.returncode != 0:
        print(f"  FAILED: {result.stderr.strip()}")
        return False

    print("  OK")
    return True


def main() -> None:
    files = sorted(glob.glob(f"{RULES_DIR}/*.yml"))
    if not files:
        print(f"No .yml files found in {RULES_DIR}")
        sys.exit(1)

    failures = []
    for filepath in files:
        if not deploy_rule(filepath):
            failures.append(filepath)

    if failures:
        print(f"\n{len(failures)} rule(s) failed to deploy:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)

    print(f"\nAll {len(files)} rule(s) deployed successfully.")


if __name__ == "__main__":
    main()