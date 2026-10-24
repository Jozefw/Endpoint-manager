"""
fleet.py

Purpose:
    Evaluate simulated endpoint devices against a configurable
    security policy, print a compliance report, and export results
    to a CSV file.

Project note:
    All device records are simulated. This script does not collect
    settings from real computers.
"""

import csv
import json


def evaluate_device(device, policy):
    """
    Evaluate one device against the supplied policy.

    Args:
        device: A dictionary containing a device's simulated settings.
        policy: A dictionary containing the organization's requirements.

    Returns:
        A dictionary containing the compliance status, risk level,
        and a list of issues found.

    Why this is a function:
        Separating the evaluation logic makes it reusable and allows
        automated tests to check it without generating a report.
    """

    # Start with an empty list. Every failed requirement adds an issue.
    issues = []

    # LOW is the default risk for a device with no policy violations.
    # Serious operating-system problems can raise this to HIGH.
    risk_level = "LOW"

    # Read the operating-system requirements from the policy.
    allowed_os = policy["allowed_operating_systems"]
    minimum_versions = policy["minimum_os_versions"]

    # Check whether the device uses an operating system approved
    # by the policy. An unsupported OS cannot be version-checked
    # using our configured minimum-version rules.
    if device["os"] not in allowed_os:
        issues.append("Unsupported operating system")
        risk_level = "HIGH"

    else:
        # Find the minimum acceptable version for this OS.
        minimum_version = minimum_versions[device["os"]]

        # Compare the simulated version against the policy minimum.
        if device["os_version"] < minimum_version:
            issues.append("OS version too old")
            risk_level = "HIGH"

    # Check disk encryption only when the policy requires it.
    # If encryption is required but disabled, record a violation.
    if policy["require_encryption"] and not device["encryption"]:
        issues.append("Encryption disabled")

        # Do not downgrade HIGH risk if another serious issue exists.
        if risk_level != "HIGH":
            risk_level = "MEDIUM"

    # Check screen-lock settings only when required by the policy.
    if policy["require_screen_lock"] and not device["screen_lock"]:
        issues.append("Screen lock disabled")

        # Preserve HIGH risk if an OS issue was already found.
        if risk_level != "HIGH":
            risk_level = "MEDIUM"

    # A device is compliant only when no issues were identified.
    if issues:
        status = "NON-COMPLIANT"
    else:
        status = "COMPLIANT"

    # Return structured results so other code and tests can use them.
    return {
        "status": status,
        "risk_level": risk_level,
        "issues": issues,
    }


def load_json_file(filename):
    """
    Read a JSON file and convert its contents into Python data.

    Keeping file loading in a function avoids repeating the same
    open-and-load code for the inventory and policy files.
    """
    with open(filename, "r") as file:
        return json.load(file)


def main():
    """
    Run the complete reporting workflow.

    This function loads the files, evaluates every device, prints
    the fleet summary, and writes the detailed CSV report.
    """

    # Load the simulated device inventory and compliance policy.
    devices = load_json_file("devices.json")
    policy = load_json_file("policy.json")

    print("ENDPOINT FLEET COMPLIANCE REPORT")
    print("--------------------------------")

    # Track the number of compliant devices for fleet-wide statistics.
    compliant_devices = 0

    # Collect one report row per device for the CSV export.
    report_rows = []

    # Evaluate each device independently against the same policy.
    for device in devices:
        result = evaluate_device(device, policy)

        # Extract the results returned by our evaluation function.
        status = result["status"]
        risk_level = result["risk_level"]
        issues = result["issues"]

        # Count compliant devices so we can calculate the fleet rate.
        if status == "COMPLIANT":
            compliant_devices += 1

        # Print the device's summary and any policy violations.
        print(
            f'{device["id"]} | {device["owner"]} | '
            f'{status} | Risk: {risk_level}'
        )

        for issue in issues:
            print(f"    ISSUE: {issue}")

        # Convert the issue list into a readable CSV field.
        # Devices without issues receive the text "None".
        issue_text = "; ".join(issues) if issues else "None"

        # Store both the original inventory fields and the evaluation
        # results so the CSV contains useful troubleshooting details.
        report_rows.append({
            "Device ID": device["id"],
            "Owner": device["owner"],
            "Operating System": device["os"],
            "OS Version": device["os_version"],
            "Encryption Enabled": device["encryption"],
            "Screen Lock Enabled": device["screen_lock"],
            "Status": status,
            "Risk Level": risk_level,
            "Issues": issue_text,
        })

    # Calculate fleet-wide statistics after all devices are checked.
    total_devices = len(devices)
    non_compliant_devices = total_devices - compliant_devices

    # Avoid dividing by zero if the inventory contains no devices.
    if total_devices > 0:
        compliance_rate = compliant_devices / total_devices * 100
    else:
        compliance_rate = 0.0

    # Print the overall fleet summary.
    print("--------------------------------")
    print(f"Total devices: {total_devices}")
    print(f"Compliant devices: {compliant_devices}")
    print(f"Non-compliant devices: {non_compliant_devices}")
    print(f"Fleet compliance: {compliance_rate:.1f}%")

    # Define the column order for the exported CSV report.
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

    # Write the report to a file that can be opened in Excel or Numbers.
    # newline="" helps Python write CSV rows correctly on different systems.
    with open("compliance_report.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the column headings first, followed by every device row.
        writer.writeheader()
        writer.writerows(report_rows)

    print("CSV report saved: compliance_report.csv")


# Run the reporting workflow only when this file is executed directly.
# Importing evaluate_device from a test file will not run the report.
if __name__ == "__main__":
    main()