# Phase 1 README: Endpoint Compliance Proof of Concept

## Objective

Build a local Python tool to evaluate a simulated endpoint fleet against security policy requirements.

## Implemented Features

- **Inventory:** Six simulated endpoint devices in `devices.json`.
- **Policy:** Approved operating systems, minimum OS versions, encryption, and screen-lock requirements in `policy.json`.
- **Compliance engine:** `fleet.py` validates inventory data, evaluates policy, assigns risk levels, and identifies violations.
- **Reporting:** Generates `compliance_report.csv` with device status, risk levels, and findings.
- **Input validation:** Handles missing required fields and invalid data types safely.
- **Automated testing:** Eight unit tests using Python's `unittest` framework.

## Compliance Results

| Metric | Result |
|---|---:|
| Total devices | 6 |
| Compliant | 4 |
| Non-compliant | 2 |
| Fleet compliance | 66.7% |
| Unit tests passed | 8 of 8 |

The two non-compliant examples demonstrate detection of disabled encryption and an unsupported operating system.

## Unit Tests

Run the tests:

```bash
python3 -m unittest -v
```

Eight scenarios are covered:

1. Fully compliant device
2. Encryption disabled
3. Screen lock disabled
4. Unsupported operating system
5. OS version below minimum
6. Multiple policy violations
7. Missing required field
8. Invalid OS version data type

## Run the Compliance Engine

```bash
python3 fleet.py
```

The script prints a compliance summary and generates or refreshes `compliance_report.csv`.

## Project Files

- `fleet.py` — Compliance evaluation and reporting
- `devices.json` — Simulated endpoint inventory
- `policy.json` — Security policy
- `test_fleet.py` — Automated tests
- `compliance_report.csv` — Generated report
- `RUNBOOK.md` — Operating and troubleshooting instructions

## Scope

All endpoint data is simulated. The project runs locally and requires no paid services or cloud infrastructure.

## Checkpoint

Git commit: `a9fed46` — Complete endpoint compliance proof of concept

## Next Phase

**Phase 2: Configuration Baselines and Drift Detection.** Compare device settings with expected configurations and identify configuration changes or drift.
