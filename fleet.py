import json

# Load simulated endpoint inventory
with open("devices.json", "r") as file:
    devices = json.load(file)

# Load compliance policy
with open("policy.json", "r") as file:
    policy = json.load(file)

allowed_os = policy["allowed_operating_systems"]
minimum_versions = policy["minimum_os_versions"]
require_encryption = policy["require_encryption"]
require_screen_lock = policy["require_screen_lock"]

print("ENDPOINT FLEET COMPLIANCE REPORT")
print("--------------------------------")

compliant_devices = 0

for device in devices:
    issues = []

    # Check whether the operating system is allowed
    if device["os"] not in allowed_os:
        issues.append("Unsupported operating system")
    else:
        minimum_version = minimum_versions[device["os"]]

        if device["os_version"] < minimum_version:
            issues.append("OS version too old")

    # Check disk encryption when required by policy
    if require_encryption and not device["encryption"]:
        issues.append("Encryption disabled")

    # Check screen lock when required by policy
    if require_screen_lock and not device["screen_lock"]:
        issues.append("Screen lock disabled")

    # Determine compliance
    if not issues:
        status = "COMPLIANT"
        compliant_devices += 1
    else:
        status = "NON-COMPLIANT"

    print(f'{device["id"]} | {device["owner"]} | {status}')

    for issue in issues:
        print(f"    ISSUE: {issue}")

# Calculate fleet statistics
total_devices = len(devices)
non_compliant_devices = total_devices - compliant_devices

if total_devices > 0:
    compliance_rate = compliant_devices / total_devices * 100
else:
    compliance_rate = 0.0

print("--------------------------------")
print(f"Total devices: {total_devices}")
print(f"Compliant devices: {compliant_devices}")
print(f"Non-compliant devices: {non_compliant_devices}")
print(f"Fleet compliance: {compliance_rate:.1f}%")