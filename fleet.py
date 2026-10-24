
"""
fleet.py

Purpose:
    Evaluate simulated endpoint devices against a configurable policy.
    Print a compliance report and export the results to CSV.

Validation:
    Check inventory structure and field types before policy evaluation.
    Invalid records are marked non-compliant with HIGH risk instead
    of crashing the report.

Scope:
    All device records are simulated. This script does not collect
    settings from real computers.
"""

import csv
import json


def evaluate_device(device, policy):
    """Validate and evaluate one simulated endpoint device."""

    # Reject records that are not JSON objects represented as dictionaries.
    if not isinstance(device, dict):
        return {
            "status": "NON-COMPLIANT",
            "risk_level": "HIGH",
            "issues": ["Invalid device record: expected a JSON object"],
        }

    # These fields are needed to evaluate and report a device.
    required_fields = [
        "id",
        "owner",
        "os",
        "os_version",
        "encryption",
        "screen_lock",
    ]

    # Find missing fields before reading any values from the record.
    issues = [
        f"Missing required field: {field}"
        for field in required_fields
        if field not in device
    ]

    # Stop early so missing values cannot cause a KeyError.
    if issues:
        return {
            "status": "NON-COMPLIANT",
            "risk_level": "HIGH",
            "issues": issues,
        }

    # IDs and owner names must be non-empty strings.
    for field in ["id", "owner"]:
        if not isinstance(device[field], str) or not device[field].strip():
            issues.append(f"Invalid value for field: {field}")

    # Operating-system names must be non-empty strings.
    if not isinstance(device["os"], str) or not device["os"].strip():
        issues.append("Invalid operating system value")

    # OS versions must be integers, and Boolean values are not acceptable.
    if (
        not isinstance(device["os_version"], int)
        or isinstance(device["os_version"], bool)
    ):
        issues.append("Invalid OS version value")

    # Security settings must be actual Boolean values, not text.
    for field in ["encryption", "screen_lock"]:
        if not isinstance(device[field], bool):
            issues.append(f"Invalid Boolean value for field: {field}")

    # Stop before policy comparisons if any value has the wrong type.
    # For example, this prevents comparing "fifteen" with the number 14.
    if issues:
        return {
            "status": "NON-COMPLIANT",
            "risk_level": "HIGH",
            "issues": issues,
        }

    # Begin policy evaluation only after inventory validation succeeds.
    issues = []
    risk_level = "LOW"

    # Read the operating-system allowlist and minimum-version settings.
    allowed_os = policy["allowed_operating_systems"]
    minimum_versions = policy["minimum_os_versions"]

    # Unsupported operating systems are high risk.
    if device["os"] not in allowed_os:
        issues.append("Unsupported operating system")
        risk_level = "HIGH"
    else:
        # Retrieve the minimum version for this approved OS.
        minimum_version = minimum_versions.get(device["os"])

        # Validate the policy value before comparing versions.
        if (
            not isinstance(minimum_version, int)
            or isinstance(minimum_version, bool)
        ):
            issues.append(
                f"Missing or invalid minimum OS version for {device['os']}"
            )
            risk_level = "HIGH"
        elif device["os_version"] < minimum_version:
            issues.append("OS version too old")
            risk_level = "HIGH"

    # Required encryption must be enabled.
    if policy["require_encryption"] and not device["encryption"]:
        issues.append("Encryption disabled")
        if risk_level != "HIGH":
            risk_level = "MEDIUM"

    # Required screen locking must be enabled.
    if policy["require_screen_lock"] and not device["screen_lock"]:
        issues.append("Screen lock disabled")
        if risk_level != "HIGH":
            risk_level = "MEDIUM"

    # A device passes only if no policy violations were found.
    status = "NON-COMPLIANT" if issues else "COMPLIANT"

    return {
        "status": status,
        "risk_level": risk_level,
        "issues": issues,
    }


def load_json_file(filename):
    """Read a JSON file and return the parsed Python data."""
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    """Load the fleet, evaluate devices, print results, and export CSV."""

    # Load simulated inventory and the organization's policy.
    devices = load_json_file("devices.json")
    policy = load_json_file("policy.json")

    print("ENDPOINT FLEET COMPLIANCE REPORT")
    print("--------------------------------")

    compliant_devices = 0
    report_rows = []

    # Evaluate each device separately.
    for device in devices:
        result = evaluate_device(device, policy)

        status = result["status"]
        risk_level = result["risk_level"]
        issues = result["issues"]

        # Count devices that satisfy every configured requirement.
        if status == "COMPLIANT":
            compliant_devices += 1

        # Use safe lookups so malformed records can still be reported.
        if isinstance(device, dict):
            device_id = device.get("id", "UNKNOWN")
            owner = device.get("owner", "UNKNOWN")
        else:
            device_id = "UNKNOWN"
            owner = "UNKNOWN"

        print(f"{device_id} | {owner} | {status} | Risk: {risk_level}")

        # Print all issues to make remediation clear.
        for issue in issues:
            print(f"    ISSUE: {issue}")

        # Prepare a readable issue summary for the CSV.
        issue_text = "; ".join(issues) if issues else "None"

        # Preserve available inventory values in the report.
        # Missing values are represented by empty strings.
        report_rows.append({
            "Device ID": device.get("id", "") if isinstance(device, dict) else "",
            "Owner": device.get("owner", "") if isinstance(device, dict) else "",
            "Operating System": device.get("os", "") if isinstance(device, dict) else "",
            "OS Version": device.get("os_version", "") if isinstance(device, dict) else "",
            "Encryption Enabled": device.get("encryption", "") if isinstance(device, dict) else "",
            "Screen Lock Enabled": device.get("screen_lock", "") if isinstance(device, dict) else "",
            "Status": status,
            "Risk Level": risk_level,
            "Issues": issue_text,
        })

    # Calculate the fleet totals and overall compliance percentage.
    total_devices = len(devices)
    non_compliant_devices = total_devices - compliant_devices
    compliance_rate = (
        compliant_devices / total_devices * 100 if total_devices else 0.0
    )

    print("--------------------------------")
    print(f"Total devices: {total_devices}")
    print(f"Compliant devices: {compliant_devices}")
    print(f"Non-compliant devices: {non_compliant_devices}")
    print(f"Fleet compliance: {compliance_rate:.1f}%")

    # Keep the report columns consistent between runs.
    fieldnames = [
        "Device ID",
        "Owner",
        "Operating System",
        "OS Version",
        "Encryption Enabled",
        "Screen Lock Enabled",
        "Status",
        "Risk Level",
        "Issues",
    ]

    # Write the report, replacing the previous generated CSV.
    with open(
        "compliance_report.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(report_rows)

    print("CSV report saved: compliance_report.csv")


# Only run the report when this file is executed directly.
# Importing evaluate_device from the test file will not generate a report.
if __name__ == "__main__":
    main()
