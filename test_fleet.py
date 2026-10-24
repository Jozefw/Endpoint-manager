
"""
fleet.py

Purpose:
    Evaluate simulated endpoint devices against a configurable security
    policy, print a compliance report, and export results to CSV.

Validation:
    Check that inventory records contain all required fields and use
    the correct data types before performing policy comparisons.

Risk model:
    LOW    - The device passes all configured policy requirements.
    MEDIUM - A security setting, such as encryption, fails a requirement.
    HIGH   - The operating system is unsupported, the OS is too old,
             or the inventory data cannot be evaluated safely.

Important:
    All inventory data is simulated. This script does not collect
    settings from real computers.
"""

import csv
import json


def evaluate_device(device, policy):
    """
    Validate and evaluate one device against the supplied policy.

    Parameters:
        device: Dictionary containing one device's inventory data.
        policy: Dictionary containing the organization's requirements.

    Returns:
        A dictionary containing:
            status: COMPLIANT or NON-COMPLIANT
            risk_level: LOW, MEDIUM, or HIGH
            issues: List of validation or policy problems

    Safety:
        Invalid or incomplete inventory data is marked HIGH risk.
        The function returns early when the data cannot be evaluated
        safely, avoiding KeyError and TypeError crashes.
    """

    # Collect every validation or compliance problem found.
    issues = []

    # A device record must be a dictionary before we can inspect fields.
    # This also protects against unexpected JSON values such as strings,
    # lists, numbers, or null appearing in the inventory.
    if not isinstance(device, dict):
        return {
            "status": "NON-COMPLIANT",
            "risk_level": "HIGH",
            "issues": ["Invalid device record: expected a JSON object"],
        }

    # Define the fields needed by the compliance engine and report.
    required_fields = [
        "id",
        "owner",
        "os",
        "os_version",
        "encryption",
        "screen_lock",
    ]

    # Check for missing fields before attempting to access their values.
    for field in required_fields:
        if field not in device:
            issues.append(f"Missing required field: {field}")

    # Stop here if required information is missing.
    # This prevents later checks from raising KeyError.
    if issues:
        return {
            "status": "NON-COMPLIANT",
            "risk_level": "HIGH",
            "issues": issues,
        }

    # Device ID and owner must be non-empty strings.
    for field in ["id", "owner"]:
        if not isinstance(device[field], str) or not device[field].strip():
            issues.append(f"Invalid value for field: {field}")

    # The operating system must be a non-empty string.
    if not isinstance(device["os"], str) or not device["os"].strip():
        issues.append("Invalid operating system value")

    # The OS version must be an integer.
    # In Python, bool is a subclass of int, so explicitly reject True
    # and False as OS version values.
    if (
        not isinstance(device["os_version"], int)
        or isinstance(device["os_version"], bool)
    ):
        issues.append("Invalid OS version value")

    # Security settings must be actual Boolean values, not strings
    # such as "true", "false", "yes", or "no".
    for field in ["encryption", "screen_lock"]:
        if not isinstance(device[field], bool):
            issues.append(f"Invalid Boolean value for field: {field}")

    # Do not compare versions or evaluate security settings when the
    # inventory contains invalid values. Flag the record for review.
    # This early return prevents errors such as comparing "fifteen"
    # with the integer 14.
    if issues:
        return {
            "status": "NON-COMPLIANT",
            "risk_level": "HIGH",
            "issues": issues,
        }

    # The record is structurally valid, so begin policy evaluation.
    # A compliant device keeps LOW risk unless a rule raises the level.
    risk_level = "LOW"

    # Read the approved operating systems and minimum versions.
    allowed_os = policy["allowed_operating_systems"]
    minimum_versions = policy["minimum_os_versions"]

    # Reject operating systems that are not on the approved allowlist.
    if device["os"] not in allowed_os:
        issues.append("Unsupported operating system")
        risk_level = "HIGH"

    else:
        # The policy should define a minimum version for every allowed OS.
        # Use .get() so an incomplete policy can be reported rather than
        # causing a KeyError during the version lookup.
        minimum_version = minimum_versions.get(device["os"])

        # Validate the policy's minimum version before comparing values.
        if (
            not isinstance(minimum_version, int)
            or isinstance(minimum_version, bool)
        ):
            issues.append(
                f"Missing or invalid minimum OS version for {device['os']}"
            )
            risk_level = "HIGH"

        # Both values are integers here, so the comparison is safe.
        elif device["os_version"] < minimum_version:
            issues.append("OS version too old")
            risk_level = "HIGH"

    # Check encryption only when the policy requires it.
    if policy["require_encryption"] and not device["encryption"]:
        issues.append("Encryption disabled")

        # Preserve HIGH risk if another check already raised the risk.
        if risk_level != "HIGH":
            risk_level = "MEDIUM"

    # Check screen-lock configuration only when required.
    if policy["require_screen_lock"] and not device["screen_lock"]:
        issues.append("Screen lock disabled")

        # Preserve HIGH risk if another check already raised the risk.
        if risk_level != "HIGH":
            risk_level = "MEDIUM"

    # Any detected issue makes the device non-compliant.
    status = "NON-COMPLIANT" if issues else "COMPLIANT"

    # Return a consistent result that can be used by tests and reports.
    return {
        "status": status,
        "risk_level": risk_level,
        "issues": issues,
    }


def load_json_file(filename):
    """
    Load a JSON file and return its contents as Python data.

    Keeping file loading in one helper avoids repeating the same
    open-and-parse logic for the inventory and policy.
    """

    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    """
    Run the endpoint fleet reporting workflow.

    Load simulated devices and policy, evaluate every record, calculate
    fleet statistics, and write the results to a CSV report.
    """

    # Load the simulated inventory and compliance policy.
    devices = load_json_file("devices.json")
    policy = load_json_file("policy.json")

    print("ENDPOINT FLEET COMPLIANCE REPORT")
    print("--------------------------------")

    # Track how many devices meet every configured requirement.
    compliant_devices = 0

    # Keep report rows in memory until all devices have been evaluated.
    report_rows = []

    # Evaluate each inventory record independently.
    for device in devices:
        result = evaluate_device(device, policy)

        # Extract the evaluation results.
        status = result["status"]
        risk_level = result["risk_level"]
        issues = result["issues"]

        # Count only fully compliant devices.
        if status == "COMPLIANT":
            compliant_devices += 1

        # Use .get() when displaying fields so missing data does not
        # crash the report after the evaluator has flagged the record.
        device_id = device.get("id", "UNKNOWN") if isinstance(device, dict) else "UNKNOWN"
        owner = device.get("owner", "UNKNOWN") if isinstance(device, dict) else "UNKNOWN"

        # Print a concise result line for each device.
        print(
            f"{device_id} | {owner} | "
            f"{status} | Risk: {risk_level}"
        )

        # Show each detected problem on its own line.
        for issue in issues:
            print(f"    ISSUE: {issue}")

        # Convert the issue list into one readable CSV field.
        issue_text = "; ".join(issues) if issues else "None"

        # Preserve available inventory values in the report.
        # Missing values are represented by an empty string.
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

    # Calculate fleet-wide totals.
    total_devices = len(devices)
    non_compliant_devices = total_devices - compliant_devices

    # Avoid division by zero if the inventory contains no devices.
    if total_devices > 0:
        compliance_rate = compliant_devices / total_devices * 100
    else:
        compliance_rate = 0.0

    # Display the summary for a quick fleet health check.
    print("--------------------------------")
    print(f"Total devices: {total_devices}")
    print(f"Compliant devices: {compliant_devices}")
    print(f"Non-compliant devices: {non_compliant_devices}")
    print(f"Fleet compliance: {compliance_rate:.1f}%")

    # Define the CSV columns and their order.
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

    # Create or overwrite the report in the project folder.
    with open(
        "compliance_report.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the column header, then one row per device.
        writer.writeheader()
        writer.writerows(report_rows)

    print("CSV report saved: compliance_report.csv")


# Run the report only when this file is executed directly.
# Importing evaluate_device() from the test file will not run main().
if __name__ == "__main__":
    main()
